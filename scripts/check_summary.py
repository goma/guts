#!/usr/bin/env python3
"""Check a GUTS JSON report summary."""
import argparse
import json
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that passed == total for every section in a GUTS JSON report summary."
    )
    parser.add_argument("report_json", help="Path to the GUTS JSON report.")
    parser.add_argument(
        "-n",
        "--expected-problems",
        type=int,
        metavar="NUM",
        help="Expected number of problems represented by results plus skipped entries.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_problems is not None and args.expected_problems < 0:
        print("Error: --expected-problems must be non-negative.", file=sys.stderr)
        return 2

    path = args.report_json
    try:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        return 2

    summary = doc.get("summary", {})
    all_passed = True

    if args.expected_problems is not None:
        results = doc.get("results", [])
        skipped = doc.get("skipped", [])
        if not isinstance(results, list) or not isinstance(skipped, list):
            print(
                "Error: report must contain list-valued 'results' and 'skipped' fields "
                "to check --expected-problems.",
                file=sys.stderr,
            )
            return 2
        actual_problems = len(results) + len(skipped)
        status = "OK" if actual_problems == args.expected_problems else "FAIL"
        if actual_problems != args.expected_problems:
            all_passed = False
        print(f"  problems: {actual_problems}/{args.expected_problems} [{status}]")

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
