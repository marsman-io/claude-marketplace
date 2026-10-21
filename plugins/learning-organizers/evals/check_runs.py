#!/usr/bin/env python3
"""Post-run checker for the eval suite: every organizer spec a run wrote must
pass `organizer.py check`, and its learner version must draw no answer the key
marks as a blank (none at all when the key marks none).

  check_runs.py <folder>... [--expect-hidden TEXT]...

A folder is anything a run left behind: a `--keep-temp` sandbox, a results
dir, a fixture. A spec is a .yaml/.yml/.json file whose top-level `type` is
one `organizer.py types` lists. `--expect-hidden TEXT` adds one line: some
checked spec's key draws an answer containing TEXT marked `blank: true`, and
no such spec's learner version draws it (the learner-version edit case).

Prints one line per spec and a total. Exit 0: at least one spec was checked
and nothing failed; 1: a spec or an expectation failed; 2: nothing to check.
Stdlib only, plus the plugin's own scripts/organizer.py (imported the way
tests/selftest.py does). Run with PYTHONDONTWRITEBYTECODE=1.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = [sys.executable, str(ROOT / "scripts" / "organizer.py")]
sys.path.insert(0, str(ROOT / "scripts"))
import organizer  # noqa: E402  (its typst runner and package path)

TYPES = {f.stem for f in organizer.EXAMPLES.glob("*.yaml")}  # what `organizer.py types` lists
TOP_TYPE = re.compile(r"""^type:[ \t]*["']?([A-Za-z0-9-]+)["']?[ \t]*(?:#.*)?$""", re.M)
TOP_BLANKS = re.compile(r"""^blanks:[ \t]*["']?(all|marked|none)["']?[ \t]*(?:#.*)?$""", re.M)
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
MAX_BYTES = 1_000_000


def spec_type(path: Path) -> str | None:
    """The organizer type of a candidate file, or None when it is not a spec."""
    try:
        if path.stat().st_size > MAX_BYTES:
            return None
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(text)
        except ValueError:
            return None
        t = data.get("type") if isinstance(data, dict) else None
    else:
        m = TOP_TYPE.search(text)
        t = m.group(1) if m else None
    return t if t in TYPES else None


def find_specs(folders: list[Path]) -> list[tuple[Path, str]]:
    seen: set[Path] = set()
    found: list[tuple[Path, str]] = []
    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder):  # does not follow links
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for name in sorted(filenames):
                p = Path(dirpath) / name
                if p.suffix.lower() not in (".yaml", ".yml", ".json") or p.is_symlink():
                    continue
                real = p.resolve()
                t = spec_type(p) if real not in seen else None
                if t:
                    seen.add(real)
                    found.append((p, t))
    return found


def drawn(spec: Path, version: str) -> tuple[list[dict] | None, str]:
    """The answers a version draws, from <organizer-answer> metadata (the self-test's query)."""
    r = organizer.typst(["eval", "query(<organizer-answer>).map(it => it.value)", "--in", str(organizer.PAGE),
                         "--format", "json"], spec.resolve(), {"format": "png", "version": version})
    if r.returncode != 0:
        err = r.stderr.strip()
        return None, err.splitlines()[0][:200] if err else f"typst exit {r.returncode}"
    return json.loads(r.stdout or "[]"), ""


def blanks_setting(spec: Path) -> str | None:
    """The spec's top-level `blanks:` (all | marked | none), when it sets one."""
    text = spec.read_text(encoding="utf-8")
    if spec.suffix.lower() == ".json":
        b = json.loads(text).get("blanks")
        return b if b in ("all", "marked", "none") else None
    m = TOP_BLANKS.search(text)
    return m.group(1) if m else None


def check_spec(spec: Path) -> tuple[list[str], list[dict], list[dict]]:
    """Problems with one spec, and the answers its key and learner versions draw."""
    r = subprocess.run([*CLI, "check", str(spec)], capture_output=True, text=True)
    if r.returncode != 0:
        detail = "; ".join(line.strip(" -") for line in r.stdout.splitlines()[1:4]) or r.stderr.strip()[-200:]
        return [f"organizer.py check exit {r.returncode}: {detail}"], [], []
    key, err = drawn(spec, "key")
    if key is None:
        return [f"key query failed: {err}"], [], []
    learner, err = drawn(spec, "learner")
    if learner is None:
        return [f"learner query failed: {err}"], key, []
    problems = []
    leaked = [a["text"] for a in learner if a.get("blank")]
    if leaked:
        problems.append(f"learner draws marked blank(s) {leaked[:3]}")
    # With no marks every answer field is blank for the learner, unless the spec
    # says `blanks: none` (references/spec.md): then the learner copy shows them.
    if not any(a.get("blank") for a in key) and learner and blanks_setting(spec) != "none":
        problems.append(f"key marks no blank, yet learner draws {[a['text'] for a in learner][:3]}")
    return problems, key, learner


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("folders", nargs="+", type=Path)
    ap.add_argument("--expect-hidden", action="append", default=[], metavar="TEXT")
    a = ap.parse_args(argv)
    missing = [str(f) for f in a.folders if not f.is_dir()]
    if missing:
        print(f"check_runs: not a folder: {', '.join(missing)}", file=sys.stderr)
        return 2

    specs = find_specs(a.folders)
    failed = 0
    answers: list[tuple[Path, list[dict], list[dict]]] = []
    for spec, t in specs:
        problems, key, learner = check_spec(spec)
        answers.append((spec, key, learner))
        if problems:
            failed += 1
            print(f"FAIL {spec} ({t}): {'; '.join(problems)}")
        else:
            marked = sum(1 for k in key if k.get("blank"))
            note = "; blanks: none, so the learner copy shows every answer" if blanks_setting(spec) == "none" else ""
            print(f"ok   {spec} ({t}): check exit 0; key draws {len(key)} answer(s), {marked} marked blank; "
                  f"learner draws {len(learner)}, none marked{note}")

    expectations_failed = 0
    for text in a.expect_hidden:
        want = text.casefold()
        holders = [(s, l) for s, k, l in answers if any(want in x["text"].casefold() and x.get("blank") for x in k)]
        shown = [s for s, l in holders if any(want in x["text"].casefold() for x in l)]
        if holders and not shown:
            print(f"ok   learner hides what the prompt named: {text!r} is marked blank in {len(holders)} spec(s) "
                  f"and not drawn in their learner version")
        else:
            expectations_failed += 1
            why = f"is drawn in the learner version of {shown[0]}" if shown else "is marked blank: true in no checked spec"
            print(f"FAIL learner hides what the prompt named: {text!r} {why}")

    if not specs:
        print(f"nothing-checked: no organizer spec under {', '.join(str(f) for f in a.folders)}")
        return 2
    print(f"total: {len(specs)} spec(s) checked, {failed} failed; "
          f"{len(a.expect_hidden)} expectation(s), {expectations_failed} failed")
    return 1 if failed or expectations_failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
