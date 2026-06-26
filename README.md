# GUTS — GOMA Unit Test Suite

GUTS is the regression test harness for the [GOMA](https://gomafem.com) finite element solver. It discovers problem directories, runs each one against a GOMA executable, and checks stdout/stderr and Exodus II output against stored blessed files. Results are written as text, HTML, and JSON reports.

## Repository layout

```
problems/          # One subdirectory per test problem, each with problem.json
scripts/
  guts.py          # Main entry point (run as: python scripts/guts.py ...)
  rebaseline       # Update blessed files from a completed run
  check_summary.py # CI helper: exits non-zero if any section has failures
  pyguts_pkg/      # Python package implementing the harness
  local_config.ini.example  # Configuration template — copy to local_config.ini not usually needed
```

## Prerequisites

- Python 3.8+
- A compiled GOMA executable
- SEACAS/Trilinos tools: `exodiff`, `decomp`, `epu` (for Exodus II diffing and parallel runs)
- `mpirun` (for parallel problems)

## Setup

Run on a command line that is able to run your goma executable with mpi run.

OR:

Copy and edit the configuration file:

```sh
cp scripts/local_config.ini.example scripts/local_config.ini
```

All `[paths]` values can also be supplied as environment variables (`GOMA_VERSION`, `DP_UTILS_BIN`, `MPIRUN`) or via CLI flags, which take precedence over the config file.

## Running the suite

```sh
# Run all problems (1 worker)
python scripts/guts.py -g /path/to/goma

# Run with 8 parallel workers
python scripts/guts.py -j 8

# Run only problems tagged "parallel" and "steady"
python scripts/guts.py -f parallel -f steady

# Run specific problems by name
python scripts/guts.py -p ldc -p beam

# Skip problems that would take more than 5 minutes
python scripts/guts.py -t 5

# Print per-problem progress as results arrive
python scripts/guts.py -v

# Keep all intermediate files (no cleanup after each problem) needed for rebaselining
python scripts/guts.py -k
```

On completion, results are written to `results/` and `data/<platform_host_timestamp>/`:

```
results/results_<timestamp>.txt
results/results_<timestamp>.html
results/latest.txt     -> symlink to most recent text report
results/latest.html    -> symlink to most recent HTML report
```

Exit code is 0 if every problem passed, 1 if any failed or aborted.

### Checking a JSON report in CI

```sh
python scripts/check_summary.py results/results_<timestamp>.json
```

Exits 0 if all sections report `passed == total`, 1 otherwise.

## Rebaselining

After intentional solver changes, update the blessed output for one or more problems:

```sh
# Preview what would be copied
python scripts/rebaseline --dry-run \
    -d data/linux_myhost_20240601_120000 \
    -p ldc -p beam

# Apply the update
python scripts/rebaseline \
    -d data/linux_myhost_20240601_120000 \
    -p ldc -p beam
```

The script copies `sout`, `serr`, and Exodus II output files from the run directory back to the problem's source directory as the new blessed references.

## Problem description format

Each problem directory contains a `problem.json` with the following structure:

```json
{
  "name": "ldc",
  "description": "...",
  "contact": { "name": "...", "email": "..." },
  "estimated_time_minutes": 1,
  "disabled": false,
  "features": ["serial", "steady", "umf", "cartesian", "2d"],
  "requirements": {
    "max_prob_var": 3,
    "max_conc": 1,
    "mde": 12,
    "solver_package": "umfpack",
    "use_arpack": "no"
  },
  "run": {
    "goma_input": "ldc.input",
    "use_mpi": false,
    "num_processors": 1,
    "use_aprepro": true,
    "use_chemkin": false
  },
  "blessed": {
    "sout": "blessed.stdout.txt",
    "serr": "blessed.stderr.txt",
    "exo_output": ["out.exoII"],
    "blessed_exo_output": ["blessed.exoII"],
    "exo_abs_tol": [1e-11],
    "exo_rel_tol": [1e-6],
    "exodiff_input_file": ["exodiff.inp"]
  },
  "extra": {
    "whacked_files": [],
    "extra_tests": false,
    "extra_test_scripts": []
  }
}
```

### Feature tags

Feature tags are used with `-f`/`--feature` to select subsets of the suite. Two special prefixes allow filtering on GOMA input file content:

- `bc_<name>` — matches problems whose input file contains `BC = <name>`
- `eq_<name>` — matches problems whose input file contains `EQ = <name>`

All other recognized tags are listed in `scripts/pyguts_pkg/known_features.py` and cover bulk physics, coordinate systems, algorithms, solvers, and solution methods.
