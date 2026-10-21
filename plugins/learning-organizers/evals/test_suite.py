#!/usr/bin/env python3
"""Free static checks on the eval suite's own files (no model calls): every case
has a case.yaml tagged from {routing, negative, edit, kit}; every case carries
the same seed-typst-cache.sh, byte for byte; no prompt names an absolute path
or ~/ (cases run in a sandbox cwd); every replay_breaks.json key names a
not_contains regex grader. The CLI's own strict schema check is the load of a
real run (README). Run: PYTHONDONTWRITEBYTECODE=1 python3 evals/test_suite.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAGS = {"routing", "negative", "edit", "kit"}
failures: list[str] = []


def expect(ok: bool, what: str) -> None:
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


cases = sorted(p.parent for p in HERE.glob("*/case.yaml"))
expect(len(cases) >= 8, f"at least 8 cases ({len(cases)})")
seed = (HERE / "01-t-chart" / "seed-typst-cache.sh").read_bytes()
not_contains: set[str] = set()
for c in cases:
    text = (c / "case.yaml").read_text(encoding="utf-8")
    m = re.search(r"^tags:[ \t]*\[([^\]]*)\]", text, re.M)
    tags = {t.strip() for t in m.group(1).split(",")} if m else set()
    expect(bool(tags) and tags <= TAGS, f"{c.name}: tags {sorted(tags)} drawn from {sorted(TAGS)}")
    expect((c / "seed-typst-cache.sh").read_bytes() == seed, f"{c.name}: seed-typst-cache.sh identical to 01-t-chart's")
    expect("scaffold_script: seed-typst-cache.sh" in text, f"{c.name}: runs the seed scaffold")
    prompt = text.split("prompt: |", 1)[1].split("\n  max_turns:", 1)[0] if "prompt: |" in text else ""
    expect(prompt.strip() != "" and not re.search(r"(?<![\w.])(?:/Users/|/Volumes/|/private/|/tmp/|~/)", prompt),
           f"{c.name}: prompt present and names no absolute path")
    for block in re.split(r"\n  - type: ", text.split("\ngraders:\n", 1)[1]):
        if block.startswith("regex") and re.search(r"^\s+match:\s*not_contains", block, re.M):
            not_contains.add(re.search(r"^\s+name:\s*(\S+)", block, re.M).group(1))
breaks = json.loads((HERE / "replay_breaks.json").read_text(encoding="utf-8"))
expect(set(breaks) == not_contains, f"replay_breaks.json covers exactly the not_contains regex graders {sorted(not_contains)}")

print(f"\n{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
