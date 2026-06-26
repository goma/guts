from __future__ import annotations
import configparser
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class GUTSConfig:
    goma_exe: str
    mpirun: str
    dp_utils_bin: str
    exodiff: str
    decomp: str
    epu: str
    goma_machinefile: str
    chemkin_home: str
    lqinterp: str
    exo_abs_tol: float
    exo_rel_tol: float
    user_email: str
    ld_library_path: str
    default_exodiff_inp: str
    scripts_dir: str

    def subprocess_env(self) -> dict:
        env = dict(os.environ)
        if self.ld_library_path:
            env["LD_LIBRARY_PATH"] = self.ld_library_path
        return env


def load_config(
    ini_path: Optional[str],
    goma_override: Optional[str],
    exodiff_bin_override: Optional[str],
    email_override: Optional[str],
    scripts_dir: str,
) -> GUTSConfig:
    cp = configparser.ConfigParser()

    resolved_ini = ini_path or str(Path(scripts_dir) / "local_config.ini")
    if Path(resolved_ini).is_file():
        cp.read(resolved_ini)

    def get(section: str, key: str, envvar: str = "", default: str = "") -> str:
        try:
            val = cp.get(section, key).strip()
            if val:
                return val
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass
        if envvar:
            ev = os.environ.get(envvar, "").strip()
            if ev:
                return ev
        return default

    goma_exe = goma_override or get("paths", "goma", "GOMA_VERSION")
    dp_utils_bin = exodiff_bin_override or get("paths", "dp_utils_bin", "DP_UTILS_BIN")
    mpitop = get("paths", "mpitop", "MPITOP")
    mpirun_raw = get("paths", "mpirun", "MPIRUN")
    if mpirun_raw:
        mpirun = mpirun_raw
    elif mpitop:
        mpirun = os.path.join(mpitop, "bin", "mpirun")
    else:
        mpirun = shutil.which("mpirun") or "mpirun"

    goma_machinefile = get("paths", "goma_machinefile", "GOMA_MACHINEFILE")

    chemkin_home = get("chemkin", "chemkin_home", "CHEMKIN_HOME", "/home/goma/chemkin_dev")
    lqinterp_raw = get("chemkin", "lqinterp", "LQINTERP")
    lqinterp = lqinterp_raw or os.path.join(chemkin_home, "bin", "lqinterp")

    exo_abs_tol = float(get("tolerances", "exo_abs_tol", "EXO_ABS_TOL", "1e-11"))
    exo_rel_tol = float(get("tolerances", "exo_rel_tol", "EXO_REL_TOL", "1e-6"))

    ld_prepend = get("environment", "ld_library_path_prepend")
    current_ld = os.environ.get("LD_LIBRARY_PATH", "")
    if ld_prepend and current_ld:
        ld_library_path = ld_prepend + ":" + current_ld
    elif ld_prepend:
        ld_library_path = ld_prepend
    else:
        ld_library_path = current_ld

    user_email = email_override or get("email", "user_email", "USER_EMAIL", "none")

    if dp_utils_bin:
        exodiff = os.path.join(dp_utils_bin, "exodiff")
        decomp = os.path.join(dp_utils_bin, "decomp")
        epu = os.path.join(dp_utils_bin, "epu")
    else:
        exodiff = shutil.which("exodiff") or "exodiff"
        decomp = shutil.which("decomp") or "decomp"
        epu = shutil.which("epu") or "epu"

    default_exodiff_inp = str(Path(scripts_dir) / "default_exodiff.inp")

    return GUTSConfig(
        goma_exe=goma_exe,
        mpirun=mpirun,
        dp_utils_bin=dp_utils_bin,
        exodiff=exodiff,
        decomp=decomp,
        epu=epu,
        goma_machinefile=goma_machinefile,
        chemkin_home=chemkin_home,
        lqinterp=lqinterp,
        exo_abs_tol=exo_abs_tol,
        exo_rel_tol=exo_rel_tol,
        user_email=user_email,
        ld_library_path=ld_library_path,
        default_exodiff_inp=default_exodiff_inp,
        scripts_dir=scripts_dir,
    )
