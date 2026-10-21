#!/usr/bin/env python3
"""Re-apply every `regex` grader of a `claude plugin eval` run to the text the
run recorded, and compare each verdict with the CLI's.

  replay_graders.py <aggregate-result.json> [--kept DIR] [--mutate]

For each case, arm and run in the result: the grader's `target` text is rebuilt
the way the CLI builds it (2.1.305) — `trace`: the run's trace.jsonl, one JSON
event per line; `{source: file, path}`: that file in the run's sandbox cwd —
and the grader's `pattern`, `flags` and `match` are applied (JavaScript RegExp
semantics: `\\w`, `\\d`, `\\b` are ASCII; `count:N` counts global matches).
`last_message`, `files` and `mock_calls` targets are reported as `skipped`
(this suite has none). The run's files come from the sandbox the CLI kept
(`--keep-temp`; unseal it first with the `chmod 700` its notice names), or with
`--kept DIR` from a copy laid out DIR/<case>/<arm>-<n>/{trace.jsonl,cwd/}.

Prints one line per grader per run and `compared N, agreeing M`. Exit 0 only
when N > 0 and N == M; 1 on any disagreement (the replay is then wrong, not the
grader); 2 when nothing could be compared.

--mutate: for every regex verdict the CLI passed, break the text in memory —
delete every match (`contains`), delete one match (`count:N`), or insert the
offending text from replay_breaks.json (`not_contains`) — and re-run the
grader: it must fail; on the original text it must pass again. Exit 1 when
any break stays green. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BREAKS = HERE / "replay_breaks.json"
JS_FLAGS = {"i": re.I, "m": re.M, "s": re.S}


def compile_js(pattern: str, flags: str) -> re.Pattern:
    f = re.ASCII
    for ch in flags:
        if ch in JS_FLAGS:
            f |= JS_FLAGS[ch]
        elif ch != "g":
            raise ValueError(f"flag {ch!r} has no Python equivalent in this replay")
    return re.compile(pattern, f)


def verdict(cfg: dict, text: str) -> tuple[bool, str]:
    rx = compile_js(cfg["pattern"], cfg.get("flags", ""))
    match = cfg.get("match", "contains")
    if match == "contains":
        ok = rx.search(text) is not None
        return ok, "matched" if ok else "pattern not found"
    if match == "not_contains":
        ok = rx.search(text) is None
        return ok, "pattern absent as expected" if ok else "pattern found (expected absent)"
    if match.startswith("count:"):
        n = sum(1 for _ in rx.finditer(text))
        return n == int(match[6:]), f"found {n} matches (expected {match[6:]})"
    return False, f"unknown match mode {match!r}"


def break_text(name: str, cfg: dict, text: str, breaks: dict) -> str | None:
    rx = compile_js(cfg["pattern"], cfg.get("flags", ""))
    match = cfg.get("match", "contains")
    if match == "contains":
        return rx.sub("", text)
    if match.startswith("count:"):
        m = rx.search(text)
        return text[:m.start()] + text[m.end():] if m else None
    if match == "not_contains":
        return text + "\n" + breaks[name] if name in breaks else None
    return None


class Run:
    def __init__(self, case: str, arm: str, i: int, rec: dict, kept: Path | None):
        self.case, self.arm, self.i, self.rec = case, arm, i, rec
        if kept is not None:
            base = kept / case / f"{arm}-{i}"
            self.trace, self.cwd = base / "trace.jsonl", base / "cwd"
        else:
            self.trace = Path(rec.get("tracePath") or "/nonexistent")
            root = self.trace.parent.parent
            sealed = root / "sealed" / "home" / "cwd"
            self.cwd = sealed if sealed.exists() else root / "home" / "cwd"

    def text(self, target) -> str | None:
        """The grader's target text, or None when the CLI would have thrown (file missing)."""
        if target == "trace":
            lines = []
            for line in self.trace.read_text(encoding="utf-8").splitlines():
                try:
                    json.loads(line)
                except ValueError:
                    continue  # the CLI keeps only lines that parse
                lines.append(line)
            return "\n".join(lines)
        if isinstance(target, dict) and target.get("source") == "file":
            f = self.cwd / target["path"]
            if not f.is_file():
                return None
            return f.read_bytes().decode("utf-8", errors="replace").lstrip("﻿")
        raise KeyError(target)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("result", type=Path)
    ap.add_argument("--kept", type=Path)
    ap.add_argument("--mutate", action="store_true")
    a = ap.parse_args(argv)
    result = json.loads(a.result.read_text(encoding="utf-8"))
    breaks = json.loads(BREAKS.read_text(encoding="utf-8")) if BREAKS.exists() else {}

    compared = agreeing = skipped = 0
    broken = stayed_green = restored_bad = 0
    for case in result["cases"]:
        regex = {g["name"]: g["config"] for g in case["graders"] if g["type"] == "regex"}
        for arm, runs in case.get("arms", {}).items():
            for i, rec in enumerate(runs, 1):
                run = Run(case["name"], arm, i, rec, a.kept)
                cli = {g["name"]: g for g in rec.get("graders", [])}
                for name, cfg in regex.items():
                    where = f"{case['name']} {arm}-{i} {name}"
                    if name not in cli:
                        continue  # not run in this arm (with-only) or the run errored
                    target = cfg.get("target", "last_message")
                    if not (target == "trace" or isinstance(target, dict)):
                        skipped += 1
                        print(f"skip  {where}: target {target} is not replayed")
                        continue
                    try:
                        text = run.text(target)
                    except OSError as e:
                        skipped += 1
                        print(f"skip  {where}: cannot read the run's files ({e}); unseal the kept sandbox or pass --kept")
                        continue
                    ok, why = (False, "file missing (the CLI throws)") if text is None else verdict(cfg, text)
                    cli_ok = bool(cli[name]["passed"])
                    compared += 1
                    agree = ok == cli_ok
                    agreeing += agree
                    print(f"{'agree' if agree else 'DIFFER'} {where}: cli {'PASS' if cli_ok else 'FAIL'}, "
                          f"replay {'PASS' if ok else 'FAIL'} ({why})")
                    if a.mutate and ok and cli_ok and text is not None:
                        bad = break_text(name, cfg, text, breaks)
                        if bad is None:
                            print(f"  break {where}: no break defined (add it to replay_breaks.json)")
                            stayed_green += 1
                            continue
                        b_ok, b_why = verdict(cfg, bad)
                        r_ok, r_why = verdict(cfg, text)
                        broken += 1
                        stayed_green += b_ok
                        restored_bad += not r_ok
                        print(f"  break {where}: {'STAYED GREEN' if b_ok else 'red'} ({b_why}); "
                              f"restored: {'green' if r_ok else 'RED'} ({r_why})")
    print(f"compared {compared}, agreeing {agreeing}, skipped {skipped}")
    if a.mutate:
        print(f"broken {broken}, stayed green {stayed_green}, restore failed {restored_bad}")
    if compared == 0:
        return 2
    return 0 if agreeing == compared and not (a.mutate and (stayed_green or restored_bad)) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
