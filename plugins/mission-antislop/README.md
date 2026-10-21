# mission-antislop

Anti-slop skills for **long-horizon agent missions**: work an agent runs unattended from a
written brief, reports on in a completion file, and hands to an independent review.

Slop here is work that looks done and isn't. Mostly it looks *proven* and isn't:
- a test a wrong implementation would pass;
- "all tests pass" copied from a log of an earlier commit;
- "no remaining callers", proven by a search scoped to one package;
- a fix that closes the cited line and leaves the same bug one row over;
- a PR body claiming more than the code does.

## Where this comes from

It started from taste-skill's
[`output-skill`](https://github.com/Leonxlnx/taste-skill/tree/main/skills/output-skill) and its
[laziness research](https://github.com/Leonxlnx/taste-skill/tree/main/research/laziness),
which fight placeholder code and truncation inside a single response. Then it was checked
against a real review record: about 350 independent adversarial verdicts on about 120
unattended missions.

The record turned the emphasis around. Placeholders appeared in about 14 units, premature
stops in none, and follow-up dumping in 4 of about 620 items. The common failures were
evidence slop:

- overclaiming prose (~115);
- tests that can't fail (~88);
- happy-path only (~85);
- false green (~64);
- incomplete sweeps (~63);
- swallowed errors (~62);
- narrow fixes (~61);
- fixes that create the next defect (≥30).

The mission's own report missed about four in five of them.

So the output-skill rules stay as a floor, but most of the weight is on whether each piece
of evidence could have failed. See [`docs/Mission slop.md`](docs/Mission%20slop.md).

Codebase-neutral: nothing assumes a language, framework or orchestrator. No agents.

## The lifecycle

| Stage | Skill | Does | Fires on |
|---|---|---|---|
| Before launch | `antislop-brief` | Reads the brief as the executing agent would and rebuilds the scope ledger. Runs 16 substance checks: the premise holds on the base; every prescribed proof can fail; properties not mechanisms; invariants and edge classes named; countable scope; deferral needs authority; gates exist; no dictated conclusion; repair briefs sweep the class. Each fail comes with the replacement line. | "check this brief for slop", "harden this brief", "check this fix-up brief" |
| During the run | `antislop-execution` | The worker's discipline. Verifies the premise and locks scope into an on-disk ledger, then requires evidence that can fail: a named wrong implementation killed (including a deleted wiring call), every figure tied to the head commit, sweeps printed with their scope, the class fixed rather than the line, edge classes named, unknown kept apart from success, disclosures in the PR body. Honest `X of Y` over an inflated done. | "run this mission", "execute this fix-up round", "make the proofs real" |
| Before review | `antislop-audit` | Rebuilds the ledger from the brief and reconciles every row (PROVEN / CLAIMED / PARTIAL-SILENT / MISSING / …). Checks green provenance, reruns sweeps wider, confirms tests fail under a wrong implementation, checks repair rounds for open same-class sites and new reachable state, and audits shipped prose. Labels every check executed or static, and hands the correctness reviewer quoted claims to falsify. | "audit this mission's DONE file", "are these proofs real", "audit this repair round" |

The **scope ledger** ties the three together:
- the brief check builds it to see whether the brief can be counted;
- the worker builds it at step 0 and keeps it on disk through compactions;
- the audit rebuilds it from the brief and compares it with the worker's copy.

A row the worker never listed is the clearest sign of scope that shrank without anyone
deciding it.

## The scanner

`scripts/slop_scan.py` is deterministic, stdlib-only Python 3. The worker runs it as a
self-check and the audit runs it as its cheap first pass.

```bash
python3 scripts/slop_scan.py --base origin/main --head HEAD --report DONE.md --report PR-BODY.md
python3 scripts/slop_scan.py --base origin/main --worktree      # include uncommitted + untracked
python3 scripts/slop_scan.py --no-diff --report DONE.md --json  # wording only
```

| Looks at | Categories |
|---|---|
| Lines a diff adds (code) | `placeholder`, `marker`, `deferral`, `skipped-test`, `swallowed-error` (an empty catch with no stated reason is `high`; one with a reason is `review`), `suppression`, `type-escape` |
| Lines a diff adds (docs, changesets) | `sweep-claim` |
| Lines a diff removes (tests) | `assertion-removed`, `assertion-loosened`, `test-deleted` |
| Completion reports, PR bodies | `sweep-claim`, `green-provenance` (test figures, head commit named nowhere), `blanket-green`, `unproven-claim`, `out-of-scope`, `handoff`, `elision` |

Exit codes are `0` (clean at `--fail-on`, default `high`), `1` (findings) and `2` (usage or
git error). A `slop-scan: allow` pragma doesn't hide a line; the line is listed under
`allowed` so a reviewer still sees it.

**Calibration.**
- *Diff rules:* about 30k merged, reviewed lines. `high` fired once, on a promise-queue
  keep-alive, which is a fair lead.
- *Report rules:* about 33k lines of real completion reports and PR bodies. Zero `high`
  hits, and about 1.3 claims per report to check. Wording rules that mostly fired on honest
  reporting were cut: "recorded as a follow-up", "partially refuted", "stubbed client".
  Deferral is judged by reconciling follow-ups against the brief, not by grepping for the
  word.

Every hit is a lead to read, not a verdict.

`green-provenance` needs to know the head commit, so it runs only when scanning a diff, or
when `--no-diff` is given an explicit `--repo`. It checks that the head SHA is named, not
that every figure was run there. A report that names a stale SHA needs the audit's step 4.

## Tests

```
python3 tests/selftest.py
```

The self-test runs the scanner's own command line against throwaway git repositories and
report files, and proves that each rule row and each category the scanner emits flags a line
it must flag, with its severity and `path:line`, and leaves a near-miss alone. It reads the
rule tables from the code, so a rule added without cases fails it. It also confirms:

- the exit codes: `0`, `1` at or above `--fail-on`, and `2` for a usage or git error, with
  the cause on stderr;
- the `--json` shape, with counts that match the findings;
- a `slop-scan: allow` line is listed under `allowed` on code, doc and report lines;
- the category table above names exactly the code's categories.

The git it runs never reads your git config. Fifty-three mutations each make it fail. They include
breaking each rule's pattern, dropping the pragma listing, shifting an exit code and
renaming a category.

## Validation

Both review skills were blind-tested on archived missions whose review outcome was already
known. They ran headless, with read-only tools, and the prompt gave no hint of the answer.

- **`antislop-brief`**, given a brief cold, flagged the exact prescribed proof that a later
  review called tautological. Its finding: the fake runner "has the fix built in", so the
  proof re-proves the fix rather than the behaviour. It found two more proofs in the same
  brief that couldn't fail.
- **`antislop-audit`**, given only a brief and a round-0 completion report, returned
  INCOMPLETE. It marked the report's "zero new failures, repo-wide" as CLAIMED, because the
  suite run it cited had not finished. A later review independently established that.

  The audit also caught:
  - a pasted test run that exercised code the report said was removed;
  - a brief-required row filed as a follow-up;
  - a "Status: complete" headline sitting over two unauthorised deferrals.

## Docs

- [`docs/Mission slop.md`](docs/Mission%20slop.md): the review-record findings, root causes
  adapted from the laziness research, which remedies transfer, which were left out and why,
  and notes on the sources.
- [`docs/Slop patterns.md`](docs/Slop%20patterns.md): the catalogue. Brief-side B1–B10,
  execution-side E1–E12, report-side R1–R6, each with a frequency band, a detection signal,
  and the skill or scanner rule that catches it.

## Layout

```
.claude-plugin/plugin.json
skills/
  antislop-brief/SKILL.md
  antislop-execution/SKILL.md
  antislop-audit/SKILL.md
scripts/
  slop_scan.py
tests/
  selftest.py
docs/
  Mission slop.md
  Slop patterns.md
README.md
```

## Install

```
/plugin install mission-antislop@marsman-io
```

(`marsman-io` is the marketplace's registered name, from `.claude-plugin/marketplace.json`.)

## Provenance

The framing and the single-response remedies are adapted from
[taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT, © 2026 Leonxlnx): banned-pattern
lists, scope count and cross-check, clean-breakpoint continuation, evidence before narrative,
verification loops.

The mission-scale patterns, their frequencies and the calibration come from one team's
review record of unattended missions. They appear here only as generalised patterns and
counts. Nothing is copied verbatim.

## License

MIT.
