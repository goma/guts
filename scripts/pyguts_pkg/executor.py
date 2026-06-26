from __future__ import annotations
import signal
import threading
import time
from concurrent.futures import ProcessPoolExecutor, wait as _wait, Future, CancelledError, FIRST_COMPLETED
from pathlib import Path
from typing import Callable, List, Optional

from .config import GUTSConfig
from .models import ProblemConfig, RunResult
from .requirements import GomaCapabilities
from .runner import run_problem, install_worker_sigterm_handler


def run_suite(
    problems: List[ProblemConfig],
    guts_cfg: GUTSConfig,
    data_base_dir: Path,
    caps: GomaCapabilities,
    *,
    jobs: int = 1,
    keep_files: bool = False,
    sort_by_time: bool = True,
    total_time_limit_minutes: Optional[int] = None,
    progress_callback: Optional[Callable[[RunResult], None]] = None,
) -> List[RunResult]:
    if sort_by_time:
        problems = sorted(
            problems, key=lambda p: p.estimated_time_minutes, reverse=True
        )

    suite_start = time.monotonic()
    results: List[RunResult] = []

    def _time_exceeded() -> bool:
        if total_time_limit_minutes is None:
            return False
        elapsed_min = (time.monotonic() - suite_start) / 60.0
        return elapsed_min >= total_time_limit_minutes

    if jobs <= 1:
        for prob in problems:
            if _time_exceeded():
                print(f"  -> Time limit reached, stopping before {prob.name}")
                break
            try:
                result = run_problem(prob, guts_cfg, data_base_dir, caps, keep_files)
            except KeyboardInterrupt:
                print("\n  -> Interrupted. Saving results collected so far.")
                break
            results.append(result)
            if progress_callback:
                progress_callback(result)
        return results

    # Parallel path
    interrupted = threading.Event()
    pool = ProcessPoolExecutor(max_workers=jobs, initializer=install_worker_sigterm_handler)
    futures: dict = {}

    def _shutdown_handler(signum, frame):
        if not interrupted.is_set():
            interrupted.set()
            print("\n  -> Interrupted. Cancelling pending problems; saving results.")
        for worker in (pool._processes or {}).values():
            try:
                worker.terminate()
            except Exception:
                pass
        # Do NOT call pool.shutdown() here — that nulls out the wakeup pipe
        # so the finally-block's shutdown(wait=True) can't re-wake the manager
        # thread, leaving it stuck in join_executor_internals().

    old_sigint = signal.getsignal(signal.SIGINT)
    old_sigterm = signal.getsignal(signal.SIGTERM)
    signal.signal(signal.SIGINT, _shutdown_handler)
    signal.signal(signal.SIGTERM, _shutdown_handler)

    try:
        for prob in problems:
            if interrupted.is_set():
                break
            fut = pool.submit(run_problem, prob, guts_cfg, data_base_dir, caps, keep_files)
            futures[fut] = prob

        pending = set(futures.keys())
        while pending and not interrupted.is_set():
            done, pending = _wait(pending, timeout=0.25, return_when=FIRST_COMPLETED)
            for fut in done:
                if interrupted.is_set():
                    break
                try:
                    result = fut.result()
                except CancelledError:
                    continue
                except BaseException as exc:
                    prob = futures[fut]
                    from .models import CheckResult, StatusCode
                    check = CheckResult(abort_reason=str(exc))
                    for attr in ("sout_code", "serr_code", "exec_code", "exo_code", "norm_code", "cust_code"):
                        setattr(check, attr, StatusCode.ABORT)
                    result = RunResult(problem=prob, check=check)

                results.append(result)
                if progress_callback:
                    progress_callback(result)

            if _time_exceeded():
                for f in pending:
                    f.cancel()
                pending = set()
                break
    finally:
        if interrupted.is_set():
            # Workers already received SIGTERM from _shutdown_handler, which
            # triggered _worker_sigterm_handler to kill GOMA.  Give them a
            # moment to finish that and exit before we SIGKILL stragglers.
            _procs = list((getattr(pool, "_processes", None) or {}).values())
            for _w in _procs:
                try:
                    _w.join(timeout=5)
                except Exception:
                    pass
            for _w in _procs:
                try:
                    if _w.is_alive():
                        _w.kill()
                except Exception:
                    pass
            for _w in _procs:
                try:
                    _w.join(timeout=2)
                except Exception:
                    pass
        # Prevent the call-queue feeder thread from blocking Python's atexit
        # when workers were killed and left a broken pipe behind.
        try:
            pool._call_queue.cancel_join_thread()
        except Exception:
            pass
        # Single shutdown with wait=True so the manager thread is fully joined
        # here, before Python's _python_exit atexit runs.
        try:
            pool.shutdown(wait=True, cancel_futures=True)
        except TypeError:
            pool.shutdown(wait=True)
        signal.signal(signal.SIGINT, old_sigint)
        signal.signal(signal.SIGTERM, old_sigterm)

    return results
