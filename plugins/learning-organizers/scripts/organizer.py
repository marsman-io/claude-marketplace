#!/usr/bin/env python3
"""Build, check and render graphic organizers from a YAML/JSON spec.

The spec file is the source of truth; every PDF, PNG, SVG and inline picture
is rebuilt from it with Typst (typst/organizers.typ). Stdlib only.

  organizer.py types                      list the organizer types
  organizer.py new <type> <path.yaml>     start a spec from the worked example
  organizer.py check <spec>               validate (exit 1 on problems; a concept
                                          map, flow chart or mind map whose drawing
                                          keeps an overlap gets a warning line)
  organizer.py render <spec> [options]    write <stem>.<version>.<ext> files
  organizer.py inline <spec> [--version]  print a ```typst block that
                                          cc-intelligent-ui draws in the terminal
  organizer.py doctor                     show typst, packages, renderer

Exit codes: 0 ok, 1 the spec has problems, 2 a tool or usage error.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "typst" / "organizers.typ"
PAGE = ROOT / "typst" / "standalone.typ"
EXAMPLES = ROOT / "examples"
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "learning-organizers"
IUI_GLOB = str(Path.home() / ".claude/plugins/cache/*/cc-intelligent-ui/*/render/packages")


def die(msg: str, code: int = 2) -> None:
    print(f"organizer: {msg}", file=sys.stderr)
    sys.exit(code)


def typst_bin() -> str:
    t = shutil.which("typst") or next((p for p in ("/opt/homebrew/bin/typst", "/usr/local/bin/typst") if os.path.exists(p)), None)
    if not t:
        die("typst is not installed (macOS: brew install typst; else https://github.com/typst/typst#installation)")
    return t


def package_path() -> str | None:
    """cetz 0.5.2 and fletcher 0.5.8: the copy cc-intelligent-ui vendors, so
    renders work offline and match its inline drawings. Without it Typst
    downloads them once into its own cache."""
    env = os.environ.get("LEARNING_ORGANIZERS_PACKAGES")
    if env:
        return env
    found = sorted(p for p in glob.glob(IUI_GLOB) if os.path.isdir(os.path.join(p, "preview", "fletcher", "0.5.8")))
    return found[-1] if found else None


def typst(args: list[str], spec: Path, inputs: dict[str, str]) -> subprocess.CompletedProcess:
    cmd = [typst_bin(), *args[:1], "--root", "/"]
    pp = package_path()
    if pp:
        cmd += ["--package-path", pp]
    cmd += ["--input", f"spec={spec}"]
    for k, v in inputs.items():
        cmd += ["--input", f"{k}={v}"]
    cmd += args[1:]
    return subprocess.run(cmd, capture_output=True, text=True)


def spec_path(p: str) -> Path:
    path = Path(p).expanduser().resolve()
    if not path.is_file():
        die(f"no such spec: {p}")
    if path.suffix.lower() not in (".yaml", ".yml", ".json"):
        die(f"a spec is a .yaml, .yml or .json file: {p}")
    return path


def check(spec: Path, quiet: bool = False) -> list[str]:
    r = typst(["eval", "query(<organizer-check>).map(it => it.value)", "--in", str(PAGE), "--format", "json"], spec, {"format": "png"})
    if r.returncode != 0:
        # YAML syntax errors and Typst failures land here.
        print(r.stderr.strip(), file=sys.stderr)
        die(f"typst could not read {spec.name}", 1)
    errs: list[str] = []
    for entry in json.loads(r.stdout or "[]"):
        errs += entry.get("errors", [])
    if not quiet:
        if errs:
            print(f"{spec.name}: {len(errs)} problem(s)")
            for e in errs:
                print(f"  - {e}")
        else:
            kinds = sorted({str(e.get('type')) for e in json.loads(r.stdout or '[]')})
            print(f"{spec.name}: ok ({', '.join(kinds)})")
    return errs


# ---------- layout geometry (concept maps, flow charts, mind maps) ----------
#
# The renderer leaves <organizer-geometry> records of what it drew: the corners
# of every node and label box and points along every edge, in page points.
# layout() reads them for one version, checks them against the spec (one box
# per node, one per drawn label, one path per edge: anything else means the
# geometry could not be read) and returns the collisions.

GRAPHS = ("concept-map", "flow-chart", "mind-map")
TOLERANCE = 1.0  # pt: overlaps and crossings deeper than this count, for every spec


class GeometryError(Exception):
    """The geometry could not be read or does not match the spec."""


def _as_list(x) -> list:
    return [] if x is None else x if isinstance(x, list) else [x]


def expected_graphs(spec) -> list[dict]:
    """Type and node, label and edge counts of every graph the spec draws, in document order."""
    if not isinstance(spec, dict):
        return []
    t = spec.get("type")
    if t == "concept-map":
        links = [l for l in _as_list(spec.get("links")) if isinstance(l, dict)]
        return [{"type": t, "node": len(_as_list(spec.get("concepts"))), "edge": len(links),
                 "label": sum(1 for l in links if l.get("label") is not None)}]
    if t == "flow-chart":
        steps = _as_list(spec.get("steps"))
        edges = labels = 0
        for i, st in enumerate(steps):
            nx, br = _as_list(st.get("next")), _as_list(st.get("branches"))
            edges += len(nx) + len(br)
            labels += sum(1 for b in br if isinstance(b, dict) and b.get("label") is not None)
            if not nx and not br and str(st.get("kind", "step")) != "end" and i + 1 < len(steps):
                edges += 1
        return [{"type": t, "node": len(steps), "edge": edges, "label": labels}]
    if t == "mind-map":
        def size(b) -> int:
            return 1 + sum(size(c) for c in (_as_list(b.get("children")) if isinstance(b, dict) else []))
        n = sum(size(b) for b in _as_list(spec.get("branches")))
        return [{"type": t, "node": n + 1, "edge": n, "label": 0}]
    if t == "handout":
        return [g for it in _as_list(spec.get("items")) for g in expected_graphs(it)]
    if t == "structured-notes":
        return [g for sec in _as_list(spec.get("sections")) if isinstance(sec, dict) and sec.get("kind") == "organizer"
                for g in expected_graphs(sec.get("organizer")) if g["type"] in GRAPHS]
    return []


def read_layout(spec: Path, version: str) -> tuple[dict, list[dict]]:
    """The spec as Typst reads it, and the geometry records one version draws."""
    load = "json" if spec.suffix.lower() == ".json" else "yaml"
    r = typst(["eval", f"(spec: {load}(sys.inputs.spec), geometry: query(<organizer-geometry>).map(it => it.value))",
               "--in", str(PAGE), "--format", "json"], spec, {"format": "png", "version": version})
    if r.returncode != 0:
        raise GeometryError(f"typst could not lay out {spec.name} ({version}): {r.stderr.strip()[:300]}")
    out = json.loads(r.stdout)
    return out["spec"], out["geometry"]


def assemble(records: list[dict]) -> dict[int, dict[str, dict]]:
    """graph → element key → {kind, id, ends, shape, box (x0, y0, x1, y1) | path [(x, y), …]}.
    An edge's canvas points are mapped onto the page through its graph's frame marks."""
    graphs: dict[int, dict[str, dict]] = {}
    for r in records:
        el = graphs.setdefault(r["graph"], {}).setdefault(r["key"], {
            "kind": r["kind"], "id": r["id"], "ends": r.get("ends"), "shape": r.get("shape", "box"),
            "pages": set(), "parts": {}})
        el["pages"].add(r["page"])
        el["parts"][r["part"]] = (float(r["x"]), float(r["y"]))
        if r.get("pts") is not None:
            el["pts"] = r["pts"]
        if r.get("unit") is not None:
            el["unit"] = float(r["unit"])
    for g in graphs.values():
        frame = g.pop("frame", None)
        for el in g.values():
            parts = el.pop("parts")
            if el["kind"] == "edge":
                el["path"] = []
                if frame and {"o", "x", "y"} <= set(frame["parts"]) and frame.get("unit"):
                    (ox, oy), (xx, xy), (yx, yy) = (frame["parts"][k] for k in ("o", "x", "y"))
                    u = frame["unit"]
                    el["path"] = [(ox + (xx - ox) * px / u + (yx - ox) * py / u,
                                   oy + (xy - oy) * px / u + (yy - oy) * py / u) for px, py in el.pop("pts", [])]
            elif "tl" in parts and "br" in parts:
                el["box"] = (*parts["tl"], *parts["br"])
    return graphs


def validate_geometry(graphs: dict[int, dict[str, dict]], want: list[dict]) -> list[str]:
    """Why these records cannot be trusted as the drawing of this spec ([] when they can)."""
    errs = []
    if len(graphs) != len(want):
        errs.append(f"{len(graphs)} graph(s) recorded, the spec draws {len(want)}")
    for (gid, g), w in zip(sorted(graphs.items()), want):
        for kind in ("node", "label", "edge"):
            n = sum(1 for el in g.values() if el["kind"] == kind)
            if n != w[kind]:
                errs.append(f"graph {gid} ({w['type']}): {n} {kind} record(s), the spec has {w[kind]}")
        for el in g.values():
            if len(el["pages"]) != 1:
                errs.append(f"{el['id']}: drawn across pages {sorted(el['pages'])}")
            if el["kind"] == "edge":
                p = el["path"]
                if len(p) < 2 or all(q == p[0] for q in p):
                    errs.append(f"{el['id']}: no drawn path")
                if not isinstance(el["ends"], list) or any(k not in g or g[k]["kind"] != "node" for k in el["ends"]):
                    errs.append(f"{el['id']}: its ends {el['ends']} are not recorded nodes")
            else:
                b = el.get("box")
                if b is None:
                    errs.append(f"{el['id']}: box corners missing")
                elif b[2] - b[0] <= 0 or b[3] - b[1] <= 0:
                    errs.append(f"{el['id']}: box has no area ({b[2] - b[0]:.1f}×{b[3] - b[1]:.1f} pt)")
                if el["kind"] == "label" and (el["ends"] not in g or g[el["ends"]]["kind"] != "edge"):
                    errs.append(f"{el['id']}: its edge {el['ends']} is not recorded")
    return errs


def outline(el: dict) -> list[tuple[float, float]]:
    """A node or label's drawn outline as a convex polygon: its box, or the diamond inscribed in it."""
    x0, y0, x1, y1 = el["box"]
    if el["shape"] == "diamond":
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        return [(x0, ym), (xm, y0), (x1, ym), (xm, y1)]
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _collide(a: list[tuple[float, float]], b: list[tuple[float, float]]) -> bool:
    """Separating axes: two convex shapes (a segment is one) collide when, along
    every edge normal of either, one must move more than the tolerance to clear
    the other."""
    for poly in (a, b):
        for (px, py), (qx, qy) in zip(poly, poly[1:] + poly[:1]):
            nx, ny = qy - py, px - qx
            norm = (nx * nx + ny * ny) ** 0.5
            if norm == 0:
                continue
            pa = [(x * nx + y * ny) / norm for x, y in a]
            pb = [(x * nx + y * ny) / norm for x, y in b]
            if min(max(pa) - min(pb), max(pb) - min(pa)) <= TOLERANCE:
                return False
    return True


def collisions(graphs: dict[int, dict[str, dict]]) -> list[str]:
    """One line per colliding pair: a node or label over another, an edge
    through a node other than its two ends, an edge through another edge's label."""
    out = []
    for g in graphs.values():
        boxes = [el for el in g.values() if el["kind"] != "edge"]
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                if _collide(outline(a), outline(b)):
                    out.append(f"{a['id']} overlaps {b['id']}")
        for key, e in g.items():
            if e["kind"] != "edge":
                continue
            segments = list(zip(e["path"], e["path"][1:]))
            for k, b in g.items():
                if (b["kind"] == "node" and k not in e["ends"]) or (b["kind"] == "label" and b["ends"] != key):
                    if any(_collide(list(s), outline(b)) for s in segments):
                        out.append(f"{e['id']} crosses {b['id']}")
    return out


def layout(spec: Path, version: str) -> list[str] | None:
    """The collisions one version draws (None: it draws no graph); GeometryError when that cannot be told."""
    data, records = read_layout(spec, version)
    want = expected_graphs(data)
    if not want and not records:
        return None
    graphs = assemble(records)
    errs = validate_geometry(graphs, want)
    if errs:
        raise GeometryError("; ".join(errs))
    return collisions(graphs)


def layout_warnings(spec: Path) -> list[str]:
    """`warning (versions): <pair>` for every collision a valid spec's drawing keeps.
    A layout the renderer could not settle is drawn anyway and reported here
    (check, render and inline all say it); geometry that cannot be read is a
    tool error (exit 2), never a clean layout."""
    found: dict[str, list[str]] = {}
    for version in ("key", "learner"):
        try:
            hits = layout(spec, version)
        except GeometryError as e:
            die(f"cannot tell whether {spec.name} lays out cleanly: {e}")
        if hits is None:
            return []
        for h in hits:
            found.setdefault(h, []).append(version)
    return [f"warning ({', '.join(v)}): {h}" for h, v in found.items()]


LAYOUT_HINT = "the drawing keeps these overlaps; shorter labels, or fewer links into and out of one node, usually clear them"


def cmd_types(_: argparse.Namespace) -> None:

    for f in sorted(EXAMPLES.glob("*.yaml")):
        first = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        print(f"{f.stem:22} {first}")


def cmd_new(a: argparse.Namespace) -> None:
    src = EXAMPLES / f"{a.type}.yaml"
    if not src.is_file():
        die(f"unknown type {a.type!r}; run `organizer.py types`")
    dst = Path(a.path).expanduser()
    if dst.exists() and not a.force:
        die(f"{dst} exists (pass --force to overwrite)")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"wrote {dst} from the {a.type} example; edit it, then `organizer.py render {dst}`")


def cmd_check(a: argparse.Namespace) -> None:
    spec = spec_path(a.spec)
    if check(spec):
        sys.exit(1)
    warnings = layout_warnings(spec)
    for w in warnings:
        print(f"  {w}")
    if warnings:
        print(f"  ({LAYOUT_HINT})")


def warn_layout(spec: Path) -> None:
    """render and inline draw a spec whose layout keeps overlaps, and say so on stderr."""
    warnings = layout_warnings(spec)
    for w in warnings:
        print(f"organizer: {spec.name}: {w}", file=sys.stderr)
    if warnings:
        print(f"organizer: {spec.name}: {LAYOUT_HINT}", file=sys.stderr)


def cmd_render(a: argparse.Namespace) -> None:
    spec = spec_path(a.spec)
    if check(spec, quiet=True):
        check(spec)
        sys.exit(1)
    warn_layout(spec)
    out_dir = Path(a.out_dir).expanduser().resolve() if a.out_dir else spec.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for version in a.version.split(","):
        if version not in ("key", "learner"):
            die(f"--version takes key and/or learner, not {version!r}")
        for fmt in a.format.split(","):
            if fmt not in ("pdf", "png", "svg"):
                die(f"--format takes pdf, png and/or svg, not {fmt!r}")
            suffix = ".dark" if a.dark and fmt != "pdf" else ""
            out = out_dir / f"{spec.stem}.{version}{suffix}.{fmt}"
            inputs = {"version": version, "format": fmt, "paper": a.paper,
                      "dark": "true" if a.dark and fmt != "pdf" else "false"}
            extra = ["--ppi", str(a.ppi)] if fmt == "png" else []
            r = typst(["compile", str(PAGE), str(out), *extra], spec, inputs)
            if r.returncode != 0:
                print(r.stderr.strip(), file=sys.stderr)
                die(f"render failed: {out.name}")
            written.append(out)
    for w in written:
        print(w)


def stable_lib() -> Path:
    """A copy of the library under a content-addressed path, so inline blocks
    already in a transcript keep compiling after the plugin updates."""
    digest = hashlib.sha256(LIB.read_bytes()).hexdigest()[:12]
    dst = CACHE / "lib" / digest / "organizers.typ"
    if not dst.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.with_suffix(".tmp")
        shutil.copyfile(LIB, tmp)
        os.replace(tmp, dst)
    return dst


def cmd_inline(a: argparse.Namespace) -> None:
    spec = spec_path(a.spec)
    if check(spec, quiet=True):
        check(spec)
        sys.exit(1)
    warn_layout(spec)
    rev = hashlib.sha256(spec.read_bytes()).hexdigest()[:8]
    lib = stable_lib()
    # The revision comment changes the block's text whenever the spec does,
    # so the renderer's cache draws the edited organizer, not the old one.
    print("```typst")
    print(f"// learning-organizers: {spec.name} ({a.version}, rev {rev})")
    print(f"#import {json.dumps(str(lib))}: organizer")
    print(f"#organizer({json.dumps(str(spec))}, theme: theme, version: {json.dumps(a.version)})")
    print("```")


def cmd_doctor(_: argparse.Namespace) -> None:
    t = shutil.which("typst")
    print(f"typst:     {t or 'missing (brew install typst)'}")
    if t:
        print(f"version:   {subprocess.run([t, '--version'], capture_output=True, text=True).stdout.strip()}")
    pp = package_path()
    print(f"packages:  {pp or 'none vendored; typst downloads cetz 0.5.2 and fletcher 0.5.8 on first render'}")
    iui = sorted(glob.glob(str(Path.home() / ".claude/plugins/cache/*/cc-intelligent-ui/*")))
    print(f"inline:    {'cc-intelligent-ui ' + Path(iui[-1]).name if iui else 'cc-intelligent-ui not installed: show PNGs instead'}")
    print(f"library:   {LIB}")


def main() -> None:
    p = argparse.ArgumentParser(prog="organizer.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("types").set_defaults(fn=cmd_types)
    n = sub.add_parser("new")
    n.add_argument("type")
    n.add_argument("path")
    n.add_argument("--force", action="store_true")
    n.set_defaults(fn=cmd_new)
    c = sub.add_parser("check")
    c.add_argument("spec")
    c.set_defaults(fn=cmd_check)
    r = sub.add_parser("render")
    r.add_argument("spec")
    r.add_argument("--format", default="pdf,png", help="pdf,png,svg (comma list; default pdf,png)")
    r.add_argument("--version", default="key,learner", help="key,learner (comma list; default both)")
    r.add_argument("--dark", action="store_true", help="dark PNG/SVG (PDFs stay light for print)")
    r.add_argument("--paper", default="us-letter", choices=("us-letter", "a4"))
    r.add_argument("--ppi", type=int, default=144)
    r.add_argument("--out-dir")
    r.set_defaults(fn=cmd_render)
    i = sub.add_parser("inline")
    i.add_argument("spec")
    i.add_argument("--version", default="key", choices=("key", "learner"))
    i.set_defaults(fn=cmd_inline)
    sub.add_parser("doctor").set_defaults(fn=cmd_doctor)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
