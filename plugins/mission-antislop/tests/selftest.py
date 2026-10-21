#!/usr/bin/env python3
"""Self-test: every rule row of slop_scan.py and every category it emits flags one input
and stays silent on a near-miss, run through the scanner's command line against real
throwaway git repositories and report files; the case table is checked against the rules
the code enumerates; the exit codes, the JSON shape and the pragma listing are pinned; and
the README's category table is proven equal to the code's. Stdlib only.
Run: python3 tests/selftest.py
"""
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCANNER = ROOT / "scripts" / "slop_scan.py"

failures: list[str] = []


def expect(ok: bool, what: str) -> None:
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts"))
import slop_scan  # noqa: E402  (only to enumerate its rule tables)


# --- harness ----------------------------------------------------------------------------

class Sandbox:
    """A temp folder whose git never sees the real config: HOME, the global config and the
    system config all point inside it, and repository discovery stops at its root."""

    def __init__(self, tmp: str):
        self.root = Path(os.path.realpath(tmp))
        (self.root / "gitconfig").write_text(
            "[user]\n\tname = selftest\n\temail = selftest@example.invalid\n"
            "[commit]\n\tgpgsign = false\n", encoding="utf-8")
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(HOME=str(self.root), XDG_CONFIG_HOME=str(self.root), GIT_CONFIG_NOSYSTEM="1",
                   GIT_CONFIG_GLOBAL=str(self.root / "gitconfig"),
                   GIT_CEILING_DIRECTORIES=str(self.root), LC_ALL="C")
        self.env = env

    def git(self, repo: Path, *args: str) -> str:
        proc = subprocess.run(["git", "-C", str(repo), *args], env=self.env,
                              capture_output=True, text=True)
        if proc.returncode != 0:
            raise SystemExit(f"selftest harness: git {' '.join(args)}: {proc.stderr.strip()}")
        return proc.stdout

    def repo(self, name: str, base: dict) -> Path:
        """A repository with `base` committed on main, then a branch `change` checked out."""
        repo = self.root / name
        repo.mkdir()
        self.git(repo, "init", "-q")
        self.git(repo, "symbolic-ref", "HEAD", "refs/heads/main")
        self.write(repo, base)
        self.git(repo, "commit", "-q", "-m", "base")
        self.git(repo, "checkout", "-q", "-b", "change")
        return repo

    def write(self, repo: Path, files: dict, stage: bool = True) -> None:
        """Write each file (None deletes it); stage by explicit pathspec unless told not to."""
        for path, text in files.items():
            target = repo / path
            if text is None:
                self.git(repo, "rm", "-q", "--", path)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            if stage:
                self.git(repo, "add", "--", path)

    def commit(self, repo: Path, files: dict) -> str:
        self.write(repo, files)
        self.git(repo, "commit", "-q", "-m", "change")
        return self.git(repo, "rev-parse", "HEAD").strip()

    def scan(self, *args: str, as_json: bool = True, label: str = "") -> "Scan":
        argv = [sys.executable, str(SCANNER), *args] + (["--json"] if as_json else [])
        proc = subprocess.run(argv, cwd=str(self.root), env=self.env, capture_output=True,
                              text=True)
        result = Scan(proc.returncode, proc.stdout, proc.stderr, None)
        if as_json and proc.returncode in (0, 1):
            result.data = check_json(proc.stdout, label or " ".join(args))
        return result


class Scan:
    def __init__(self, code: int, out: str, err: str, data):
        self.code, self.out, self.err, self.data = code, out, err, data

    def at(self, where: str) -> list:
        """(category, severity) of every finding at `where`, a `path:line`."""
        return [(f["category"], f["severity"]) for f in (self.data or {}).get("findings", [])
                if f["where"] == where]

    def under(self, path: str) -> list:
        """(category, severity) of every finding on `path`, at a line or on the whole file."""
        return [(f["category"], f["severity"]) for f in (self.data or {}).get("findings", [])
                if f["where"] == path or f["where"].startswith(path + ":")]


FINDING_KEYS = {"severity", "category", "where", "text", "note"}


def check_json(out: str, label: str):
    """C5: stdout parses, has meta/counts/findings, and the counts agree with the findings."""
    try:
        data = json.loads(out)
    except ValueError as exc:
        expect(False, f"json parses ({label}): {exc}")
        return None
    shape = isinstance(data, dict) and {"meta", "counts", "findings"} <= set(data) \
        and all(isinstance(f, dict) and set(f) == FINDING_KEYS for f in data["findings"])
    tallies = {s: sum(1 for f in data.get("findings", []) if f.get("severity") == s)
               for s in ("high", "review", "info")}
    expect(shape and data["counts"] == tallies,
           f"json shape and counts agree ({label}): counts {data.get('counts')} tallies {tallies}")
    return data


# --- C1: the rules, as the code enumerates them -----------------------------------------

def literal_categories() -> set:
    """Every category the scanner emits through a literal Finding(severity, "<category>", …)."""
    tree = ast.parse(SCANNER.read_text(encoding="utf-8"))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "Finding" and len(node.args) >= 2 \
                and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str):
            found.add(node.args[1].value)
    return found


def enumerated_keys() -> set:
    keys = {(table, i, row[0], row[1]) for table in ("ADDED_RULES", "REPORT_RULES")
            for i, row in enumerate(getattr(slop_scan, table))}
    return keys | {("Finding", c) for c in literal_categories()}


def code_categories() -> set:
    return {category_of(k) for k in enumerated_keys()}


def A(i: int, category: str, severity: str) -> tuple:
    return ("ADDED_RULES", i, category, severity)


def R(i: int, category: str, severity: str) -> tuple:
    return ("REPORT_RULES", i, category, severity)


def F(category: str) -> tuple:
    return ("Finding", category)


def category_of(key: tuple) -> str:
    return key[1] if key[0] == "Finding" else key[2]


def case_name(key: tuple) -> str:
    return f"Finding {key[1]}" if key[0] == "Finding" else f"{key[0]}[{key[1]}] {key[2]}/{key[3]}"


# --- C2/C3: diff cases ------------------------------------------------------------------
# One repository holds every diff case: DIFF_BASE is committed on main and DIFF_HEAD on the
# branch (None deletes a file). A case reads one `where` (`path:line`, or a bare path for
# the whole file) in one run ("plain", or "docs" for --include-docs). A "flag" case asserts
# the findings at `where` are exactly [(category, severity)] (the row's severity unless the
# case names another), so first-match-wins and the pragma both show; a "miss" case asserts
# no finding of the key's category there.

DIFF_BASE = {
    "README.md": "base\n",
    "tests/test_rm.py": "def test_rm():\n    assert a == 1\n    assert b == 2\n",
    "tests/test_rw.py": "def test_rw():\n    assert a == 1\n",
    "tests/test_l2.py": "def test_l2():\n    assert x == 1\n",
    "tests/test_l3.py": "def test_l3():\n    assert f() == 1\n",
    "tests/test_l4.py": "def test_l4():\n    assert f() == 1\n",
    "tests/test_l5.py": "def test_l5():\n    assert f() == 1\n",
    "tests/test_l6.py": "def test_l6():\n    assert x == 1\n    assert f()\n",
    "tests/l1.test.ts": "expect(total).toBe(3);\n",
    "tests/l1m.test.ts": "expect(total).toBe(3);\n",
    "tests/test_old.py": "# the retired parser suite\ndef test_old_parser():\n    assert parse('q') == 7\n",
    "src/old_helper.go": "package helper\n\nfunc Retired() int { return 41 }\n",
}

DIFF_HEAD = {
    # placeholder, any scope
    "src/a0.py": "def load():\n    raise NotImplementedError\n",
    "vendor/a0.py": "def load():\n    raise NotImplementedError\n",
    "docs/a0.md": "The exporter is not implemented.\n",
    "src/a0b.py": "x = 1  # TODO: not implemented\n",
    # placeholder, comment scope
    "src/a1.py": "def run():\n    # rest of the implementation goes here\n    return 0\n",
    "src/a1m.py": "msg = \"rest of the implementation\"\n",
    "src/a2.ts": "// placeholder until the API lands\nexport const api = 1;\n",
    "src/a2m.tsx": "export const F = () => <input placeholder=\"Name\" />;\n",
    "src/a2b.py": "# placeholder TODO\n",
    # marker
    "src/a3.go": "package a\n\n// TODO: handle retries\n",
    "src/a3m.py": "TODO = 3\n",
    # deferral
    "src/a4.py": "limit = 10  # hard-coded for the demo\n",
    "src/a4m.py": "label = \"for now\"\n",
    "src/a4b.py": "# TODO: remove this workaround\n",
    # skipped-test
    "tests/a5.test.ts": "it.skip(\"does x\", () => {\n  run();\n});\n",
    "tests/a5m.test.ts": "// use it.skip( only with a linked issue\n",
    "tests/a6.test.ts": "describe.skipIf(isWindows)(\"x\", () => {\n  run();\n});\n",
    "tests/a6m.test.ts": "// describe.skipIf( is fine for a platform gap\n",
    # swallowed-error, one line
    "src/a7.ts": "try { run(); } catch (e) {}\n",
    "src/a7m.ts": "// never write catch (e) {} here\n",
    "src/a7r.ts": "try { run(); } catch (e) {} // best effort cleanup only\n",
    "src/a7w.ts": "try { run(); } catch (e) {} // ignore\n",
    "tests/a7t.test.ts": "try { run(); } catch (e) {}\n",
    "src/a7p.py": "try:\n    run()\nexcept OSError: pass\n",
    "src/a7pm.py": "try:\n    run()\nexcept OSError: pass_through()\n",
    "src/a8.sh": "rm -f build.out || true\n",
    "src/a8m.sh": "# avoid || true in CI scripts\n",
    # suppression, any scope
    "src/a9.ts": "// @ts-ignore\nconst x = load();\n",
    "docs/a9.md": "Add // eslint-disable only with a reason.\n",
    # type-escape, ts code only
    "src/a10.ts": "const x = y as any;\n",
    "src/a10.test.ts": "const x = y as any;\n",
    "src/a10.py": "x = y as any\n",
    "src/a10c.ts": "// never write `as any` here\n",
    # swallowed-error across lines
    "src/m1.ts": "try {\n  run();\n} catch (e) {\n}\n",
    "src/m1r.ts": "try {\n  run();\n} catch (e) {\n  // the cache is optional here\n}\n",
    "src/m1w.ts": "try {\n  run();\n} catch (e) {\n  // ignore it\n}\n",
    "src/m1m.ts": "try {\n  run();\n} catch (e) {\n  log(e);\n}\n",
    "tests/m1t.test.ts": "try {\n  run();\n} catch (e) {\n}\n",
    "src/m2.py": "try:\n    run()\nexcept OSError:\n    pass\n",
    "src/m2r.py": "try:\n    run()\nexcept OSError:  # the file may be gone\n    pass\n",
    "src/m2m.py": "try:\n    run()\nexcept OSError:\n    log.warning(\"gone\")\n",
    # pragma
    "src/p1.ts": "const x = y as any; // slop-scan: allow\n",
    "src/p1m.ts": "const x = y as any; // slop-scan allow\n",
    "NOTES-p.md": "intro\nevery caller is updated slop-scan: allow\n",
    "NOTES-pq.md": "the `slop-scan: allow` pragma lists a line\n",
    # sweep-claim on doc lines
    "NOTES.md": "intro\nEvery caller is updated.\n",
    "NOTES-m.md": "The phrase `every caller` needs its search.\n",
    "vendor/NOTES.md": "Every caller is updated.\n",
    # assertions removed, loosened, deleted
    "tests/test_rm.py": "def test_rm():\n    assert a == 1\n",
    "tests/test_rw.py": "def test_rw():\n    assert a == 2\n",
    "tests/test_l2.py": "def test_l2():\n    assert x\n",
    "tests/test_l3.py": "def test_l3():\n    assert f()\n",
    "tests/test_l4.py": "def test_l4():\n    assert f() == 2\n",
    "tests/test_l5.py": "def test_l5():\n    assert f() > 0\n",
    "tests/test_l6.py": "def test_l6():\n    assert ok\n    assert g() > 0\n",
    "tests/l1.test.ts": "expect(total).toBeTruthy();\n",
    "tests/l1m.test.ts": "expect(total).toEqual(3);\n",
    "tests/test_old.py": None,
    "src/old_helper.go": None,
}

DIFF_CASES = [
    # (key, kind, where, run, severity when not the row's)
    (A(0, "placeholder", "high"), "flag", "src/a0.py:2", "plain", None),
    (A(0, "placeholder", "high"), "miss", "vendor/a0.py:2", "plain", None),
    (A(0, "placeholder", "high"), "miss", "docs/a0.md:1", "plain", None),
    (A(0, "placeholder", "high"), "flag", "docs/a0.md:1", "docs", None),
    (A(0, "placeholder", "high"), "flag", "src/a0b.py:1", "plain", None),
    (A(1, "placeholder", "high"), "flag", "src/a1.py:2", "plain", None),
    (A(1, "placeholder", "high"), "miss", "src/a1m.py:1", "plain", None),
    (A(2, "placeholder", "review"), "flag", "src/a2.ts:1", "plain", None),
    (A(2, "placeholder", "review"), "miss", "src/a2m.tsx:1", "plain", None),
    (A(2, "placeholder", "review"), "flag", "src/a2b.py:1", "plain", None),
    (A(3, "marker", "review"), "flag", "src/a3.go:3", "plain", None),
    (A(3, "marker", "review"), "miss", "src/a3m.py:1", "plain", None),
    (A(3, "marker", "review"), "miss", "src/a0b.py:1", "plain", None),
    (A(3, "marker", "review"), "miss", "src/a2b.py:1", "plain", None),
    (A(4, "deferral", "review"), "flag", "src/a4.py:1", "plain", None),
    (A(4, "deferral", "review"), "miss", "src/a4m.py:1", "plain", None),
    (A(4, "deferral", "review"), "miss", "src/a4b.py:1", "plain", None),
    (A(5, "skipped-test", "high"), "flag", "tests/a5.test.ts:1", "plain", None),
    (A(5, "skipped-test", "high"), "miss", "tests/a5m.test.ts:1", "plain", None),
    (A(6, "skipped-test", "review"), "flag", "tests/a6.test.ts:1", "plain", None),
    (A(6, "skipped-test", "review"), "miss", "tests/a6m.test.ts:1", "plain", None),
    (A(7, "swallowed-error", "high"), "flag", "src/a7.ts:1", "plain", None),
    (A(7, "swallowed-error", "high"), "miss", "src/a7m.ts:1", "plain", None),
    (A(7, "swallowed-error", "high"), "flag", "src/a7r.ts:1", "plain", "review"),
    # current behaviour, intent open: see followup F1 (one comment word counts as a reason on
    # a one-line swallow; across lines the reason needs three words, as src/m1w.ts shows)
    (A(7, "swallowed-error", "high"), "flag", "src/a7w.ts:1", "plain", "review"),
    (A(7, "swallowed-error", "high"), "flag", "tests/a7t.test.ts:1", "plain", "review"),
    (A(7, "swallowed-error", "high"), "flag", "src/a7p.py:3", "plain", None),
    (A(7, "swallowed-error", "high"), "miss", "src/a7pm.py:3", "plain", None),
    (A(8, "swallowed-error", "review"), "flag", "src/a8.sh:1", "plain", None),
    (A(8, "swallowed-error", "review"), "miss", "src/a8m.sh:1", "plain", None),
    (A(9, "suppression", "review"), "flag", "src/a9.ts:1", "plain", None),
    (A(9, "suppression", "review"), "miss", "docs/a9.md:1", "plain", None),
    (A(9, "suppression", "review"), "flag", "docs/a9.md:1", "docs", None),
    (A(10, "type-escape", "review"), "flag", "src/a10.ts:1", "plain", None),
    (A(10, "type-escape", "review"), "miss", "src/a10.test.ts:1", "plain", None),
    (A(10, "type-escape", "review"), "miss", "src/a10.py:1", "plain", None),
    (A(10, "type-escape", "review"), "miss", "src/a10c.ts:1", "plain", None),
    (F("swallowed-error"), "flag", "src/m1.ts:3", "plain", "high"),
    (F("swallowed-error"), "flag", "src/m1r.ts:3", "plain", "review"),
    (F("swallowed-error"), "flag", "src/m1w.ts:3", "plain", "high"),
    (F("swallowed-error"), "flag", "tests/m1t.test.ts:3", "plain", "review"),
    (F("swallowed-error"), "flag", "src/m2.py:3", "plain", "high"),
    (F("swallowed-error"), "flag", "src/m2r.py:3", "plain", "review"),
    (F("swallowed-error"), "miss", "src/m1m.ts:3", "plain", None),
    (F("swallowed-error"), "miss", "src/m2m.py:3", "plain", None),
    (F("allowed"), "flag", "src/p1.ts:1", "plain", "info"),
    (F("allowed"), "miss", "src/p1m.ts:1", "plain", None),
    (A(10, "type-escape", "review"), "flag", "src/p1m.ts:1", "plain", None),
    (F("allowed"), "flag", "NOTES-p.md:2", "plain", "info"),
    (F("allowed"), "flag", "NOTES-p.md:2", "docs", "info"),
    # current behaviour, intent open: see followup F2 (a pragma on a doc or report line that
    # no rule would flag is not listed; on a scanned code line it always is)
    (F("allowed"), "miss", "NOTES-pq.md:1", "plain", None),
    (F("sweep-claim"), "flag", "NOTES.md:2", "plain", "review"),
    (F("sweep-claim"), "miss", "NOTES-m.md:1", "plain", None),
    (F("sweep-claim"), "miss", "vendor/NOTES.md:1", "plain", None),
    (F("test-deleted"), "flag", "tests/test_old.py", "plain", "high"),
    (F("test-deleted"), "miss", "src/old_helper.go", "plain", None),
    (F("assertion-removed"), "flag", "tests/test_rm.py:3", "plain", "high"),
    (F("assertion-removed"), "miss", "tests/test_rw.py", "plain", None),
    (F("assertion-removed"), "miss", "tests/test_old.py", "plain", None),
    (F("assertion-loosened"), "flag", "tests/l1.test.ts:1", "plain", "review"),
    (F("assertion-loosened"), "flag", "tests/test_l2.py:2", "plain", "review"),
    (F("assertion-loosened"), "flag", "tests/test_l3.py:2", "plain", "review"),
    # a removed truthiness assert must not cancel the loose one added for a strict one
    (F("assertion-loosened"), "flag", "tests/test_l6.py:2", "plain", "review"),
    (F("assertion-loosened"), "miss", "tests/l1m.test.ts", "plain", None),
    (F("assertion-loosened"), "miss", "tests/test_l4.py", "plain", None),
    (F("assertion-loosened"), "miss", "tests/test_l5.py", "plain", None),
]


# --- C2/C3: report cases ----------------------------------------------------------------
# One report file: each case's text, then a blank line; `line` is the case's line within
# its text. A "flag" case asserts (category, severity) is among the findings at that line
# (report rules do not stop at the first match), and an `allowed` line is the only finding
# on its line; a "miss" asserts the category is absent.

REPORT_CASES = [
    # (key, kind, text, line)
    (R(0, "handoff", "high"), "flag", "Done. Let me know if you want the docs too.", 1),
    (R(0, "handoff", "high"), "miss", "The phrase `let me know` is banned in reports.", 1),
    (R(1, "elision", "high"), "flag", "The other handlers follow, and so on.", 1),
    (R(1, "elision", "high"), "miss", "## And so on", 1),
    (R(2, "sweep-claim", "review"), "flag", "No other callers remain.", 1),
    (R(2, "sweep-claim", "review"), "miss", "```\nNo other callers remain.\n```", 2),
    (R(3, "unproven-claim", "review"), "flag", "The retry should now work on Linux.", 1),
    (R(3, "unproven-claim", "review"), "miss", "Avoid `should work` without a command.", 1),
    (R(4, "blanket-green", "review"), "flag", "All tests pass.", 1),
    (R(4, "blanket-green", "review"), "miss", "# All tests pass", 1),
    (R(5, "out-of-scope", "review"), "flag", "Retries are out of scope here.", 1),
    (R(5, "out-of-scope", "review"), "miss", "~~~\nRetries are out of scope here.\n~~~", 2),
    (F("allowed"), "flag", "Fixed it. All tests pass slop-scan: allow", 1),
    (F("allowed"), "flag", "Ran it: 12 passed slop-scan: allow", 1),
    (F("allowed"), "miss", "```\nAll tests pass slop-scan: allow\n```", 2),
    # current behaviour, intent open: see followup F2
    (F("allowed"), "miss", "Reviewed the diff. slop-scan: allow", 1),
]

# green-provenance: (kind, mode, report text); {head7} is the scanned head's short SHA.
GREEN_CASES = [
    ("flag", "diff", "Ran the suite: 12 passed, 0 failed.\n"),
    ("miss", "diff", "Ran the suite at {head7}: 12 passed, 0 failed.\n"),
    ("flag", "no-diff --repo", "Ran the suite: 12 passed, 0 failed.\n"),
    ("miss", "no-diff", "Ran the suite: 12 passed, 0 failed.\n"),
    ("miss", "worktree", "Ran the suite: 12 passed, 0 failed.\n"),
]


def check_coverage() -> None:
    """C1: every enumerated rule row and literal category has a flag and a miss case, and no
    case names a row or category the code does not have."""
    cases = [(c[0], c[1]) for c in DIFF_CASES + REPORT_CASES]
    cases += [(F("green-provenance"), c[0]) for c in GREEN_CASES]
    have: dict = {}
    for key, kind in cases:
        have.setdefault(key, set()).add(kind)
    code = enumerated_keys()
    expect(len(literal_categories()) >= 7,
           f"enumerated {len(slop_scan.ADDED_RULES)} ADDED_RULES, {len(slop_scan.REPORT_RULES)} "
           f"REPORT_RULES rows and literal categories {sorted(literal_categories())}")
    for key in sorted(code, key=str):
        kinds = have.get(key, set())
        expect(kinds == {"flag", "miss"},
               f"coverage: {case_name(key)} has a flag and a miss case (has {sorted(kinds)})")
    for key in sorted(set(have) - code, key=str):
        expect(False, f"coverage: a case names {case_name(key)}, which the code does not have")


def run_diff_cases(box: Sandbox) -> None:
    repo = box.repo("diff", DIFF_BASE)
    head = box.commit(repo, DIFF_HEAD)
    diff = ["--repo", str(repo), "--base", "main", "--head", "HEAD"]
    runs = {"plain": box.scan(*diff, label="diff"),
            "docs": box.scan(*diff, "--include-docs", label="diff --include-docs")}
    for name, result in runs.items():
        meta = result.data["meta"] if result.data else {}
        expect(result.code in (0, 1) and meta.get("head_sha") == head
               and meta.get("diff") == "main...HEAD",
               f"diff run [{name}]: exit {result.code}, meta.head_sha is the repo head")
    for key, kind, where, run, sev in DIFF_CASES:
        result = runs[run]
        cat = category_of(key)
        got = result.under(where) if re.search(r":\d+$", where) is None else result.at(where)
        if kind == "flag":
            want = [(cat, sev or key[3])]
            expect(got == want, f"{case_name(key)} flags {where} as {want[0]} [{run}] (got {got})")
        else:
            expect(all(c != cat for c, _ in got),
                   f"{case_name(key)} near-miss {where}: no {cat} [{run}] (got {got})")


def run_report_cases(box: Sandbox) -> None:
    lines: list = []
    places = []
    for _, _, text, line in REPORT_CASES:
        places.append(len(lines) + line)
        lines.extend(text.split("\n") + [""])
    report = box.root / "report.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    result = box.scan("--no-diff", "--report", str(report), label="no-diff report")
    meta = result.data["meta"] if result.data else {}
    expect(result.data is not None and meta.get("head_sha") is None and meta.get("diff") is None,
           "report run: --no-diff without --repo has no head and no diff")
    for (key, kind, text, _), place in zip(REPORT_CASES, places):
        got = result.at(f"{report}:{place}")
        cat = category_of(key)
        shown = text.replace("\n", " / ")
        if kind == "flag":
            want = (cat, "info" if cat == "allowed" else key[3])
            ok = got == [want] if cat == "allowed" else want in got
            expect(ok, f"{case_name(key)} flags report line {place} {shown!r} (got {got})")
        else:
            expect(all(c != cat for c, _ in got),
                   f"{case_name(key)} near-miss report line {place} {shown!r} (got {got})")


def run_green_cases(box: Sandbox) -> None:
    repo = box.repo("green", {"src/g.py": "x = 1\n"})
    head = box.commit(repo, {"src/g.py": "x = 2\n"})
    modes = {"diff": ["--repo", str(repo), "--base", "main", "--head", "HEAD"],
             "no-diff --repo": ["--no-diff", "--repo", str(repo)],
             "no-diff": ["--no-diff"],
             "worktree": ["--repo", str(repo), "--base", "main", "--worktree"]}
    for n, (kind, mode, text) in enumerate(GREEN_CASES):
        report = box.root / f"green-{n}.md"
        report.write_text(text.format(head7=head[:7]), encoding="utf-8")
        result = box.scan(*modes[mode], "--report", str(report), label=f"green {mode}")
        got = result.at(f"{report}:1")
        hit = ("green-provenance", "review") in got
        want_head = None if mode in ("no-diff", "worktree") else head
        meta = result.data["meta"] if result.data else {}
        expect(result.data is not None and meta.get("head_sha") == want_head
               and hit == (kind == "flag"),
               f"Finding green-provenance {kind} in {mode} mode{' (head named)' if '{' in text else ''}, "
               f"meta.head_sha {'null' if want_head is None else 'the head'} (got {got})")


# --- C4: exit codes, the human summary, the worktree mode -------------------------------

def run_exit_cases(box: Sandbox) -> None:
    repo = box.repo("exits", {"src/base.py": "x = 1\n"})
    branches = {"clean": {"src/ok.py": "y = 2\n"},
                "high": {"src/h.py": "raise NotImplementedError\n"},
                "review": {"src/r.py": "# TODO: tidy\n"},
                "info": {"src/i.ts": "const v = w as any; // slop-scan: allow\n"}}
    for name, files in branches.items():
        box.git(repo, "checkout", "-q", "-b", name, "main")
        box.commit(repo, files)
    diff = ["--repo", str(repo), "--base", "main", "--head", "HEAD"]
    for branch, extra, code in [("clean", [], 0), ("clean", ["--fail-on", "review"], 0),
                                ("high", [], 1), ("high", ["--fail-on", "never"], 0),
                                ("review", [], 0), ("review", ["--fail-on", "review"], 1),
                                ("info", ["--fail-on", "review"], 0)]:
        box.git(repo, "checkout", "-q", branch)
        r = box.scan(*diff, *extra, label=f"exit, {branch} branch {' '.join(extra)}".strip())
        counts = r.data["counts"] if r.data else None
        expect(r.code == code, f"exit {code}: {branch} branch {' '.join(extra) or '(default)'} "
                               f"(got {r.code}, counts {counts})")

    box.git(repo, "checkout", "-q", "high")
    j = box.scan(*diff, label="summary json").data or {"counts": {}}
    text = box.scan(*diff, as_json=False)
    m = re.search(r"^summary: (\d+) high, (\d+) review, (\d+) allowed\.", text.out, re.M)
    got = tuple(int(x) for x in m.groups()) if m else None
    want = tuple(j["counts"].get(s) for s in ("high", "review", "info"))
    expect(got == want and want == (1, 0, 0) and text.code == 1,
           f"human summary line counts equal the JSON counts ({got} vs {want})")

    plain = box.root / "not-a-repo"
    plain.mkdir()
    report = box.root / "exit-report.md"
    report.write_text("All tests pass.\n", encoding="utf-8")
    for args, cause, what in [
            (["--repo", str(repo), "--base", "no-such-ref", "--head", "HEAD"], "no-such-ref",
             "unknown --base ref"),
            (["--repo", str(plain), "--base", "main", "--head", "HEAD"], "not a git repository",
             "--repo that is not a git repository"),
            (["--no-diff", "--repo", str(plain), "--report", str(report)], "not a git repository",
             "--no-diff --repo that is not a git repository"),
            (["--no-diff"], "--no-diff needs at least one --report", "--no-diff with no --report"),
            (["--no-diff", "--report", str(box.root / "missing.md")], "cannot read report",
             "a --report path that does not exist"),
            (["--no-diff", "--report", str(box.root)], "cannot read report",
             "a --report path that is a folder")]:
        r = box.scan(*args, label=what)
        expect(r.code == 2 and cause in r.err and r.out.strip() == "",
               f"exit 2: {what}; stderr names the cause, stdout empty "
               f"(got {r.code}, stderr {r.err.strip()[-80:]!r}, stdout {len(r.out)} chars)")


def run_worktree_case(box: Sandbox) -> None:
    repo = box.repo("worktree", {"src/w.py": "x = 1\n"})
    box.write(repo, {"src/w.py": "x = 1\n# TODO: wt\n", "src/u.ts": "const a = b as any;\n"},
              stage=False)
    r = box.scan("--repo", str(repo), "--base", "main", "--worktree", label="worktree")
    meta = r.data["meta"] if r.data else {}
    expect(r.at("src/w.py:2") == [("marker", "review")]
           and r.at("src/u.ts:1") == [("type-escape", "review")]
           and r.data is not None and meta.get("head_sha") is None
           and meta.get("diff") == "main...(working tree)",
           f"--worktree scans uncommitted and untracked lines, meta.head_sha null "
           f"(w.py:2 {r.at('src/w.py:2')}, u.ts:1 {r.at('src/u.ts:1')}, meta.diff {meta.get('diff')})")


# --- C7: the docs name exactly the code's categories ------------------------------------

def backticked(text: str) -> set:
    """Backticked words outside parentheses (parentheses hold severities, not categories)."""
    return set(re.findall(r"`([a-z][a-z-]*)`", re.sub(r"\([^)]*\)", "", text)))


def check_docs() -> None:
    code = code_categories()
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    rows = re.search(r"^\| Looks at \| Categories \|\n\|[-|]+\|\n((?:\|.*\n)+)", readme, re.M)
    table: set = set()
    for row in (rows.group(1).splitlines() if rows else []):
        table |= backticked(row.split("|")[2])
    expect(rows is not None and table == code - {"allowed"},
           f"README category table equals the code's {len(code - {'allowed'})} categories "
           f"minus allowed (README only {sorted(table - code)}, "
           f"code only {sorted(code - {'allowed'} - table)})")
    prose = readme.replace(rows.group(0), "") if rows else readme
    expect("allowed" in code and "`allowed`" in prose and "allowed" not in table,
           "README prose, not its table, names `allowed`")

    patterns = (ROOT / "docs" / "Slop patterns.md").read_text(encoding="utf-8")
    named: set = set()
    for para in re.findall(r"^\*\*Caught by:\*\*(.*(?:\n.+)*)", patterns, re.M):
        for part in re.sub(r"\([^)]*\)", "", para).split(";"):
            if part.strip().startswith("scanner:"):
                named |= backticked(part)
    expect(len(named) >= 8 and named <= code,
           f"Slop patterns.md names {len(named)} scanner categories, every one in the code "
           f"(unknown {sorted(named - code)})")


# --- run --------------------------------------------------------------------------------

check_coverage()
with tempfile.TemporaryDirectory() as tmp:
    box = Sandbox(tmp)
    run_diff_cases(box)
    run_report_cases(box)
    run_green_cases(box)
    run_exit_cases(box)
    run_worktree_case(box)
check_docs()

print(f"\n{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
