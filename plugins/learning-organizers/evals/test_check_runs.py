#!/usr/bin/env python3
"""Free self-test for check_runs.py over committed fixtures: a good spec passes
with one `ok` line, a spec that fails `organizer.py check` fails it by name, an
empty folder and a folder of non-organizer YAML are `nothing-checked`, an
explicit `blanks: none` lets the learner copy show unmarked answers but never a
marked one, and the
`--expect-hidden` line passes only for an answer the key marks blank. Stdlib
only, no model calls. Run: PYTHONDONTWRITEBYTECODE=1 python3 evals/test_check_runs.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures" / "check_runs"
CHECK = [sys.executable, str(HERE / "check_runs.py")]

failures: list[str] = []


def run(*args: str) -> tuple[int, str]:
    r = subprocess.run([*CHECK, *args], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def expect(ok: bool, what: str, out: str = "") -> None:
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)
        print("     | " + out.strip().replace("\n", "\n     | "))


code, out = run(str(FIX / "good"))
spec_lines = [line for line in out.splitlines() if line.startswith(("ok   ", "FAIL ")) and ".yaml" in line]
expect(code == 0 and len(spec_lines) == 1 and spec_lines[0].startswith("ok   ") and "bridges.yaml" in spec_lines[0],
       "good fixture: exit 0 with one ok line", out)
expect("2 marked blank" in out and "learner draws 4, none marked" in out,
       "good fixture: the key marks 2 blanks and the learner draws none of them", out)

code, out = run(str(FIX / "bad"))
expect(code == 1 and "FAIL" in out and "missing-key.yaml" in out and "missing `right`" in out,
       "bad fixture: exit 1 naming missing-key.yaml and its problem", out)

code, out = run(str(FIX / "good"), str(FIX / "bad"))
expect(code == 1 and out.count("bridges.yaml") == 1 and "total: 2 spec(s) checked, 1 failed" in out,
       "good + bad: exit 1, both checked, one failed", out)

with tempfile.TemporaryDirectory() as empty:
    code, out = run(empty)
    expect(code == 2 and out.startswith("nothing-checked"), "empty folder: exit 2 nothing-checked", out)

code, out = run(str(FIX / "no-specs"))
expect(code == 2 and out.startswith("nothing-checked"), "non-organizer YAML only: exit 2 nothing-checked", out)

code, out = run(str(FIX / "good"), str(FIX / "no-specs"))
expect(code == 0 and "total: 1 spec(s) checked, 0 failed" in out, "good + non-organizer YAML: exit 0, one spec", out)

code, out = run(str(FIX / "blanks-none"))
expect(code == 0 and "blanks: none, so the learner copy shows every answer" in out,
       "blanks: none with no marks: exit 0, the learner copy shows every answer by request", out)

code, out = run(str(FIX / "blanks-none-marked"))
expect(code == 1 and "learner draws marked blank(s) ['Landlord repairs']" in out,
       "blanks: none does not excuse a marked blank the learner copy draws: exit 1", out)

code, out = run(str(FIX / "good"), "--expect-hidden", "lane closures")
expect(code == 0 and "ok   learner hides what the prompt named: 'lane closures'" in out,
       "--expect-hidden on a marked answer: exit 0", out)

code, out = run(str(FIX / "good"), "--expect-hidden", "built in place")
expect(code == 1 and "FAIL learner hides what the prompt named: 'built in place'" in out,
       "--expect-hidden on an unmarked answer: exit 1", out)

print(f"\n{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
