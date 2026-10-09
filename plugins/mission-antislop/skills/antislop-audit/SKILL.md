---
name: antislop-audit
description: Read-only completeness and evidence audit of an unattended agent run, done before its correctness review. Given the brief, the completion report (DONE file, PR body) and the branch diff, it rebuilds the scope ledger from the brief and reconciles every row against claimed evidence and the actual diff. It then checks the evidence itself: every green figure is tied to the head commit and the suite really ran; each test cited as proof fails under a named wrong implementation; every sweep claim survives its search rerun wider; repair rounds closed the defect class and created no new one; shipped prose claims no more than the code does. It runs a deterministic slop scan, catches buried losses and dumped follow-ups, and returns COMPLETE, COMPLETE WITH DECLARED GAPS, or INCOMPLETE, with a return-to-agent list and the claims a correctness reviewer should try to falsify. Triggers on "audit this mission's DONE file", "is this run actually complete", "check the completion report against the brief", "are these proofs real", "did the agent cut corners", "antislop audit", "slop scan this branch", "audit this repair round". NOT a full correctness or security review (pair it with an adversarial review), NOT for checking a brief before launch (use antislop-brief), NOT for the executing agent's own self-check (antislop-execution covers that).
---

# Anti-slop audit

A completion report is the agent describing its own work, not proof that the work is ready.
In the review record behind this plugin (`${CLAUDE_PLUGIN_ROOT}/docs/Mission slop.md`),
about four in five of the defects a repair round had to fix were missing from the mission's
own report. The most common were evidence defects:

- overclaiming prose;
- tests a wrong implementation passes;
- green figures from a stale log or the wrong commit;
- sweeps whose scope made them pass;
- fixes that closed the cited line but not the class.

This audit checks completeness and evidence, cheaply, before an expensive correctness
review. It then hands that review the specific claims worth falsifying.

Read-only throughout. Patterns and IDs: `${CLAUDE_PLUGIN_ROOT}/docs/Slop patterns.md`.

## Inputs

- The **brief**: the authoritative scope. For a repair round, also the review it answers.
- The **completion report** and **PR body**, plus the agent's ledger if it kept one.
- The **repo** and the **base…head** range: the branch against its merge base.
- The **follow-ups file**, if the run wrote one.

If something is missing, say which input, and audit what you have. Without the brief there
is no scope to reconcile against, so report that instead of guessing.

## Label every check

Mark each check in your output **[executed]** (you ran a command or a test) or **[static]**
(you reasoned from reading). Reviews in the record often asserted things they never ran. Be
the exception, and say which is which.

## Procedure

### 1. Gather cheap [executed]

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/slop_scan.py" --repo <repo> --base <base> --head <head> \
  --report <completion-report.md> --report <pr-body.md>
git -C <repo> diff --stat <base>...<head>
git -C <repo> rev-parse --short <head>
```

The scanner is deterministic, and every hit is a lead, not a verdict:

- **Added lines:** placeholders, skipped or focused tests, swallowed errors, suppressions,
  type escapes, and sweep claims in docs and changesets.
- **Removed lines:** test assertions, loosened matchers, deleted test files.
- **The reports:**
  - `sweep-claim`: the claims to verify in step 5;
  - `green-provenance`: test figures, with the head commit named nowhere in the report;
  - handoffs, elisions, unproven and blanket claims.

`allowed` lines are exemptions the author granted themselves. Read them too.

### 2. Rebuild the ledger from the brief yourself

Build it the same way antislop-execution does: one row per deliverable or clause, compound
clauses split, each row with the brief line it comes from. Build yours before you read the
agent's ledger, then diff the two. A row the agent never listed is the clearest sign that
scope shrank without anyone deciding it.

### 3. Reconcile every row

Give each row exactly one status, citing the diff hunk (`file:line`) and the report section
it rests on:

| status | meaning |
|---|---|
| `PROVEN` | Diff hunks implement it, and the evidence passes step 4. |
| `CLAIMED` | The report says done, but the evidence is missing, can't fail, or comes from another commit. |
| `PARTIAL-DECLARED` | The report says partial, names what remains, and the PR body says so too. |
| `PARTIAL-SILENT` | Only part of the clause was delivered (often the weaker half of "X and Y"), and nothing says so. |
| `MISSING` | No claim and no diff. |
| `DEFERRED-AUTHORISED` | Deferred, quoting a brief line that allows it. |
| `DEFERRED-UNAUTHORISED` | Deferred with no brief line behind it. |
| `REFUTED` | The report shows, with evidence, that the brief's premise is false on the base; nothing was changed for it. |
| `GATED` | Stopped at a gate the brief names, with a decision memo. A gate the agent ruled on itself is not `GATED`. |

### 4. Audit the evidence

Walk every claim in the report that carries evidence.

- **Green provenance.** Every pass or fail figure quotes a log, the command, and a commit
  equal to the head. Check the suite really ran: the scheduled task count, the skipped
  count, no cache hit, no stop at the first red, no "build failed so tests were skipped".
  A figure from an earlier commit, or with no commit, is `CLAIMED` until re-run. Re-run it
  yourself if you are allowed to run tests [executed]. A red called "baseline" must be red
  on the base revision.
- **Tests that can fail.** For the two or three tests the report leans on most:
  - name the plausible wrong implementation;
  - check the test builds the production composition, not a hand-made one;
  - check its fakes and fixtures match what the real producer emits;
  - check it doesn't mock the seam it claims to prove.

  If you may run tests, execute the wrong implementation and confirm red: break the logic,
  and also **delete the wiring call** [executed]. Otherwise reason from the assertion and
  label it [static]. A report whose only mutation was "revert the hunk" has proven
  reachability, not the property.
- **Edge classes.** Compare the brief's named classes (case, Unicode, time zone, OS, EACCES
  vs ENOENT, concurrency, crash between steps, re-runs) with the tests. An unnamed class the
  code obviously touches is a finding even if the brief was silent. Raise it as a brief
  defect as well (antislop-brief S5).
- **Unknown vs success.** Each new error path keeps refused, indeterminate and success
  apart. Retries retry. Rollbacks check.

### 5. Audit the claims in shipped prose

Shipped prose means the PR title and body, commit messages, changesets, docs, help and
remedy strings, and comments in the diff. Take every scanner `sweep-claim`, plus any universal
claim the scanner missed:

- **Re-run the sweep wider** [executed]: every repo or package, case-insensitive,
  multiline, generated clients, docs that quote the string. A sweep whose stated scope is
  what makes it pass is `CLAIMED`.
- **Comments and docs** that describe behaviour must match the code. Check every place the
  claim is repeated, because corrections often land at the top and not in the table row
  that repeats them.
- **Disclosures** (partial rows, behaviour changes, widened inputs) must be in the PR body
  or commit, not only in the completion report.
- **The headline status** must match the ledger. "Status: complete" over a buried loss is a
  finding.

### 6. Repair rounds: class and delta

If this run answers a review:

- **Class.** For each finding, did the fix enumerate the class (producers, consumers,
  sibling rows, branches, packages) with a search, scope stated? Re-run that search
  [executed]. Same-class sites still open are `CLAIMED` for that finding.
- **Delta.** Review what the fix itself makes reachable: fail-open where it used to fail
  closed, secrets in a new error message, double application on retry, a claim "corrected"
  into more files. Fixes are where the next round's blocker usually comes from.

### 7. Check the follow-ups and severity

- **Dumped follow-ups.** Compare each follow-up item with the ledger. If it is a ledger
  row, it was dumped. This is rare, but check every item; a phrase grep mostly finds honest
  reporting.
- **Softened severity.** Every "pre-existing" or "not this PR's defect" must be shown on the
  base revision. Otherwise it belongs to this run.

### 8. Triage the scan hits

Classify every `high` hit as **real**, **justified** (the line or the brief says why), or
**false positive** (say why). Read the `review` hits quickly. A cluster of them in one file
usually marks the clause that was rushed.

### 9. Give the verdict

- `COMPLETE`: every row is PROVEN, REFUTED, DEFERRED-AUTHORISED or GATED; no `real` scan
  hit; no unbacked sweep claim; every figure is tied to the head.
- `COMPLETE WITH DECLARED GAPS`: as above, plus PARTIAL-DECLARED rows the PR body is honest
  about. Ready for review once someone accepts the gaps.
- `INCOMPLETE`: any of these:
  - a CLAIMED, PARTIAL-SILENT, MISSING or DEFERRED-UNAUTHORISED row;
  - an open same-class site in a repair round;
  - a dumped follow-up;
  - a buried loss;
  - a `real` high hit.

  It goes back to the agent before any correctness review.

## Output

```
AUDIT: COMPLETE | COMPLETE WITH DECLARED GAPS | INCOMPLETE — <counts by status>
head: <sha> · executed checks: <n> · static checks: <m>

Ledger reconciliation (M rows from <brief>; agent's ledger: N rows, <diff vs mine>)
| id | brief says | status | diff | evidence | [executed]/[static] | note |

Evidence audit
| claim (report §) | provenance (commit?) | can it fail? (wrong impl named / run) | verdict |

Shipped-prose claims
| claim (where) | backing (search + scope / test) | rerun wider? | verdict |

Repair round (if any): <finding → class enumerated? → sites still open → new reachable state>
Scan triage: <k> high (<real / justified / false positive>), <j> review read.
Follow-ups dumped: <list or none>. Severity softened: <list or none>.

Return to agent (if INCOMPLETE), one line per item, written as the defect brief:
- C4 PARTIAL-SILENT: the brief requires X and Y; only X landed — <where Y should land>.

Claims for the correctness reviewer to falsify (quoted, not paraphrased):
- "<central claim>" (PR body §…) — <the evidence that would refute it>.
```

The last section is the handoff to the reviewer. Quote the claims exactly, because a
paraphrase lets a reviewer falsify a claim the author never made.
