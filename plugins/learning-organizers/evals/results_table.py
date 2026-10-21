#!/usr/bin/env python3
"""Print the with-plugin vs no-plugin results table for one or more
`claude plugin eval --ablation with-without` results, with the post-run
checker's verdict on every spec each arm wrote.

  results_table.py <aggregate-result.json>[:<kept-dir>]...

Per case: mean score per arm (the CLI's), delta, the plugin-skill indicator
(runs whose Skill calls named graphic-organizer or lesson-kit, read from the
`tool_used: Skill` graders), the checker (check_runs.py's rules) over each
arm's sandbox cwd, and the case's cost (its runs' agent + judge cost). A run's files are read from the
kept sandbox, or from <kept-dir>/<case>/<arm>-<n>/cwd when given (as
replay_graders.py --kept). Totals are computed here, not by hand.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_runs  # noqa: E402
from replay_graders import Run  # noqa: E402

CALLED = re.compile(r"Skill called (\d+)x")


def skill_calls(rec: dict, case: dict) -> int | None:
    names = {g["name"] for g in case["graders"]
             if g["type"] == "tool_used" and g["config"].get("tool") == "Skill"}
    for g in rec.get("graders", []):
        if g["name"] in names:
            m = CALLED.search(g.get("explanation", ""))
            if m:
                return int(m.group(1))
    return None


def checker(runs: list[Run]) -> str:
    specs = ok = 0
    for r in runs:
        if not r.cwd.is_dir():
            continue
        for spec, _t in check_runs.find_specs([r.cwd]):
            specs += 1
            problems, _k, _l = check_runs.check_spec(spec)
            ok += not problems
    return "nothing-checked" if specs == 0 else f"{ok}/{specs} ok"


def main(argv: list[str]) -> int:
    rows, total_cost, partial = [], 0.0, []
    for arg in argv:
        res_path, _, kept = arg.partition(":")
        result = json.loads(Path(res_path).read_text(encoding="utf-8"))
        total_cost += result.get("costUsd") or 0.0
        if result.get("partial"):
            partial.append(res_path)
        for case in result["cases"]:
            arms = case.get("arms", {})
            agg = case.get("aggregates", {})
            runs = {arm: [Run(case["name"], arm, i, rec, Path(kept) if kept else None)
                          for i, rec in enumerate(recs, 1)] for arm, recs in arms.items()}
            fired = [skill_calls(rec, case) for rec in arms.get("with", [])]
            ind = f"{sum(1 for f in fired if f)}/{len(fired)} runs" if fired and None not in fired else "n/a"
            mean = lambda recs: sum(r["score"] for r in recs) / len(recs) if recs else float("nan")  # noqa: E731
            w, wo = mean(arms.get("with", [])), mean(arms.get("without", []))
            errors = sum(1 for recs in arms.values() for r in recs if r.get("error"))
            rows.append((case["name"], w, wo, agg.get("delta", w - wo), ind,
                         checker(runs.get("with", [])), checker(runs.get("without", [])),
                         sum(r.get("costUsd") or 0.0 for recs in arms.values() for r in recs),
                         len(arms.get("with", [])), errors))
    print("| case | with-plugin score | no-plugin score | delta | Skill indicator (with arm) | checker, with arm | checker, no-plugin arm | cost (USD) |")
    print("|---|---|---|---|---|---|---|---|")
    for name, w, wo, d, ind, cw, cwo, cost, n, errors in rows:
        note = f" ({errors} run error(s))" if errors else ""
        print(f"| {name} | {w:.2f} | {wo:.2f} | {d:+.2f} | {ind} | {cw} | {cwo} | {cost:.4f} |{note}")
    print(f"\n{len(rows)} case(s); cases' run costs (agent + judge) ${sum(r[7] for r in rows):.4f}; "
          f"invocations' reported costUsd ${total_cost:.4f}" + (f"; PARTIAL: {', '.join(partial)}" if partial else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
