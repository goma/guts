from __future__ import annotations
import argparse
import datetime
import os
import platform
import socket
import sys
from pathlib import Path
from typing import List, Optional

from .config import GUTSConfig, load_config
from .discovery import discover_problems, filter_problems, validate_features
from .executor import run_suite
from .models import RunMeta, RunResult, StatusCode
from .reports import write_html_report, write_json_report, write_text_report
from .requirements import get_goma_capabilities


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pyguts",
        description="GUTS Python test harness for GOMA finite element solver.",
    )
    p.add_argument(
        "-g", "--goma",
        metavar="PATH",
        help="Path to GOMA executable (overrides config file).",
    )
    p.add_argument(
        "-f", "--feature",
        metavar="FEATURE",
        action="append",
        dest="features",
        default=[],
        help="Run only problems with this feature tag (stackable).",
    )
    p.add_argument(
        "-p", "--problem",
        metavar="NAME",
        action="append",
        dest="problems",
        default=[],
        help="Run only this problem by name (stackable).",
    )
    p.add_argument(
        "-t",
        metavar="NUM",
        dest="max_problem_time",
        type=int,
        default=None,
        help="Skip problems whose estimated_time_minutes exceeds NUM.",
    )
    p.add_argument(
        "-T",
        metavar="NUM",
        dest="max_total_time",
        type=int,
        default=None,
        help="Stop the suite after NUM total minutes.",
    )
    p.add_argument(
        "-j", "--jobs",
        metavar="N",
        type=int,
        default=1,
        help="Number of parallel worker processes (default: 1).",
    )
    p.add_argument(
        "-k", "--keep",
        action="store_true",
        help="Keep all files in data directory (no cleanup).",
    )
    p.add_argument(
        "--no-sort",
        action="store_true",
        help="Do not sort problems by estimated time before running.",
    )
    p.add_argument(
        "--exodiff-bin",
        metavar="DIR",
        default=None,
        help="Directory containing exodiff/decomp/epu (overrides config).",
    )
    p.add_argument(
        "--config",
        metavar="FILE",
        default=None,
        help="Path to local_config.ini (default: scripts/local_config.ini).",
    )
    p.add_argument(
        "-m", "--email",
        metavar="ADDR",
        default=None,
        help="Override result notification email address.",
    )
    p.add_argument(
        "--output-dir",
        metavar="DIR",
        default=None,
        help="Root directory for results/ and data/ output (default: repo root).",
    )
    p.add_argument(
        "--json",
        metavar="PATH",
        default=None,
        help="Write JSON results to this file.",
    )
    p.add_argument(
        "--problems-dir",
        metavar="DIR",
        default=None,
        help="Override the default problems/ directory.",
    )
    p.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print per-problem progress as results arrive.",
    )
    return p


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    scripts_dir = str(Path(__file__).resolve().parent.parent)

    cfg = load_config(
        ini_path=args.config,
        goma_override=args.goma,
        exodiff_bin_override=args.exodiff_bin,
        email_override=args.email,
        scripts_dir=scripts_dir,
    )

    if not cfg.goma_exe:
        parser.error(
            "GOMA executable not specified. Use -g/--goma or set 'goma' in local_config.ini."
        )
    if not Path(cfg.goma_exe).is_file():
        parser.error(f"GOMA executable not found: {cfg.goma_exe}")

    # Determine output and problems directories
    repo_root = str(Path(scripts_dir).parent)
    output_dir = args.output_dir or repo_root
    problems_dir_path = Path(args.problems_dir or os.path.join(repo_root, "problems"))

    if not problems_dir_path.is_dir():
        parser.error(f"Problems directory not found: {problems_dir_path}")

    # Validate requested features
    unknown = validate_features(args.features)
    if unknown:
        print(f"  Warning: unknown feature(s): {', '.join(unknown)}", file=sys.stderr)

    # Discover and filter problems
    print(f"  -> Discovering problems in {problems_dir_path} ...")
    all_problems = discover_problems(problems_dir_path)
    print(f"  -> Found {len(all_problems)} problems.")

    to_run, skipped = filter_problems(
        all_problems,
        requested_names=args.problems,
        required_features=args.features,
        max_time_minutes=args.max_problem_time,
    )

    if not to_run:
        print("  -> No problems to run after filtering.")
        sys.exit(0)

    n_skip_display = len([s for s in skipped if s[1] != "not_requested"])
    print(f"  -> Running {len(to_run)} problems ({n_skip_display} skipped).")

    # Parse GOMA capabilities once
    print(f"  -> Checking GOMA build: {cfg.goma_exe}")
    caps = get_goma_capabilities(cfg.goma_exe, cfg.subprocess_env())
    if not caps.version_output_present:
        print("  -> 'goma -v' did not report build flags; skipping requirement checks.")
    else:
        print(f"  -> MDE={caps.mde} MAX_PROB_VAR={caps.max_prob_var} "
              f"MAX_CONC={caps.max_conc} PARALLEL={caps.is_parallel}")

    # Set up run metadata
    now = datetime.datetime.now()
    plat = platform.system().lower()
    host = socket.gethostname()
    data_dir_name = f"{plat}_{host}_{now.strftime('%m%d%y_%H%M%S')}"
    data_base_dir = Path(output_dir) / "data" / data_dir_name

    command_line = " ".join(sys.argv)

    meta = RunMeta(
        start_time=now,
        host=host,
        platform=plat,
        goma_exe=cfg.goma_exe,
        command_line=command_line,
        output_dir=output_dir,
        data_dir_name=data_dir_name,
        problems_dir=str(problems_dir_path),
        scripts_dir=scripts_dir,
    )

    data_base_dir.mkdir(parents=True, exist_ok=True)

    # Progress callback
    def _progress(result: RunResult) -> None:
        if args.verbose:
            c = result.check
            p = result.problem
            status = "ABORT" if c.abort_reason else ("PASS" if c.passed() else "FAIL")
            elapsed = f"{c.elapsed_seconds:.1f}s"
            print(
                f"  [{status:5s}] {p.name:<35s} "
                f"SOUT={c.sout_code.value} SERR={c.serr_code.value} "
                f"EXEC={c.exec_code.value} ExoII={c.exo_code.value} "
                f"Norms={c.norm_code.value} Custom={c.cust_code.value} "
                f"({elapsed})"
            )
            if not c.abort_reason and not c.passed():
                data_dir = Path(c.data_dir)
                for label, fname in [("STDOUT", p.run.goma_sout), ("STDERR", p.run.goma_serr)]:
                    fpath = data_dir / fname
                    if fpath.is_file():
                        lines = fpath.read_text(errors="replace").splitlines()
                        tail = lines[-50:]
                        print(f"    -- tail {label} --")
                        for line in tail:
                            print(f"    {line}")
                if c.exo_code == StatusCode.FAILED and c.exo_log:
                    print("    -- exodiff comparison --")
                    for line in c.exo_log.splitlines():
                        print(f"    {line}")

    # Run the suite
    print(
        f"  -> Starting suite: {len(to_run)} problems, "
        f"{args.jobs} worker(s), data → {data_base_dir}"
    )
    results = run_suite(
        to_run,
        cfg,
        data_base_dir,
        caps,
        jobs=args.jobs,
        keep_files=args.keep,
        sort_by_time=not args.no_sort,
        total_time_limit_minutes=args.max_total_time,
        progress_callback=_progress,
    )

    # Write reports
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    results_dir = Path(output_dir) / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    txt_path = results_dir / f"results_{timestamp}.txt"
    html_path = results_dir / f"results_{timestamp}.html"
    json_path = results_dir / f"results_{timestamp}.json"

    # Also write to data dir
    data_txt_path = data_base_dir / "results.txt"
    data_html_path = data_base_dir / "results.html"
    data_json_path = data_base_dir / "results.json"

    print(f"  -> Writing results to {results_dir} ...")

    write_text_report(results, skipped, txt_path, meta)
    write_text_report(results, skipped, data_txt_path, meta)
    write_html_report(results, skipped, html_path, meta)
    write_html_report(results, skipped, data_html_path, meta)
    write_json_report(results, skipped, data_json_path, meta)

    # Symlinks to latest results
    for name, target in [("latest.txt", txt_path), ("latest.html", html_path)]:
        link = results_dir / name
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(target.name)

    if args.json:
        json_path = Path(args.json)
        write_json_report(results, skipped, json_path, meta)
        print(f"  -> JSON written to {json_path}")

    # Print summary
    print("")
    print("=" * 60)
    n_pass = sum(1 for r in results if r.check.passed() and not r.check.abort_reason)
    n_fail = sum(1 for r in results if not r.check.passed() and not r.check.abort_reason)
    n_abort = sum(1 for r in results if r.check.abort_reason)
    print(f"  RESULTS: {n_pass} passed, {n_fail} failed, {n_abort} aborted, {n_skip_display} skipped")
    print(f"  HTML:    {html_path}")
    print(f"  Text:    {txt_path}")
    print("=" * 60)

    # Exit with failure code if any problem failed
    if n_fail > 0 or n_abort > 0:
        sys.exit(1)
