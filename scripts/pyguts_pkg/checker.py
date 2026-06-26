from __future__ import annotations
import os
import re
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

from .models import CheckResult, ProblemConfig, StatusCode
from .config import GUTSConfig

_SERR_PATTERNS = [
    "Segmentation Fault",
    "Deformation Grad",
    "Bus Error",
    "NaN",
    "YUK",
    "FAILED",
    "non-convergence",
]

_SOUT_REQUIRED = "done"

_REGEXSCI = r"[0-9]*\.?[0-9]+[eE][+-][0-9]+"
_RESIDUAL_PAT = re.compile(
    r":[0-9][0-9]:[0-9][0-9] \[0\] " + _REGEXSCI + r" " + _REGEXSCI + r" " + _REGEXSCI
)
_CORRECTION_PAT = re.compile(
    _REGEXSCI + r" " + _REGEXSCI + r" " + _REGEXSCI
    + r"\s*[A-Za-z0-9]*\s*" + _REGEXSCI + r"/" + _REGEXSCI
)


def check_sout(sout_path: Path) -> Tuple[StatusCode, str]:
    if not sout_path.is_file():
        return StatusCode.FAILED, f"ERROR: stdout file missing: {sout_path.name}"
    text = sout_path.read_text(errors="replace")
    if _SOUT_REQUIRED in text:
        return StatusCode.OK, "PASSED: Standard output scan"
    return StatusCode.FAILED, f'FAILED: "{_SOUT_REQUIRED}" not found in stdout'


def check_serr(serr_path: Path) -> Tuple[StatusCode, str]:
    if not serr_path.is_file():
        return StatusCode.FAILED, f"ERROR: stderr file missing: {serr_path.name}"
    text = serr_path.read_text(errors="replace")
    found = []
    for pat in _SERR_PATTERNS:
        if pat in text:
            found.append(pat)
    if found:
        return StatusCode.FAILED, "FAILED: stderr contains: " + ", ".join(
            f'"{p}"' for p in found
        )
    return StatusCode.OK, "PASSED: Standard error scan"


def check_exec(return_code: int) -> Tuple[StatusCode, str]:
    if return_code == 0:
        return StatusCode.OK, "PASSED: Zero error-status check"
    return StatusCode.FAILED, f"FAILED: GOMA exited with status {return_code}"


def check_exodiff(
    config: ProblemConfig,
    data_dir: Path,
    guts_cfg: GUTSConfig,
) -> Tuple[StatusCode, str]:
    blessed_list = config.blessed.blessed_exo_output
    output_list = config.blessed.exo_output
    abs_tols = config.blessed.exo_abs_tol
    rel_tols = config.blessed.exo_rel_tol
    inp_files = config.blessed.exodiff_input_file

    if not blessed_list:
        return StatusCode.NA, "No ExodusII files to compare."

    overall = StatusCode.OK
    log_lines: List[str] = []

    for i, (blessed_name, output_name) in enumerate(zip(blessed_list, output_list)):
        abs_tol = abs_tols[i] if i < len(abs_tols) else guts_cfg.exo_abs_tol
        rel_tol = rel_tols[i] if i < len(rel_tols) else guts_cfg.exo_rel_tol
        eif_name = inp_files[i] if i < len(inp_files) else ""

        blessed_path = Path(config.source_dir) / blessed_name
        output_path = data_dir / output_name

        log_lines.append("")
        log_lines.append(f"o ExodusII comparison between:")
        log_lines.append(f"  -> Blessed file : {blessed_name}")
        log_lines.append(f"  -> test file    : {output_name}")
        log_lines.append(f"  -> absolute tol : {abs_tol}")
        log_lines.append(f"  -> relative tol : {rel_tol}")
        log_lines.append("")

        if not blessed_path.is_file():
            msg = f"ERROR: Blessed ExodusII file missing: {blessed_name}"
            log_lines.append(f"     * {msg}")
            overall = StatusCode.FAILED
            continue

        if not output_path.is_file():
            msg = f"ERROR: GOMA ExodusII file missing: {output_name}"
            log_lines.append(f"     * {msg}")
            overall = StatusCode.FAILED
            continue

        cmd = [
            guts_cfg.exodiff,
            "-stat",
            "-F", str(abs_tol),
            "-t", str(rel_tol),
        ]

        if eif_name:
            eif_path = data_dir / eif_name
            if not eif_path.is_file():
                eif_path = Path(config.source_dir) / eif_name
            if eif_path.is_file():
                cmd += ["-f", str(eif_path)]
            else:
                log_lines.append(f"     * WARNING: exodiff input file not found: {eif_name}")
        else:
            # Use default exodiff input if available
            default_inp = Path(guts_cfg.default_exodiff_inp)
            if default_inp.is_file():
                cmd += ["-f", str(default_inp)]

        cmd += [str(blessed_path), str(output_path)]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(data_dir),
            env=guts_cfg.subprocess_env(),
        )
        log_lines.append(result.stdout)
        log_lines.append(result.stderr)

        if result.returncode == 0:
            log_lines.append(
                f"     * PASSED: ExodusII comparison ({blessed_name} vs. {output_name})"
            )
        else:
            log_lines.append(
                f"     * FAILED: ExodusII comparison ({blessed_name} vs. {output_name})"
            )
            overall = StatusCode.FAILED

    return overall, "\n".join(log_lines)


def _extract_norm_string(text: str) -> str:
    res_m = _RESIDUAL_PAT.search(text)
    cor_m = _CORRECTION_PAT.search(text)

    parts = []
    if res_m:
        parts.append(res_m.group(0))
    parts.append(" ")
    if cor_m:
        parts.append(cor_m.group(0))

    joined = "".join(parts)
    # cut -d ' ' -f3-8 (fields are 1-indexed; Python: indices 2:8)
    fields = joined.split(" ")
    selected = " ".join(fields[2:8])
    return selected.replace("-00", "+00")


def check_norms(
    config: ProblemConfig,
    data_dir: Path,
) -> Tuple[StatusCode, str]:
    blessed_sout_name = config.blessed.sout
    goma_sout_name = config.run.goma_sout

    if not blessed_sout_name:
        return StatusCode.NA, "No blessed stdout file specified."

    blessed_sout = Path(config.source_dir) / blessed_sout_name
    goma_sout = data_dir / goma_sout_name

    if not blessed_sout.is_file():
        return StatusCode.FAILED, f"ERROR: Missing blessed stdout: {blessed_sout_name}"
    if not goma_sout.is_file():
        return StatusCode.FAILED, f"ERROR: Missing GOMA stdout: {goma_sout_name}"

    blessed_text = blessed_sout.read_text(errors="replace")
    goma_text = goma_sout.read_text(errors="replace")

    blessed_norms = _extract_norm_string(blessed_text)
    goma_norms = _extract_norm_string(goma_text)

    lines = [
        "Base Initial Residuals:",
        "--------------------------------------------------------",
        blessed_norms or "(none found)",
        "--------------------------------------------------------",
        "Current Version Residuals:",
        "--------------------------------------------------------",
        goma_norms or "(none found)",
        "--------------------------------------------------------",
    ]
    log = "\n".join(lines)

    if blessed_norms.split() == goma_norms.split():
        return StatusCode.OK, "PASSED: Norms comparison test\n\n" + log
    return StatusCode.FAILED, "FAILED: Norms comparison test\n\n" + log


def check_custom(
    config: ProblemConfig,
    data_dir: Path,
    guts_cfg: GUTSConfig,
) -> Tuple[StatusCode, str]:
    if not config.extra.extra_tests or not config.extra.extra_test_scripts:
        return StatusCode.NA, "No custom tests for this problem."

    log_lines: List[str] = []
    overall = StatusCode.OK

    base_env = guts_cfg.subprocess_env()
    extra_env = {
        **base_env,
        "GOMA_SOUT": str(data_dir / config.run.goma_sout),
        "GOMA_SERR": str(data_dir / config.run.goma_serr),
        "BLESSED_SOUT": str(Path(config.source_dir) / config.blessed.sout),
        "BLESSED_SERR": str(Path(config.source_dir) / config.blessed.serr),
        "custom_tests_file": str(data_dir / "custTests.txt"),
        "extra_test_code": str(data_dir / "extra_test_result"),
    }

    for scr_name in config.extra.extra_test_scripts:
        scr_path = data_dir / scr_name
        if not scr_path.is_file():
            scr_path = Path(config.source_dir) / scr_name

        log_lines.append(f"Custom Tests from script: {scr_name}")

        if not scr_path.is_file():
            log_lines.append(f"  ERROR: script not found: {scr_name}")
            overall = StatusCode.FAILED
            continue

        result = subprocess.run(
            ["/bin/bash", str(scr_path)],
            capture_output=True,
            text=True,
            cwd=str(data_dir),
            env=extra_env,
        )
        log_lines.append(result.stdout)
        if result.stderr:
            log_lines.append(result.stderr)

        code_file = data_dir / "extra_test_result.txt"
        if code_file.is_file():
            code_str = code_file.read_text().strip()
            if code_str.upper() != "OK":
                overall = StatusCode.FAILED
        elif result.returncode != 0:
            overall = StatusCode.FAILED

    return overall, "\n".join(log_lines)


def check_all(
    config: ProblemConfig,
    data_dir: Path,
    guts_cfg: GUTSConfig,
    return_code: int,
) -> CheckResult:
    result = CheckResult()

    sout_path = data_dir / config.run.goma_sout
    serr_path = data_dir / config.run.goma_serr

    result.sout_code, sout_log = check_sout(sout_path)
    result.serr_code, serr_log = check_serr(serr_path)
    result.exec_code, exec_log = check_exec(return_code)
    result.exo_code, result.exo_log = check_exodiff(config, data_dir, guts_cfg)
    result.norm_code, result.norm_log = check_norms(config, data_dir)
    result.cust_code, result.cust_log = check_custom(config, data_dir, guts_cfg)

    result.build_log = "\n".join([sout_log, serr_log, exec_log])
    return result
