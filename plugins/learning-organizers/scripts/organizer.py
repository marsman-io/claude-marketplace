#!/usr/bin/env python3
"""Build, check and render graphic organizers from a YAML/JSON spec.

The spec file is the source of truth; every PDF, PNG, SVG and inline picture
is rebuilt from it with Typst (typst/organizers.typ). Stdlib only.

  organizer.py types                      list the organizer types
  organizer.py new <type> <path.yaml>     start a spec from the worked example
  organizer.py check <spec>               validate (exit 1 on problems)
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
    sys.exit(1 if check(spec_path(a.spec)) else 0)


def cmd_render(a: argparse.Namespace) -> None:
    spec = spec_path(a.spec)
    if check(spec, quiet=True):
        check(spec)
        sys.exit(1)
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
