#!/usr/bin/env python3
"""Check that passed == total for every section in a GUTS JSON report summary."""
import json
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <report.json>", file=sys.stderr)
        return 2

    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        return 2

    summary = doc.get("summary", {})
    all_passed = True

    for section, value in summary.items():
        if not isinstance(value, dict):
            continue
        passed = value.get("passed")
        total = value.get("total")
        if passed is None or total is None:
            continue
        status = "OK" if passed == total else "FAIL"
        if passed != total:
            all_passed = False
        print(f"  {section}: {passed}/{total} [{status}]")

    if all_passed:
        print("All sections passed.")
        return 0
    else:
        print("One or more sections have failures.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
