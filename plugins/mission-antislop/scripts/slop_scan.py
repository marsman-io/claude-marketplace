#!/usr/bin/env python3
"""slop_scan: a deterministic completeness-slop pass over a git diff and completion reports.

It flags what a diff ADDS that looks unfinished or hides failure (placeholders, skipped or
focused tests, swallowed errors, check suppressions, type escapes), test assertions and test
files a diff REMOVES, and report wording that claims, elides, downgrades or defers without
evidence. It is the cheap first pass that runs before any expensive review: every hit is a
lead to read, not a verdict.

A line carrying `slop-scan: allow` is not hidden; it is listed under `allowed` so a reviewer
still sees every exemption the author granted themselves.

Exit codes: 0 = nothing at or above --fail-on, 1 = findings at or above --fail-on,
2 = usage or git error. Standard library only; Python 3.8+.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass

ALLOW_PRAGMA = "slop-scan: allow"
ALLOW_NOTE = "author-granted exemption; confirm it is warranted"

# --- path classes -----------------------------------------------------------------------

TEST_PATH = re.compile(
    r"(^|/)(tests?|__tests__|specs?|e2e)/"
    r"|[._-](test|spec)\.[A-Za-z0-9]+$"
    r"|_test\.(go|py|rs|exs?)$"
    r"|(^|/)test_[^/]*\.py$"
)
DOC_PATH = re.compile(r"\.(md|mdx|markdown|txt|rst|adoc)$|(^|/)CHANGELOG[^/]*$", re.I)
SKIP_PATH = re.compile(
    r"(^|/)(yarn\.lock|package-lock\.json|pnpm-lock\.yaml|Cargo\.lock|poetry\.lock|go\.sum)$"
    r"|\.(snap|min\.js|map|svg)$"
    r"|(^|/)(dist|build|vendor|node_modules)/"
)
TS_PATH = re.compile(r"\.(ts|tsx|mts|cts)$")

# --- added-line rules: (category, severity, pattern, scope, path_filter) -----------------
# scope "comment" matches only a line's comment text, so a UI `placeholder=` attribute or a
# "for now" string in product copy does not fire; scope "code" skips comment-only lines, so
# prose that mentions `it.skip(` or `|| true` does not fire; scope "any" matches the whole line.
# path_filter "code" means non-test files only. Rule order matters: first match wins.
# Severities were calibrated against ~30k merged, reviewed lines: "high" should rarely fire on
# finished work; everything that legitimate code also does sits at "review".

ADDED_RULES = [
    ("placeholder", "high", re.compile(
        r"\b(not (yet )?implemented|unimplemented)\b|\btodo!\s*\(|\bunimplemented!\s*\("
        r"|NotImplementedError|throw new Error\(\s*['\"`](todo|tbd|not implemented)", re.I),
     "any", None),
    ("placeholder", "high", re.compile(
        r"^\s*\.\.\.\s*$"
        r"|\brest of (the )?(code|implementation|logic|file|cases)\b"
        r"|\bimplement (this|me|here|later)\b"
        r"|\b(add|fill in) (more|the rest|remaining)\b"
        r"|\bsimilar(ly)? (to|for) (the )?(above|remaining|others|rest)\b", re.I),
     "comment", None),
    ("placeholder", "review", re.compile(r"\bplaceholder\b|\bTBD\b", re.I), "comment", None),
    ("marker", "review", re.compile(r"\b(TODO|FIXME|XXX|HACK)\b"), "comment", None),
    ("deferral", "review", re.compile(
        r"\b(for now|temporar(y|ily)|stub(bed)?|dummy|hard-?coded|quick (fix|hack)|workaround"
        r"|until we|later we)\b", re.I),
     "comment", None),
    ("skipped-test", "high", re.compile(
        r"\.(skip|only|todo|fixme)\s*\("
        r"|\b(xit|xdescribe|xtest|xcontext|fit|fdescribe)\s*\("
        r"|@pytest\.mark\.(skip|xfail)\b|\bpytest\.skip\("
        r"|@(Ignore|Disabled)\b|\bt\.Skip(Now|f)?\(|#\[ignore\]"),
     "code", None),
    ("skipped-test", "review", re.compile(r"\.skipIf\s*\(|\.runIf\s*\(|@pytest\.mark\.skipif\b"),
     "code", None),
    ("swallowed-error", "high", re.compile(
        r"catch\s*(\([^)]*\))?\s*\{\s*\}"
        r"|except\b[^:\n]*:\s*(pass|\.\.\.)\s*(#.*)?$"
        r"|\.catch\(\s*(\(\s*\w*\s*\)|\w+)\s*=>\s*(\{\s*\}|null|undefined|void 0|false)\s*\)"
        r"|\.catch\(\s*(noop|_\.noop)?\s*\)"),
     "code", None),
    ("swallowed-error", "review", re.compile(
        r"\|\|\s*true\b|\|\|\s*:\s*$|\blet _ = |\.ok\(\);|\b_ = \w+\(|\berr\s*=\s*nil\b"),
     "code", None),
    ("suppression", "review", re.compile(
        r"@ts-(ignore|expect-error|nocheck)|eslint-disable|biome-ignore|#\s*type:\s*ignore"
        r"|#\s*noqa|#\[allow\(|//\s*nolint|pylint:\s*disable|(istanbul|c8) ignore"),
     "any", None),
    ("type-escape", "review", re.compile(r"\bas any\b|:\s*any\b|\bas unknown as\b|<any>"),
     "code", "ts-code"),
]


def rule_applies(path_filter: str | None, path: str) -> bool:
    if path_filter == "ts-code":
        return bool(TS_PATH.search(path)) and not TEST_PATH.search(path)
    return True


def adjust_severity(category: str, severity: str, path: str, text: str) -> str:
    """A swallow in a test, or one that states its reason on the same line, is a lead to
    read rather than a likely defect."""
    if category == "swallowed-error" and severity == "high":
        if TEST_PATH.search(path) or comment_text(text) is not None:
            return "review"
    return severity

CATCH_OPEN = re.compile(r"\bcatch\s*(\([^)]*\))?\s*\{\s*(//.*)?$")
EXCEPT_OPEN = re.compile(r"^\s*except\b[^:\n]*:\s*(#.*)?$")
BLOCK_CLOSE = re.compile(r"^\s*\}\s*[;)]*\s*$")
PY_EMPTY_BODY = re.compile(r"^\s*(pass|\.\.\.)\s*(#.*)?$")
ASSERTION = re.compile(
    r"\b(expect|assert\w*|should|require)\s*[.(]|^\s*assert\s|\bt\.(Error|Fatal)f?\("
    r"|\b(assert_eq|assert_ne|assert)!\s*\(")
STRICT_MATCHER = re.compile(
    r"\.(toBe|toEqual|toStrictEqual|toThrow\w*|toHaveBeenCalledWith|toHaveBeenCalledTimes)\("
    r"|\bassert(_eq|_ne)!\s*\(|\bassert(Equal|Equals|StrictEqual|Raises|Throws)\b"
    r"|\bassert\.(equal|strictEqual|deepEqual|deepStrictEqual|throws|rejects)\("
    r"|^\s*assert\s+.*(==|!=|\bis\b|\bin\b)")
LOOSE_MATCHER = re.compile(
    r"\.(toBeDefined|toBeTruthy|toBeFalsy|toBeGreaterThan\w*|toBeLessThan\w*|toContain|toMatch"
    r"|toHaveBeenCalled|toBeInstanceOf)\(|\.not\.toBe(Null|Undefined)\("
    r"|\bassert(True|IsNotNone|Greater\w*|Less\w*)\b|\bassert\.ok\(|^\s*assert\s+\w+\s*$")
# A bare truthiness `assert <expr>` (no comparison) counts as loose only where it is added:
# counted where it is removed, it would cancel the loose one that replaced a strict one.
TRUTHY_ASSERT = re.compile(r"^\s*assert\s+(?!.*(==|!=|<|>|\bis\b|\bin\b))\S")

# --- report rules: (category, severity, pattern, note) ----------------------------------
# Calibrated against ~33k lines of real completion reports and PR bodies. Wording rules that
# fired mostly on honest reporting ("partially refuted", "recorded as a follow-up") were cut:
# deferral is judged by reconciling follow-ups against the brief, not by grepping for it.

SWEEP_CLAIM = re.compile(
    r"\bno (other |remaining |more )?(\w+ ){0,2}(remains?|left|survives?)\b"
    r"|\bnothing else\b|\bno other (\w+ )?(caller|site|consumer|reference|path|use|occurrence)s?\b"
    r"|\b(every|all|each) (other )?(caller|call site|site|consumer|producer|reference|use|usage"
    r"|occurrence|instance|path|code path|branch)s?\b"
    r"|\ball \d+ (\w+ )?(callers|sites|consumers|references|uses|occurrences|instances|tests"
    r"|files|packages)\b"
    r"|\bzero (new )?(failures|regressions|references|hits|occurrences)\b|\bno (new )?regressions\b"
    r"|\bfully (covered|tested|removed|migrated|swept)\b|\bexhaustive(ly)?\b"
    r"|\bcompletely (removed|covered|migrated)\b", re.I)
SWEEP_NOTE = ("a sweep or coverage claim: back it with the enumerating command and its scope, "
              "or an enumerating test, or narrow the wording")

REPORT_RULES = [
    ("handoff", "high", re.compile(
        r"\b(let me know|would you like|shall i|do you want me|if you('d)? (want|like) me to"
        r"|i can (also )?(add|provide|continue|implement) (this|that|it|more|the rest))\b", re.I),
     "a question or offer in an unattended run's report is a stop at a non-gate"),
    ("elision", "high", re.compile(
        r"\b(and so on|the rest (follows|is) (the same|similar(ly)?)"
        r"|similar(ly)? for the (rest|remaining|others)|same (pattern|approach) (applies|for the rest)"
        r"|for brevity|left as an exercise)\b", re.I),
     "elision stands in for work or evidence; enumerate it"),
    ("sweep-claim", "review", SWEEP_CLAIM, SWEEP_NOTE),
    ("unproven-claim", "review", re.compile(
        r"\b(should (now )?(work|pass|be fine|be ok|handle)|works as expected|seems to (work|pass)"
        r"|appears to (work|pass)|presumably|in theory)\b", re.I),
     "a claim with no command and output behind it"),
    ("blanket-green", "review", re.compile(
        r"\ball (the )?tests? (pass|passed|passing|are green|green)\b|\bfully tested\b"
        r"|\b(every|all) (the )?(\w+ )?(checks?|suites?|tests?)\b[^.;]{0,40}?\b(pass|passes|passed|green)\b"
        r"|\bcomprehensive(ly)? tested\b|\b100% (coverage|passing)\b|\beverything (works|passes)\b",
        re.I),
     "name the exact command, its counts, and the comparison against the known baseline"),
    ("out-of-scope", "review", re.compile(r"\bout of scope\b|\bpunted\b|\bnot addressed\b", re.I),
     "deferral needs the brief line that authorises it"),
]

INLINE_CODE = re.compile(r"`[^`]*`")
TEST_FIGURE = re.compile(
    r"\b\d+\s*(passed|failed|passing|failing)\b|\b\d+\s*/\s*\d+\s*(tests?|tasks?|pass(ed)?|green)\b"
    r"|\btests? (all )?pass(ed)?\b|\b(all|every) (tests?|suites?|checks?) (pass|passed|green)\b", re.I)

SEVERITY_RANK = {"never": 99, "high": 2, "review": 1, "info": 0}


@dataclass
class Finding:
    severity: str
    category: str
    where: str
    text: str
    note: str = ""


# --- helpers ----------------------------------------------------------------------------

def git(repo: str, *args: str) -> str:
    cmd = ["git", "-C", repo, "-c", "core.quotePath=false", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)}: {proc.stderr.strip()}")
    return proc.stdout


def comment_text(line: str) -> str | None:
    """Return the comment portion of a code line, or None if it has no comment."""
    stripped = line.lstrip()
    if stripped.startswith(("#[", "#!")):  # Rust attributes, shebangs
        return None
    for marker in ("//", "#", "/*", "*", "--", "<!--", ";"):
        if stripped.startswith(marker):
            return stripped[len(marker):]
    for marker in (" // ", " # ", " /* ", " -- "):
        idx = line.find(marker)
        if idx != -1:
            return line[idx + len(marker):]
    return None


def states_reason(line: str) -> bool:
    """True when a line's comment says why, not just "ignore" or "noop": three words or more."""
    words = re.findall(r"[A-Za-z0-9']+", comment_text(line) or "")
    return len(words) >= 3


def is_comment_only(line: str) -> bool:
    s = line.strip()
    if s.startswith(("#[", "#!")):
        return False
    return s == "" or s.startswith(("//", "#", "/*", "*", "*/"))


def clip(text: str, width: int = 110) -> str:
    text = text.strip()
    return text if len(text) <= width else text[: width - 1] + "…"


# --- diff scan --------------------------------------------------------------------------

class DiffScanner:
    def __init__(self, include_docs: bool):
        self.include_docs = include_docs
        self.findings: list[Finding] = []
        self.files: set[str] = set()
        self.added = 0
        self.removed = 0
        self.assert_delta: dict[str, list] = {}  # path -> [added, removed, removed_lines]
        self.matchers: dict[str, list] = {}  # path -> [strict+, strict-, loose+, loose-, first_ln]
        self._pending: dict[str, tuple] = {}  # path -> (kind, open_ln, text, last_ln, has_reason)

    def wants_code_rules(self, path: str) -> bool:
        if SKIP_PATH.search(path):
            return False
        return self.include_docs or not DOC_PATH.search(path)

    def add(self, path: str, ln: int, text: str) -> None:
        self.added += 1
        self.files.add(path)
        where = f"{path}:{ln}"
        doc_sweep = DOC_PATH.search(path) and not SKIP_PATH.search(path) \
            and SWEEP_CLAIM.search(INLINE_CODE.sub("", text))
        if ALLOW_PRAGMA in text:
            # Listed once, whether it exempts the doc sweep, the code rules, or both.
            if doc_sweep or self.wants_code_rules(path):
                self.findings.append(Finding("info", "allowed", where, clip(text), ALLOW_NOTE))
            return
        if doc_sweep:
            self.findings.append(Finding("review", "sweep-claim", where, clip(text), SWEEP_NOTE))
        if not self.wants_code_rules(path):
            return
        self._track_empty_block(path, ln, text)
        comment_line = is_comment_only(text)
        for category, severity, pattern, scope, path_filter in ADDED_RULES:
            if not rule_applies(path_filter, path) or (scope == "code" and comment_line):
                continue
            target = comment_text(text) if scope == "comment" else text
            if target is not None and pattern.search(target):
                severity = adjust_severity(category, severity, path, text)
                self.findings.append(Finding(severity, category, where, clip(text)))
                break
        if TEST_PATH.search(path):
            if ASSERTION.search(text):
                self.assert_delta.setdefault(path, [0, 0, []])[0] += 1
            self._count_matcher(path, ln, text, added=True)

    def remove(self, path: str, ln: int, text: str) -> None:
        self.removed += 1
        self.files.add(path)
        if TEST_PATH.search(path):
            if ASSERTION.search(text):
                entry = self.assert_delta.setdefault(path, [0, 0, []])
                entry[1] += 1
                entry[2].append((ln, text))
            self._count_matcher(path, ln, text, added=False)

    def _count_matcher(self, path: str, ln: int, text: str, added: bool) -> None:
        entry = self.matchers.setdefault(path, [0, 0, 0, 0, None])
        if STRICT_MATCHER.search(text):
            entry[0 if added else 1] += 1
        elif LOOSE_MATCHER.search(text) or (added and TRUTHY_ASSERT.search(text)):
            entry[2 if added else 3] += 1
            if added and entry[4] is None:
                entry[4] = ln

    def _track_empty_block(self, path: str, ln: int, text: str) -> None:
        """Catch a catch/except whose body, across consecutive added lines, does nothing.
        A body with no stated reason is high; one whose comment says why is a lead (review)."""
        pending = self._pending.get(path)
        if pending:
            kind, open_ln, open_text, last_ln, has_reason = pending
            if ln == last_ln + 1:
                closes = (kind == "catch" and BLOCK_CLOSE.match(text)) or \
                         (kind == "except" and PY_EMPTY_BODY.match(text))
                if closes:
                    has_reason = has_reason or states_reason(text)
                    quiet = has_reason or TEST_PATH.search(path)
                    body = "empty catch body" if kind == "catch" else "except body is only pass"
                    note = f"{body}, reason stated" if has_reason else f"{body}, no reason stated"
                    self.findings.append(Finding("review" if quiet else "high", "swallowed-error",
                                                 f"{path}:{open_ln}", clip(open_text), note))
                    del self._pending[path]
                    return
                if is_comment_only(text):
                    has_reason = has_reason or states_reason(text)
                    self._pending[path] = (kind, open_ln, open_text, ln, has_reason)
                    return
            del self._pending[path]
        opener = "catch" if CATCH_OPEN.search(text) else "except" if EXCEPT_OPEN.match(text) else None
        if opener:
            self._pending[path] = (opener, ln, text, ln, states_reason(text))

    def finish(self, deleted: list[str]) -> None:
        for path in deleted:
            if TEST_PATH.search(path):
                self.findings.append(Finding("high", "test-deleted", path, "(whole file deleted)",
                                             "a deleted test needs a named replacement or the brief's say-so"))
        for path, (added, removed, lines) in sorted(self.assert_delta.items()):
            if removed > added and path not in deleted:
                sample = "; ".join(clip(t, 60) for _, t in lines[:3])
                self.findings.append(Finding(
                    "high", "assertion-removed", f"{path}:{lines[0][0]}",
                    f"-{removed} +{added} assertion lines: {sample}",
                    "net assertions removed from a test file; confirm none was weakened to go green"))
        for path, (s_add, s_rem, l_add, l_rem, first_ln) in sorted(self.matchers.items()):
            if path not in deleted and s_rem > s_add and l_add > l_rem:
                self.findings.append(Finding(
                    "review", "assertion-loosened", f"{path}:{first_ln}",
                    f"exact matchers -{s_rem} +{s_add}, loose matchers +{l_add} -{l_rem}",
                    "exact assertions traded for looser ones; confirm the narrowing is intended "
                    "and disclosed"))


HUNK = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def scan_diff_text(diff: str, scanner: DiffScanner) -> None:
    old_path = new_path = None
    old_ln = new_ln = 0
    for raw in diff.splitlines():
        if raw.startswith("diff --git "):
            old_path = new_path = None
        elif raw.startswith("--- "):
            p = raw[4:].strip()
            old_path = None if p == "/dev/null" else p[2:] if p.startswith("a/") else p
        elif raw.startswith("+++ "):
            p = raw[4:].strip()
            new_path = None if p == "/dev/null" else p[2:] if p.startswith("b/") else p
        elif raw.startswith("@@"):
            m = HUNK.match(raw)
            if m:
                old_ln, new_ln = int(m.group(1)), int(m.group(2))
        elif raw.startswith("+") and new_path:
            scanner.add(new_path, new_ln, raw[1:])
            new_ln += 1
        elif raw.startswith("-") and old_path:
            scanner.remove(old_path, old_ln, raw[1:])
            old_ln += 1


def scan_repo(repo: str, base: str, head: str, worktree: bool, include_docs: bool) -> tuple:
    scanner = DiffScanner(include_docs)
    common = ["--no-color", "--no-ext-diff", "--find-renames", "--src-prefix=a/", "--dst-prefix=b/"]
    if worktree:
        merge_base = git(repo, "merge-base", base, "HEAD").strip()
        diff = git(repo, "diff", *common, "--unified=0", merge_base)
        status = git(repo, "diff", "--name-status", "--find-renames", merge_base)
        label = f"{base}...(working tree)"
    else:
        diff = git(repo, "diff", *common, "--unified=0", f"{base}...{head}")
        status = git(repo, "diff", "--name-status", "--find-renames", f"{base}...{head}")
        label = f"{base}...{head}"
    scan_diff_text(diff, scanner)
    if worktree:
        for path in git(repo, "ls-files", "--others", "--exclude-standard").splitlines():
            try:
                with open(f"{repo}/{path}", encoding="utf-8") as fh:
                    for i, line in enumerate(fh, start=1):
                        scanner.add(path, i, line.rstrip("\n"))
            except (UnicodeDecodeError, OSError):
                continue
    deleted = [ln.split("\t", 1)[1] for ln in status.splitlines() if ln.startswith("D\t")]
    scanner.finish(deleted)
    return scanner, label


# --- report scan ------------------------------------------------------------------------

def scan_report(path: str, head_sha: str | None) -> list[Finding]:
    """Wording rules per line, then one provenance check per report: test figures quoted
    without the head commit anywhere in the report may have come from an earlier commit."""
    findings: list[Finding] = []
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        raise RuntimeError(f"cannot read report {path}: {exc}") from exc
    in_fence = False
    figures: list[int] = []
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence or stripped.startswith("#"):
            continue
        prose = INLINE_CODE.sub("", line)
        if ALLOW_PRAGMA in line:
            # Listed when it exempts a wording rule or a test figure the provenance check counts.
            if TEST_FIGURE.search(prose) or any(rule[2].search(prose) for rule in REPORT_RULES):
                findings.append(Finding("info", "allowed", f"{path}:{i}", clip(line), ALLOW_NOTE))
            continue
        if TEST_FIGURE.search(prose):
            figures.append(i)
        for category, severity, pattern, note in REPORT_RULES:
            if pattern.search(prose):
                findings.append(Finding(severity, category, f"{path}:{i}", clip(line), note))
    if head_sha and figures and head_sha[:7] not in "\n".join(lines):
        findings.append(Finding(
            "review", "green-provenance", f"{path}:{figures[0]}",
            f"{len(figures)} test figure line(s); head {head_sha[:10]} is not named anywhere",
            "tie every pass/fail figure to a log run at the head commit, or re-run it there"))
    return findings


# --- output -----------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="slop_scan.py",
        description="Flag unfinished or failure-hiding lines in a diff, and evidence-free "
                    "wording in completion reports. Every hit is a lead, not a verdict.")
    ap.add_argument("--repo", default=None, help="git checkout to scan (default: .)")
    ap.add_argument("--base", default="origin/main", help="base ref (default: origin/main)")
    ap.add_argument("--head", default="HEAD", help="head ref (default: HEAD)")
    ap.add_argument("--worktree", action="store_true",
                    help="scan merge-base(base, HEAD) against the working tree, untracked files "
                         "included (a self-check before committing)")
    ap.add_argument("--report", action="append", default=[], metavar="FILE",
                    help="completion report / PR body to phrase-scan (repeatable)")
    ap.add_argument("--no-diff", action="store_true", help="scan only the --report files")
    ap.add_argument("--include-docs", action="store_true",
                    help="apply code rules to markdown/text files too")
    ap.add_argument("--fail-on", choices=["high", "review", "never"], default="high",
                    help="lowest severity that makes the exit code 1 (default: high)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args(argv)

    if args.no_diff and not args.report:
        ap.error("--no-diff needs at least one --report")
    repo_given = args.repo is not None
    args.repo = args.repo or "."

    findings: list[Finding] = []
    meta = {"diff": None, "files": 0, "added": 0, "removed": 0, "reports": args.report,
            "head_sha": None}
    try:
        # The provenance check needs the commit the reports describe: the scanned head, or in
        # --no-diff mode only a repo named explicitly (the shell's cwd may be any repo at all).
        # A working tree has no commit for a report to name.
        if not args.worktree and (not args.no_diff or repo_given):
            meta["head_sha"] = git(args.repo, "rev-parse", "--verify",
                                   f"{args.head}^{{commit}}").strip()
        if not args.no_diff:
            scanner, label = scan_repo(args.repo, args.base, args.head, args.worktree,
                                       args.include_docs)
            findings.extend(scanner.findings)
            meta.update(diff=label, files=len(scanner.files), added=scanner.added,
                        removed=scanner.removed)
        for report in args.report:
            findings.extend(scan_report(report, meta["head_sha"]))
    except RuntimeError as exc:
        print(f"slop_scan: {exc}", file=sys.stderr)
        return 2

    order = {"high": 0, "review": 1, "info": 2}
    findings.sort(key=lambda f: (order[f.severity], f.category, f.where))
    counts = {s: sum(1 for f in findings if f.severity == s) for s in ("high", "review", "info")}

    if args.json:
        print(json.dumps({"meta": meta, "counts": counts,
                          "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        if meta["diff"]:
            print(f"slop-scan  {meta['diff']}  ({meta['files']} files, "
                  f"+{meta['added']} -{meta['removed']})")
        for report in args.report:
            print(f"report     {report}")
        if not findings:
            print("no findings")
        for f in findings:
            note = f"  [{f.note}]" if f.note else ""
            print(f"{f.severity:<6}  {f.category:<17} {f.where}\n        {f.text}{note}")
        print(f"summary: {counts['high']} high, {counts['review']} review, "
              f"{counts['info']} allowed. Every hit is a lead to read, not a verdict.")

    threshold = SEVERITY_RANK[args.fail_on]
    worst = max((SEVERITY_RANK[f.severity] for f in findings), default=-1)
    return 1 if worst >= threshold else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
