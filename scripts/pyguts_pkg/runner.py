from __future__ import annotations
import os
import shutil
import signal as _signal
import subprocess
import time
from pathlib import Path
from typing import List, Optional

from .checker import check_all
from .config import GUTSConfig
from .models import CheckResult, ProblemConfig, RunResult, StatusCode
from .requirements import GomaCapabilities, check_requirements

# Tracks the active GOMA subprocess in each worker process so a SIGTERM
# handler can kill it before the worker exits.
_current_goma_proc = None


def _worker_sigterm_handler(signum, frame):
    proc = _current_goma_proc
    if proc is not None:
        try:
            os.killpg(proc.pid, _signal.SIGKILL)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
    raise SystemExit(0)


def install_worker_sigterm_handler():
    """Call as ProcessPoolExecutor initializer so workers kill GOMA on SIGTERM."""
    _signal.signal(_signal.SIGTERM, _worker_sigterm_handler)


def _whack_files(data_dir: Path, names: List[str]) -> None:
    for name in names:
        f = data_dir / name
        if f.exists():
            f.unlink()


def _run_subprocess(cmd: List[str], data_dir: Path, env: dict, label: str) -> int:
    result = subprocess.run(
        cmd,
        cwd=str(data_dir),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode


def _clean_data_dir(data_dir: Path, config: ProblemConfig) -> None:
    keep = {
        config.run.goma_sout,
        config.run.goma_serr,
        "exec_status.txt",
        "exoComparison.txt",
        "normComparison.txt",
        "custTests.txt",
        "build.txt",
        "abort.txt",
    }
    for f in data_dir.iterdir():
        if f.is_file() and f.name not in keep:
            try:
                f.unlink()
            except Exception:
                pass
        elif f.is_dir():
            try:
                shutil.rmtree(f)
            except Exception:
                pass


def run_problem(
    config: ProblemConfig,
    guts_cfg: GUTSConfig,
    data_base_dir: Path,
    caps: GomaCapabilities,
    keep_files: bool,
) -> RunResult:
    data_dir = data_base_dir / config.name
    check = CheckResult()
    check.data_dir = str(data_dir)

    start = time.monotonic()

    # 1. Prepare data directory
    if data_dir.exists():
        shutil.rmtree(data_dir)
    shutil.copytree(config.source_dir, str(data_dir))

    # 2. Remove any stale generated files listed in whacked_files
    _whack_files(data_dir, list(config.extra.whacked_files))

    # 3. Check build requirements
    ok, failures = check_requirements(caps, config.requirements, config.run.num_processors)
    build_log_lines = []
    if not ok:
        build_log_lines.append("Build requirements not met:")
        build_log_lines.extend(f"  -> {f}" for f in failures)
        build_log_lines.append("Build rejected.")
        check.abort_reason = "; ".join(failures)
        check.build_log = "\n".join(build_log_lines)
        _write_file(data_dir / "abort.txt", check.abort_reason)
        _write_file(data_dir / "build.txt", check.build_log)
        check.elapsed_seconds = time.monotonic() - start
        check.sout_code = StatusCode.ABORT
        check.serr_code = StatusCode.ABORT
        check.exec_code = StatusCode.ABORT
        check.exo_code = StatusCode.ABORT
        check.norm_code = StatusCode.ABORT
        check.cust_code = StatusCode.ABORT
        return RunResult(problem=config, check=check)
    else:
        build_log_lines.append("Build accepted.")
        check.build_log = "\n".join(build_log_lines)
        _write_file(data_dir / "build.txt", check.build_log)

    # 4. Copy goma executable into data dir
    goma_exe_dest = data_dir / "goma.exe"
    try:
        shutil.copy2(guts_cfg.goma_exe, str(goma_exe_dest))
        goma_exe_dest.chmod(goma_exe_dest.stat().st_mode | 0o111)
    except Exception as exc:
        check.abort_reason = f"Failed to copy GOMA executable: {exc}"
        _write_file(data_dir / "abort.txt", check.abort_reason)
        check.elapsed_seconds = time.monotonic() - start
        for attr in ("sout_code", "serr_code", "exec_code", "exo_code", "norm_code", "cust_code"):
            setattr(check, attr, StatusCode.ABORT)
        return RunResult(problem=config, check=check)

    env = guts_cfg.subprocess_env()
    goma_exe_path = str(goma_exe_dest)

    # 5. Run ChemKin preprocessing if needed
    if config.run.use_chemkin and config.run.chemkin_input:
        rc = _run_subprocess(
            [guts_cfg.lqinterp, config.run.chemkin_input],
            data_dir,
            env,
            "chemkin",
        )
        if rc != 0:
            check.abort_reason = f"LQInterp returned error {rc}"
            _write_file(data_dir / "abort.txt", check.abort_reason)
            check.elapsed_seconds = time.monotonic() - start
            for attr in ("sout_code", "serr_code", "exec_code", "exo_code", "norm_code", "cust_code"):
                setattr(check, attr, StatusCode.ABORT)
            return RunResult(problem=config, check=check)

    # 6. Decompose mesh if parallel
    if config.run.use_decomp and config.run.brk_exo_in:
        decomp_cmd = [
            guts_cfg.decomp,
            "-p", str(config.run.num_processors),
            config.run.brk_exo_in,
        ]
        _run_subprocess(decomp_cmd, data_dir, env, "decomp")

    # 7. Build and run GOMA command
    sout_path = data_dir / config.run.goma_sout
    serr_path = data_dir / config.run.goma_serr

    if config.run.use_mpi and config.run.num_processors > 1:
        goma_cmd: List[str] = [
            guts_cfg.mpirun,
            "-np", str(config.run.num_processors),
            "--bind-to", "none",
        ]
        if guts_cfg.goma_machinefile:
            goma_cmd += ["-machinefile", guts_cfg.goma_machinefile]
        goma_cmd += [goma_exe_path, "-i", config.run.goma_input]
    else:
        goma_cmd = [goma_exe_path, "-i", config.run.goma_input]

    if config.run.goma_opts:
        goma_cmd.extend(config.run.goma_opts.split())

    if config.run.use_aprepro:
        goma_cmd.append("-a")
        if config.run.aprepro_flags:
            goma_cmd.extend(config.run.aprepro_flags.split())

    with open(sout_path, "w") as sout_f, open(serr_path, "w") as serr_f:
        proc = subprocess.Popen(
            goma_cmd,
            stdout=sout_f,
            stderr=serr_f,
            cwd=str(data_dir),
            env=env,
            start_new_session=True,
        )
        global _current_goma_proc
        _current_goma_proc = proc
        try:
            try:
                proc.wait()
            except (KeyboardInterrupt, SystemExit):
                try:
                    os.killpg(proc.pid, _signal.SIGTERM)
                except Exception:
                    proc.terminate()
                try:
                    proc.wait(timeout=5)
                except Exception:
                    try:
                        os.killpg(proc.pid, _signal.SIGKILL)
                    except Exception:
                        proc.kill()
                    proc.wait()
                raise
        finally:
            _current_goma_proc = None
    goma_return_code = proc.returncode
    _write_file(data_dir / "exec_status.txt", f"GOMA Execution Status: {goma_return_code}\n")

    # 8. Reassemble parallel output
    if config.run.use_decomp and config.run.fix_exo_basename:
        epu_cmd = [
            guts_cfg.epu,
            "-auto",
            f"{config.run.fix_exo_basename}.exoII.{config.run.num_processors}.0",
        ]
        _run_subprocess(epu_cmd, data_dir, env, "epu")

    # 9. Run all checks
    check = check_all(config, data_dir, guts_cfg, goma_return_code)
    check.data_dir = str(data_dir)
    check.elapsed_seconds = time.monotonic() - start

    # Write comparison logs to files
    _write_file(data_dir / "exoComparison.txt", check.exo_log)
    _write_file(data_dir / "normComparison.txt", check.norm_log)
    _write_file(data_dir / "custTests.txt", check.cust_log)
    _write_file(data_dir / "build.txt", check.build_log)

    # 10. Clean data directory unless keeping files
    if not keep_files:
        _clean_data_dir(data_dir, config)

    return RunResult(problem=config, check=check)


def _write_file(path: Path, content: str) -> None:
    try:
        path.write_text(content)
    except Exception:
        pass
