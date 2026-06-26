from __future__ import annotations
import json
import re
from pathlib import Path
from typing import List, Optional, Tuple

from .models import (
    CheckResult,
    ContactInfo,
    ProblemBlessed,
    ProblemConfig,
    ProblemExtra,
    ProblemRequirements,
    ProblemRun,
    RunResult,
    StatusCode,
)
from .known_features import KNOWN_FEATURES


def load_problem_config(prob_dir: Path) -> ProblemConfig:
    with open(prob_dir / "problem.json") as f:
        d = json.load(f)

    contact = d.get("contact", {})
    reqs = d.get("requirements", {})
    run = d.get("run", {})
    blessed = d.get("blessed", {})
    extra = d.get("extra", {})

    return ProblemConfig(
        name=d["name"],
        description=d.get("description", ""),
        contact=ContactInfo(
            name=contact.get("name", ""),
            email=contact.get("email", ""),
        ),
        estimated_time_minutes=int(d.get("estimated_time_minutes", 0)),
        disabled=bool(d.get("disabled", False)),
        features=tuple(d.get("features", [])),
        requirements=ProblemRequirements(
            max_prob_var=int(reqs.get("max_prob_var", 0)),
            max_conc=int(reqs.get("max_conc", 0)),
            mde=int(reqs.get("mde", 0)),
            solver_package=reqs.get("solver_package", ""),
            use_arpack=reqs.get("use_arpack", "no"),
            enable_omega_h=reqs.get("enable_omega_h", ""),
        ),
        run=ProblemRun(
            use_aprepro=bool(run.get("use_aprepro", False)),
            aprepro_flags=run.get("aprepro_flags", ""),
            use_chemkin=bool(run.get("use_chemkin", False)),
            chemkin_input=run.get("chemkin_input", ""),
            use_mpi=bool(run.get("use_mpi", False)),
            num_processors=int(run.get("num_processors", 1)),
            use_decomp=bool(run.get("use_decomp", False)),
            brk_input=run.get("brk_input", ""),
            brk_exo_in=run.get("brk_exo_in", ""),
            fix_exo_basename=run.get("fix_exo_basename", ""),
            goma_input=run.get("goma_input", ""),
            goma_serr=run.get("goma_serr", "serr.txt"),
            goma_sout=run.get("goma_sout", "sout.txt"),
            goma_opts=run.get("goma_opts", ""),
        ),
        blessed=ProblemBlessed(
            serr=blessed.get("serr", ""),
            sout=blessed.get("sout", ""),
            exo_output=tuple(blessed.get("exo_output", [])),
            blessed_exo_output=tuple(blessed.get("blessed_exo_output", [])),
            exo_abs_tol=tuple(float(x) for x in blessed.get("exo_abs_tol", [])),
            exo_rel_tol=tuple(float(x) for x in blessed.get("exo_rel_tol", [])),
            exodiff_input_file=tuple(blessed.get("exodiff_input_file", [])),
        ),
        extra=ProblemExtra(
            whacked_files=tuple(extra.get("whacked_files", [])),
            extra_tests=bool(extra.get("extra_tests", False)),
            extra_test_scripts=tuple(extra.get("extra_test_scripts", [])),
        ),
        source_dir=str(prob_dir.resolve()),
    )


def discover_problems(problems_dir: Path) -> List[ProblemConfig]:
    problems = []
    for entry in sorted(problems_dir.iterdir()):
        if not entry.is_dir():
            continue
        if not (entry / "problem.json").is_file():
            continue
        try:
            problems.append(load_problem_config(entry))
        except Exception as exc:
            print(f"  Warning: skipping {entry.name}: {exc}")
    return problems


def validate_features(features: List[str]) -> List[str]:
    unknown = []
    for f in features:
        if f.startswith("bc_") or f.startswith("eq_"):
            continue
        if f not in KNOWN_FEATURES:
            unknown.append(f)
    return unknown


def _file_contains(filepath: Path, pattern: str) -> bool:
    try:
        text = filepath.read_text(errors="replace").lower()
        return pattern.lower() in text
    except Exception:
        return False


def prob_matches_features(p: ProblemConfig, required: List[str]) -> bool:
    for feat in required:
        if feat.startswith("bc_"):
            bc_name = feat[3:]
            input_file = Path(p.source_dir) / p.run.goma_input
            if not _file_contains(input_file, f"bc = {bc_name}"):
                return False
        elif feat.startswith("eq_"):
            eq_name = feat[3:]
            input_file = Path(p.source_dir) / p.run.goma_input
            if not _file_contains(input_file, f"eq = {eq_name}"):
                return False
        else:
            if feat not in p.features:
                return False
    return True


def filter_problems(
    problems: List[ProblemConfig],
    requested_names: List[str],
    required_features: List[str],
    max_time_minutes: Optional[int],
) -> Tuple[List[ProblemConfig], List[Tuple[ProblemConfig, str]]]:
    requested_set = set(requested_names)
    to_run: List[ProblemConfig] = []
    skipped: List[Tuple[ProblemConfig, str]] = []

    for p in problems:
        explicitly_requested = p.name in requested_set

        # If names were specified and this one wasn't named, skip it
        if requested_names and not explicitly_requested:
            skipped.append((p, "not_requested"))
            continue

        # Disabled: skip unless explicitly named
        if p.disabled and not explicitly_requested:
            skipped.append((p, "DISABLED"))
            continue

        # Feature filter (bypass if explicitly named)
        if required_features and not explicitly_requested:
            if not prob_matches_features(p, required_features):
                skipped.append((p, "feature_mismatch"))
                continue

        # Time limit (bypass if explicitly named)
        if max_time_minutes is not None and not explicitly_requested:
            if p.estimated_time_minutes > max_time_minutes:
                skipped.append((
                    p,
                    f"exceeds_time_limit_{p.estimated_time_minutes}min",
                ))
                continue

        to_run.append(p)

    return to_run, skipped


def make_skipped_result(problem: ProblemConfig, reason: str) -> RunResult:
    check = CheckResult(
        sout_code=StatusCode.SKIP,
        serr_code=StatusCode.SKIP,
        exec_code=StatusCode.SKIP,
        exo_code=StatusCode.SKIP,
        norm_code=StatusCode.SKIP,
        cust_code=StatusCode.SKIP,
        skip_reason=reason,
    )
    return RunResult(problem=problem, check=check)
