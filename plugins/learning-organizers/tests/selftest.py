#!/usr/bin/env python3
"""Self-test: every example validates and renders in both versions; the
learner version of a spec with answers differs from its key; every bad spec
is refused with the expected problem; an edited spec gets a new inline
revision; and, when cc-intelligent-ui is installed, its renderer draws an
inline block. Stdlib only. Run: python3 tests/selftest.py
"""
from __future__ import annotations

import copy
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
        expect("warning" not in r.stdout, f"check {ex.name} gives no layout warning")
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

    # Layout geometry: every graph example and every spec in tests/layout/, in
    # both versions, draws no node or label over another, no edge through a
    # node other than its ends and no edge through another edge's label. The
    # records must match the spec (one box per node and drawn label, one path
    # per edge, every box with area), or the geometry was not read. A spec
    # whose first line is `# expect-collision: <pair>` is deliberately dense:
    # it must draw that collision, and check, render and inline must say so.
    layouts = [ex for ex in examples if ex.stem in organizer.GRAPHS] + sorted((ROOT / "tests" / "layout").glob("*.yaml"))
    reference = None
    for spec in layouts:
        first = spec.read_text(encoding="utf-8").splitlines()[0]
        dense = first.removeprefix("# expect-collision:").strip() if first.startswith("# expect-collision:") else None
        if dense:
            line = f"warning (key, learner): {dense}"
            r = run("check", str(spec))
            expect(r.returncode == 0 and f"  {line}\n" in r.stdout, f"check {spec.name} warns: {line!r}")
            r = run("render", str(spec), "--format", "png", "--version", "key", "--ppi", "40", "--out-dir", str(out))
            expect(r.returncode == 0 and line in r.stderr and Path(r.stdout.strip()).is_file(),
                   f"render {spec.name} draws it and warns the same")
            r = run("inline", str(spec))
            expect(r.returncode == 0 and r.stdout.startswith("```typst") and line in r.stderr,
                   f"inline {spec.name} prints the block and warns the same")
        for version in ("key", "learner"):
            try:
                data, records = organizer.read_layout(spec, version)
            except organizer.GeometryError as e:
                expect(False, f"geometry {spec.name} ({version}) is read: {e}")
                continue
            graphs = organizer.assemble(records)
            want = organizer.expected_graphs(data)
            errs = organizer.validate_geometry(graphs, want)
            got = [sum(1 for g in graphs.values() for el in g.values() if el["kind"] == k) for k in ("node", "label", "edge")]
            need = [sum(w[k] for w in want) for k in ("node", "label", "edge")]
            expect(bool(want) and not errs, f"geometry {spec.name} ({version}): {got[0]} node boxes + {got[1]} label boxes + "
                   f"{got[2]} edge paths recorded, the spec draws {' + '.join(map(str, need))}, every box with area {errs[:2]}")
            hits = organizer.collisions(graphs)
            if dense:
                expect(dense in hits, f"layout {spec.name} ({version}) draws the collision it is built for {hits}")
            else:
                expect(not hits, f"layout {spec.name} ({version}) draws no collision {hits}")
            if spec.name == "concept-map.yaml" and version == "key":
                reference = (graphs, want)

    # The check itself, fed a real render's geometry: two concept boxes moved
    # onto each other are reported; no records, a missing record or boxes
    # without area are never a clean layout.
    if reference:
        graphs, want = reference
        moved = copy.deepcopy(graphs)
        g = next(iter(moved.values()))
        by_id = {el["id"]: el for el in g.values()}
        by_id["concept anchor"]["box"] = tuple(v + 6 for v in by_id["concept duct"]["box"])
        hits = organizer.collisions(moved)
        expect({"concept anchor overlaps concept duct", "concept duct overlaps concept anchor"} & set(hits),
               f"two concept boxes forced to overlap are reported {hits[:3]}")
        expect(bool(organizer.validate_geometry({}, want)), "no geometry records is not a clean layout")
        fewer = copy.deepcopy(graphs)
        g = next(iter(fewer.values()))
        del g[next(k for k, el in g.items() if el["kind"] == "label")]
        expect(bool(organizer.validate_geometry(fewer, want)), "a missing label record is not a clean layout")
        flat = copy.deepcopy(graphs)
        for el in next(iter(flat.values())).values():
            if "box" in el:
                el["box"] = (0.0, 0.0, 0.0, 0.0)
        expect(bool(organizer.validate_geometry(flat, want)), "boxes without area are not a clean layout")
    else:
        expect(False, "the concept-map example's geometry was read for the check's own tests")

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
