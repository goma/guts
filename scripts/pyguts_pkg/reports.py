from __future__ import annotations
import json
import os
from pathlib import Path
from typing import List, Tuple

from .models import CheckResult, ProblemConfig, RunMeta, RunResult, StatusCode

_HR = "-" * 89

_HTML_CSS = """
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f9fafb;
    color: #111827;
    margin: 0;
    padding: 24px;
}
h2 {
    color: #1f2937;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 8px;
    margin-top: 32px;
}
table {
    border-collapse: collapse;
    width: 100%;
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 24px;
    font-size: 0.9em;
}
th {
    background: #374151;
    color: white;
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
    white-space: nowrap;
}
td {
    padding: 8px 12px;
    border-bottom: 1px solid #e5e7eb;
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: #f3f4f6; }
.ok   { color: #16a34a; font-weight: bold; }
.fail { color: #dc2626; font-weight: bold; }
.na   { color: #6b7280; }
.skip { color: #d97706; }
.abort { color: #7c3aed; font-weight: bold; }
a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }
.config-table th { background: #f3f4f6; color: #374151; width: 200px; }
.info-links a { margin-right: 6px; font-size: 0.8em; }
</style>
"""


def _status_class(code: StatusCode) -> str:
    if code == StatusCode.OK:
        return "ok"
    if code == StatusCode.FAILED:
        return "fail"
    if code == StatusCode.SKIP:
        return "skip"
    if code == StatusCode.ABORT:
        return "abort"
    return "na"


def _lpad(s: str, width: int = 40) -> str:
    return s.ljust(width)[:width]


def _tpad(s: str, width: int = 8) -> str:
    return s.ljust(width)[:width]


def _rel_data(meta: RunMeta, prob_name: str, filename: str) -> str:
    return f"../data/{meta.data_dir_name}/{prob_name}/{filename}"


def _rel_source(meta: RunMeta, prob_name: str, filename: str) -> str:
    results_dir = Path(meta.output_dir) / "results"
    prob_source = Path(meta.problems_dir) / prob_name / filename
    try:
        return os.path.relpath(prob_source, results_dir)
    except ValueError:
        return str(prob_source)


def write_text_report(
    results: List[RunResult],
    skipped: List[Tuple[ProblemConfig, str]],
    path: Path,
    meta: RunMeta,
) -> None:
    aborted = [r for r in results if r.check.abort_reason]
    run_results = [r for r in results if not r.check.abort_reason]

    lines: List[str] = []
    lines.append(_HR)
    lines.append("")
    lines.append("        GUTS Configuration Summary")
    lines.append("")
    lines.append(f"Time Started        = {meta.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Host Machine / Type = {meta.host} / {meta.platform}")
    lines.append(f"GOMA Executable     = {meta.goma_exe}")
    lines.append(f"GUTS Command Line   = {meta.command_line}")
    lines.append(f"GUTS Data Directory = {meta.output_dir}/data/{meta.data_dir_name}")
    lines.append(f"Results Directory   = {meta.output_dir}/results/")
    lines.append("")
    lines.append(_HR)
    lines.append("")
    lines.append("SUMMARY OF TESTED PROBLEMS")
    lines.append("")

    hdr = (
        _lpad("Test Problem") + " "
        + _tpad("SOUT") + " "
        + _tpad("SERR") + " "
        + _tpad("Exec.") + " "
        + _tpad("ExoII") + " "
        + _tpad("Norms") + " "
        + _tpad("Custom") + " "
        + _tpad("Time")
    )
    lines.append(hdr)
    lines.append(_HR)

    for r in sorted(run_results, key=lambda x: x.problem.name):
        c = r.check
        elapsed_min = f"{c.elapsed_seconds / 60:.1f}m"
        row = (
            _lpad(r.problem.name) + " "
            + _tpad(c.sout_code.value) + " "
            + _tpad(c.serr_code.value) + " "
            + _tpad(c.exec_code.value) + " "
            + _tpad(c.exo_code.value) + " "
            + _tpad(c.norm_code.value) + " "
            + _tpad(c.cust_code.value) + " "
            + _tpad(elapsed_min)
        )
        lines.append(row)

    lines.append(_HR)

    # Aborted
    lines.append("")
    lines.append(_HR)
    if not aborted:
        lines.append("NO PROBLEMS WERE ABORTED")
    else:
        lines.append("THE FOLLOWING PROBLEMS WERE ABORTED")
        lines.append("")
        lines.append(_lpad("Test Problem") + " Reason aborted")
        lines.append(_HR)
        for r in aborted:
            reason = r.check.abort_reason.replace("_", " ")
            lines.append(_lpad(r.problem.name) + " " + reason)
    lines.append(_HR)

    # Skipped
    lines.append("")
    lines.append(_HR)
    shown = [(p, r) for p, r in skipped if r != "not_requested"]
    if not shown:
        lines.append("NO PROBLEMS WERE SKIPPED")
    else:
        lines.append("THE FOLLOWING PROBLEMS WERE SKIPPED")
        lines.append("")
        lines.append(_lpad("Test Problem") + " Reason skipped")
        lines.append(_HR)
        for p, reason in shown:
            display = "This problem is disabled" if reason == "DISABLED" else reason.replace("_", " ")
            lines.append(_lpad(p.name) + " " + display)
    lines.append(_HR)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def write_html_report(
    results: List[RunResult],
    skipped: List[Tuple[ProblemConfig, str]],
    path: Path,
    meta: RunMeta,
) -> None:
    aborted = [r for r in results if r.check.abort_reason]
    run_results = [r for r in results if not r.check.abort_reason]

    def cell(code: StatusCode, href: str, label: str = "") -> str:
        cls = _status_class(code)
        display = label or code.value
        return f'<td><a href="{href}" class="{cls}">{display}</a></td>'

    lines: List[str] = []
    lines.append("<!DOCTYPE html>")
    lines.append("<html lang='en'>")
    lines.append("<head>")
    lines.append("<meta charset='UTF-8'>")
    lines.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
    lines.append("<title>GUTS Results Summary</title>")
    lines.append(_HTML_CSS)
    lines.append("</head>")
    lines.append("<body>")

    lines.append("<h2>GUTS Configuration Summary</h2>")
    lines.append("<table class='config-table'>")
    rows = [
        ("Time Started", meta.start_time.strftime("%Y-%m-%d %H:%M:%S")),
        ("Host / Platform", f"{meta.host} / {meta.platform}"),
        ("GOMA Executable", meta.goma_exe),
        ("Command Line", f"<tt>{meta.command_line}</tt>"),
        ("Data Directory", f"<tt>{meta.output_dir}/data/{meta.data_dir_name}</tt>"),
        ("Results Directory", f"<tt>{meta.output_dir}/results/</tt>"),
    ]
    for label, val in rows:
        lines.append(f"<tr><th>{label}</th><td>{val}</td></tr>")
    lines.append("</table>")

    lines.append("<h2>Summary of Tested Problems</h2>")
    lines.append("<table>")
    lines.append(
        "<tr>"
        "<th>Test Problem</th>"
        "<th>Std Out</th>"
        "<th>Std Err</th>"
        "<th>Exec Status</th>"
        "<th>ExoII</th>"
        "<th>Norms</th>"
        "<th>Custom</th>"
        "<th>Time</th>"
        "<th>Info</th>"
        "</tr>"
    )

    for r in sorted(run_results, key=lambda x: x.problem.name):
        c = r.check
        p = r.problem
        elapsed_min = f"{c.elapsed_seconds / 60:.1f}m"

        def _dc(filename: str) -> str:
            return _rel_data(meta, p.name, filename)

        def _sc(filename: str) -> str:
            return _rel_source(meta, p.name, filename)

        prob_link = f'<a href="{_sc("")}">{p.name}</a>'

        info = (
            f'<span class="info-links">'
            f'<a href="{_sc("problem.json")}">json</a>'
            f'<a href="{_sc(p.run.goma_input)}">input</a>'
            f'<a href="{_sc("vp_title")}">about</a>'
            f'</span>'
        )

        lines.append("<tr>")
        lines.append(f"<td>{prob_link}</td>")
        lines.append(cell(c.sout_code, _dc(p.run.goma_sout)))
        lines.append(cell(c.serr_code, _dc(p.run.goma_serr)))
        lines.append(cell(c.exec_code, _dc("exec_status.txt")))
        lines.append(cell(c.exo_code, _dc("exoComparison.txt")))
        lines.append(cell(c.norm_code, _dc("normComparison.txt")))
        lines.append(cell(c.cust_code, _dc("custTests.txt")))
        lines.append(f'<td class="na">{elapsed_min}</td>')
        lines.append(f"<td>{info}</td>")
        lines.append("</tr>")

    lines.append("</table>")

    # Aborted
    if not aborted:
        lines.append("<h2>No Problems Were Aborted</h2>")
    else:
        lines.append("<h2>The Following Problems Were Aborted</h2>")
        lines.append("<table>")
        lines.append(
            "<tr><th>Test Problem</th><th>Reason Aborted</th><th>Build Log</th></tr>"
        )
        for r in aborted:
            p = r.problem
            reason = r.check.abort_reason.replace("_", " ")
            abort_href = _rel_data(meta, p.name, "abort.txt")
            build_href = _rel_data(meta, p.name, "build.txt")
            lines.append(
                f"<tr>"
                f"<td>{p.name}</td>"
                f'<td><a href="{abort_href}">{reason}</a></td>'
                f'<td><a href="{build_href}">build.txt</a></td>'
                f"</tr>"
            )
        lines.append("</table>")

    # Skipped
    shown = [(p, r) for p, r in skipped if r != "not_requested"]
    if not shown:
        lines.append("<h2>No Problems Were Skipped &mdash; YOU ROCK!</h2>")
    else:
        lines.append("<h2>The Following Problems Were Skipped</h2>")
        lines.append("<table>")
        lines.append("<tr><th>Test Problem</th><th>Reason</th></tr>")
        for p, reason in shown:
            display = "This problem is disabled" if reason == "DISABLED" else reason.replace("_", " ")
            lines.append(f"<tr><td>{p.name}</td><td>{display}</td></tr>")
        lines.append("</table>")

    import datetime
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"<p><small>GUTS finished at <b>{end_time}</b></small></p>")
    lines.append("</body>")
    lines.append("</html>")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def write_json_report(
    results: List[RunResult],
    skipped: List[Tuple[ProblemConfig, str]],
    path: Path,
    meta: RunMeta,
) -> None:
    run_results = [r for r in results if not r.check.abort_reason]
    aborted = [r for r in results if r.check.abort_reason]
    shown_skipped = [(p, r) for p, r in skipped if r != "not_requested"]

    check_fields = [
        ("sout", lambda c: c.sout_code),
        ("serr", lambda c: c.serr_code),
        ("exec", lambda c: c.exec_code),
        ("exo",  lambda c: c.exo_code),
        ("norms", lambda c: c.norm_code),
        ("custom", lambda c: c.cust_code),
    ]

    summary: dict = {}
    for key, getter in check_fields:
        eligible = [r for r in run_results if getter(r.check) != StatusCode.NA]
        passed = sum(1 for r in eligible if getter(r.check) == StatusCode.OK)
        summary[key] = {"passed": passed, "total": len(eligible)}
    summary["aborted"] = len(aborted)
    summary["skipped"] = len(shown_skipped)

    individual = []
    for r in sorted(run_results, key=lambda x: x.problem.name):
        c = r.check
        individual.append({
            "name": r.problem.name,
            "parallel": r.problem.run.use_mpi,
            "elapsed_seconds": round(c.elapsed_seconds, 1),
            "sout": c.sout_code.value,
            "serr": c.serr_code.value,
            "exec": c.exec_code.value,
            "exo": c.exo_code.value,
            "norms": c.norm_code.value,
            "custom": c.cust_code.value,
            "passed": c.passed(),
        })
    for r in sorted(aborted, key=lambda x: x.problem.name):
        c = r.check
        individual.append({
            "name": r.problem.name,
            "parallel": r.problem.run.use_mpi,
            "elapsed_seconds": round(c.elapsed_seconds, 1),
            "sout": c.sout_code.value,
            "serr": c.serr_code.value,
            "exec": c.exec_code.value,
            "exo": c.exo_code.value,
            "norms": c.norm_code.value,
            "custom": c.cust_code.value,
            "passed": False,
            "abort_reason": c.abort_reason,
        })

    skipped_list = [
        {
            "name": p.name,
            "reason": "Problem is disabled" if r == "DISABLED" else r.replace("_", " "),
        }
        for p, r in shown_skipped
    ]

    doc = {
        "meta": {
            "start_time": meta.start_time.isoformat(),
            "host": meta.host,
            "platform": meta.platform,
            "goma_exe": meta.goma_exe,
            "command_line": meta.command_line,
            "output_dir": meta.output_dir,
            "data_dir_name": meta.data_dir_name,
        },
        "summary": summary,
        "results": individual,
        "skipped": skipped_list,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
