#!/usr/bin/env python3
"""Self-test: every example validates and renders in both versions; the
learner version of a spec with answers differs from its key; every bad spec
is refused with the expected problem; an edited spec gets a new inline
revision; and, when cc-intelligent-ui is installed, its renderer draws an
inline block. Stdlib only. Run: python3 tests/selftest.py
"""
from __future__ import annotations

import glob
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = [sys.executable, str(ROOT / "scripts" / "organizer.py")]
# Specs whose example carries no answers: key and learner draw the same.
NO_ANSWERS = {"assessment-checklist", "rubric", "self-questioning"}

failures: list[str] = []


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([*CLI, *args], capture_output=True, text=True)


sys.path.insert(0, str(ROOT / "scripts"))
import organizer  # noqa: E402  (its typst runner and package path)


def drawn(spec: Path, version: str) -> list[dict]:
    """The answers a version actually draws, from <organizer-answer> metadata."""
    r = organizer.typst(["eval", "query(<organizer-answer>).map(it => it.value)", "--in", str(organizer.PAGE),
                         "--format", "json"], spec, {"format": "png", "version": version})
    if r.returncode != 0:
        failures.append(f"query answers of {spec.name}: {r.stderr.strip()[:200]}")
        return []
    return json.loads(r.stdout)


def expect(ok: bool, what: str) -> None:
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp)
    examples = sorted((ROOT / "examples").glob("*.yaml"))
    expect(len(examples) == 13, f"13 examples found ({len(examples)})")
    for ex in examples:
        r = run("check", str(ex))
        expect(r.returncode == 0, f"check {ex.name}")
        r = run("render", str(ex), "--format", "pdf,png", "--ppi", "40", "--out-dir", str(out))
        files = r.stdout.split()
        expect(r.returncode == 0 and len(files) == 4 and all(Path(f).stat().st_size > 0 for f in files),
               f"render {ex.name} → 4 files")
        key, learner = drawn(ex, "key"), drawn(ex, "learner")
        leaked = [a["text"] for a in learner if a["blank"]]
        expect(not leaked, f"learner {ex.name} draws no marked blank {leaked[:3]}")
        if not any(a["blank"] for a in key):
            # no marked items: every answer field is blanked for the learner
            expect(not learner, f"learner {ex.name} draws no answers {[a['text'] for a in learner][:3]}")
        if ex.stem not in NO_ANSWERS:
            expect(len(key) > len(learner), f"key {ex.name} shows answers the learner version hides ({len(key)} > {len(learner)})")

    for bad in sorted((ROOT / "tests" / "bad").glob("*.yaml")):
        want = bad.read_text(encoding="utf-8").splitlines()[0].removeprefix("# expect:").strip()
        r = run("check", str(bad))
        expect(r.returncode == 1 and want in r.stdout, f"refuse {bad.name}: {want!r}")
        r = run("render", str(bad), "--out-dir", str(out))
        expect(r.returncode == 1, f"render refuses {bad.name}")

    spec = out / "t.yaml"
    shutil.copyfile(ROOT / "examples" / "t-chart.yaml", spec)
    a = run("inline", str(spec)).stdout
    spec.write_text(spec.read_text(encoding="utf-8").replace("rows: 6", "rows: 7"), encoding="utf-8")
    b = run("inline", str(spec)).stdout
    expect(a.startswith("```typst") and a != b, "an edited spec gets a new inline revision")

    iui = sorted(glob.glob(str(Path.home() / ".claude/plugins/cache/*/cc-intelligent-ui/*/render")))
    if iui and shutil.which("typst"):
        render = Path(iui[-1])
        doc = out / "doc.json"
        doc.write_text(json.dumps({"base": tmp, "segments": ["Intro\n\n" + b]}), encoding="utf-8")
        for theme in ("dark", "light"):
            r = subprocess.run(["typst", "compile", "--root", "/", "--package-path", str(render / "packages"),
                                "--format", "png", "--input", f"theme={theme}",
                                "--input", f"theme-dir={render / 'themes' / 'claude-code'}",
                                "--input", f"doc={doc}", "--input", "width=600",
                                str(render / "md.typ"), str(out / f"iui-{theme}-{{0p}}.png")],
                               capture_output=True, text=True)
            # md.typ shows a failed live block as code in safe mode only; a
            # normal compile that errors means the block would not draw.
            expect(r.returncode == 0, f"cc-intelligent-ui draws the inline block ({theme})")
    else:
        print("skip cc-intelligent-ui is not installed")

print(f"\n{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
