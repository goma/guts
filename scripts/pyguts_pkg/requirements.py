from __future__ import annotations
import re
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class GomaCapabilities:
    mde: Optional[int]
    max_prob_var: Optional[int]
    max_conc: Optional[int]
    is_parallel: bool
    enable_front: str
    enable_aztec: str
    enable_sparse: str
    enable_umfpack: str
    enable_arpack: str
    enable_omega_h: str
    enable_petsc: str
    petsc_use_complex: str
    version_output_present: bool  # False → old build, skip checks


_CAPS_CACHE: dict = {}


def get_goma_capabilities(goma_exe: str, env: dict) -> GomaCapabilities:
    if goma_exe in _CAPS_CACHE:
        return _CAPS_CACHE[goma_exe]
    caps = _parse_goma_version(goma_exe, env)
    _CAPS_CACHE[goma_exe] = caps
    return caps


def _parse_goma_version(goma_exe: str, env: dict) -> GomaCapabilities:
    try:
        result = subprocess.run(
            [goma_exe, "-v"],
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
        output = result.stdout + result.stderr
    except Exception:
        output = ""

    if "MAX_PROB_VAR" not in output:
        return GomaCapabilities(
            mde=None, max_prob_var=None, max_conc=None,
            is_parallel=False,
            enable_front="", enable_aztec="", enable_sparse="",
            enable_umfpack="", enable_arpack="", enable_omega_h="",
            enable_petsc="", petsc_use_complex="",
            version_output_present=False,
        )

    def _extract(key: str) -> str:
        m = re.search(rf"{re.escape(key)}\s*=\s*(\S+)", output)
        return m.group(1).strip() if m else ""

    def _extract_int(key: str) -> Optional[int]:
        val = _extract(key)
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    return GomaCapabilities(
        mde=_extract_int("MDE"),
        max_prob_var=_extract_int("MAX_PROB_VAR"),
        max_conc=_extract_int("MAX_CONC"),
        is_parallel="PARALLEL" in output,
        enable_front=_extract("ENABLE_FRONT"),
        enable_aztec=_extract("ENABLE_AZTEC"),
        enable_sparse=_extract("ENABLE_SPARSE"),
        enable_umfpack=_extract("ENABLE_UMFPACK"),
        enable_arpack=_extract("ENABLE_ARPACK"),
        enable_omega_h=_extract("ENABLE_OMEGA_H"),
        enable_petsc=_extract("ENABLE_PETSC"),
        petsc_use_complex=_extract("PETSC_USE_COMPLEX"),
        version_output_present=True,
    )


def check_requirements(
    caps: GomaCapabilities,
    reqs,  # ProblemRequirements
    num_processors: int,
) -> Tuple[bool, List[str]]:
    """Returns (ok, list_of_failure_reasons)."""
    if not caps.version_output_present:
        return True, []

    failures: List[str] = []

    if caps.mde is not None and caps.mde < reqs.mde:
        failures.append(f"MDE too small: {caps.mde} < {reqs.mde}")
    if caps.max_prob_var is not None and caps.max_prob_var < reqs.max_prob_var:
        failures.append(
            f"MAX_PROB_VAR too small: {caps.max_prob_var} < {reqs.max_prob_var}"
        )
    if caps.max_conc is not None and caps.max_conc < reqs.max_conc:
        failures.append(f"MAX_CONC too small: {caps.max_conc} < {reqs.max_conc}")

    if num_processors > 1 and not caps.is_parallel:
        failures.append(
            f"GOMA not built for PARALLEL (num_processors={num_processors})"
        )

    pkg = reqs.solver_package.lower()
    if pkg == "front":
        if caps.enable_front == "no":
            failures.append("GOMA not built with solver: FRONT")
    elif pkg == "aztec":
        if caps.enable_aztec == "no":
            failures.append("GOMA not built with solver: AZTEC")
    elif pkg == "lu":
        if caps.enable_sparse == "no":
            failures.append("GOMA not built with solver: SPARSE (lu)")
    elif pkg == "umfpack":
        if caps.enable_umfpack == "no":
            failures.append("GOMA not built with solver: UMFPACK")
    elif pkg == "petsc":
        if caps.enable_petsc == "no":
            failures.append("GOMA not built with solver: PETSc")
        if caps.petsc_use_complex == "yes":
            failures.append("GOMA built with PETSc complex (need real)")
    elif pkg == "petsc_complex":
        if caps.enable_petsc == "no":
            failures.append("GOMA not built with solver: PETSc complex")
        if caps.petsc_use_complex != "yes":
            failures.append("GOMA not built with PETSc complex")
    # amesos / amesos2 / other: no specific flag to check

    if reqs.use_arpack.lower() == "yes":
        if caps.enable_arpack == "no":
            failures.append("GOMA not built with ARPACK")

    if reqs.enable_omega_h.lower() == "yes":
        if caps.enable_omega_h == "no":
            failures.append("GOMA not built with OMEGA_H")

    return len(failures) == 0, failures
