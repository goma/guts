from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class StatusCode(str, Enum):
    OK = "OK"
    FAILED = "FAILED"
    SKIP = "SKIP"
    NA = "n/a"
    ABORT = "ABORT"


@dataclass(frozen=True)
class ContactInfo:
    name: str
    email: str


@dataclass(frozen=True)
class ProblemRequirements:
    max_prob_var: int
    max_conc: int
    mde: int
    solver_package: str
    use_arpack: str
    enable_omega_h: str


@dataclass(frozen=True)
class ProblemRun:
    use_aprepro: bool
    aprepro_flags: str
    use_chemkin: bool
    chemkin_input: str
    use_mpi: bool
    num_processors: int
    use_decomp: bool
    brk_input: str
    brk_exo_in: str
    fix_exo_basename: str
    goma_input: str
    goma_serr: str
    goma_sout: str
    goma_opts: str


@dataclass(frozen=True)
class ProblemBlessed:
    serr: str
    sout: str
    exo_output: tuple
    blessed_exo_output: tuple
    exo_abs_tol: tuple
    exo_rel_tol: tuple
    exodiff_input_file: tuple


@dataclass(frozen=True)
class ProblemExtra:
    whacked_files: tuple
    extra_tests: bool
    extra_test_scripts: tuple


@dataclass(frozen=True)
class ProblemConfig:
    name: str
    description: str
    contact: ContactInfo
    estimated_time_minutes: int
    disabled: bool
    features: tuple
    requirements: ProblemRequirements
    run: ProblemRun
    blessed: ProblemBlessed
    extra: ProblemExtra
    source_dir: str


@dataclass
class CheckResult:
    sout_code: StatusCode = StatusCode.NA
    serr_code: StatusCode = StatusCode.NA
    exec_code: StatusCode = StatusCode.NA
    exo_code: StatusCode = StatusCode.NA
    norm_code: StatusCode = StatusCode.NA
    cust_code: StatusCode = StatusCode.NA
    elapsed_seconds: float = 0.0
    abort_reason: str = ""
    skip_reason: str = ""
    build_log: str = ""
    exo_log: str = ""
    norm_log: str = ""
    cust_log: str = ""
    data_dir: str = ""

    def passed(self) -> bool:
        bad = {StatusCode.FAILED, StatusCode.ABORT}
        return not any(
            c in bad for c in [
                self.sout_code, self.serr_code, self.exec_code,
                self.exo_code, self.norm_code, self.cust_code,
            ]
        )


@dataclass
class RunResult:
    problem: ProblemConfig
    check: CheckResult


@dataclass
class RunMeta:
    start_time: datetime.datetime
    host: str
    platform: str
    goma_exe: str
    command_line: str
    output_dir: str
    data_dir_name: str
    problems_dir: str
    scripts_dir: str
