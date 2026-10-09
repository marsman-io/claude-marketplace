---
name: antislop-execution
description: Working discipline for an agent executing a brief unattended over a long horizon (a mission, a background run, a multi-hour task, a fix-up round after review) so the result is proven rather than proven-looking. It locks scope into an on-disk ledger before the first edit. It makes every piece of evidence able to fail: mutations that kill a named wrong implementation, every green figure tied to the head commit, every sweep claim printed with its search and scope. It fixes defect classes rather than cited lines, names edge classes, keeps unknown apart from success, bans placeholders and evidence-free wording, and makes an honest "5 of 7, here is what is left" the acceptable way to stop short. Load it at step 0 of any unattended run. Triggers on "work through this brief unattended", "run this mission", "execute this fix-up round", "don't ship half-finished work", "make the proofs real", "finish every clause", "anti-slop execution". NOT for interactive pair work where the user is present to steer, NOT for writing or checking the brief (use antislop-brief), NOT for auditing someone else's finished run (use antislop-audit).
---

# Anti-slop execution

An unattended run fails quietly, and mostly not by leaving work visibly unfinished. In the
review record behind this plugin (`${CLAUDE_PLUGIN_ROOT}/docs/Mission slop.md`), the common
failures were *evidence* that looked like proof:

- prose claiming more than the code does;
- tests a wrong implementation would pass;
- green figures from a stale log or the wrong commit;
- sweeps whose search scope is what made them pass;
- fixes that closed the cited line but not the bug class;
- repairs that created the next blocker.

The mission's own report missed about four in five of these; an independent reviewer found
them, a round later. Placeholders and premature stops were the rare tail.

These are trained defaults, not limits: tutorial-shaped tests, stopping pressure that turns
into declaring done early, and the urge to make red go away rather than report it. The
rules below replace those defaults. Each one exists because the default cost a review
round.

## Step 0: verify the premise, lock the scope

**Verify before fixing.** Check that every symbol, path and command the brief names exists
on the base, and reproduce any bug it asserts. If a premise is false, the row is `refused`:
write down the evidence and change nothing for it.

**Build the scope ledger** and keep it on disk. It is the memory that survives compaction,
restarts and long runs.

- **Where.** In a file beside the completion report, such as `LEDGER-<slug>.md`, or
  wherever the brief says. Never in the completion report itself: some controllers treat
  that file's appearance as "done".
- **Rows.** One row per deliverable or clause, in the brief's words, with the line it comes
  from. Use the brief's IDs (C1, C2, …). Split compound clauses: delivering the weaker half
  of "X and Y" and calling it done is the commonest silent shrink.
- **Count.** `locked: N rows from <brief> @ <sha>` at the top. Only the brief adds rows.
  Work you discover goes under **Discovered**.
- **Ambiguity.** When the brief allows two readings, take the one that delivers more of its
  stated goal, and note it on the row as `[intent]` with one line of reasoning. Never settle
  toward less work without saying so.

```markdown
# Scope ledger — <brief>
locked: 7 rows from PROMPT-<slug>.md @ 3f2a9c1

| id | deliverable (brief's words) | from | status | evidence |
|----|-----------------------------|------|--------|----------|
| C1 | refuse a second writer with a typed error | §2 C1 | done | lock.test.ts:41; red under guard-removed AND wiring-deleted @ 9e1b2c4 |
| C2a | re-running after a crash converges | §2 C2 | partial | SIGKILL between steps 2–3 proven; 4–5 not yet |
| C2b | …and leaves no orphan lock | §2 C2 | todo | |

## Discovered (outside the brief; these go to follow-ups)
- <file:line>: <what, and why it is outside the ledger>
```

**Terminal statuses:**
- `done`: built, with evidence that would fail if the work were wrong.
- `partial`: built in part; the row says exactly what remains.
- `refused`: the premise is false on the base; evidence cited, nothing changed for it.
- `blocked-at-gate`: hit a named stop; memo written; other rows carried on.
- `deferred-by-brief`: quote the line.

You are not finished while any row is `todo` or `in-progress`.

## The work loop: one row at a time

For each row: implement, prove, record, mark. Then the next row. Don't build everything and
test at the end. That is how runs finish with ten clauses implemented, three proven, and a
report that says "all tested".

## Evidence that can fail

These rules target the failures the record shows most. Apply them to every row.

1. **Name the wrong implementation, then kill it.** Before writing a test, write down the
   plausible wrong implementation: "also deletes the unstamped disks", "matches the path
   case-sensitively", "never calls the guard because the wiring was dropped". The mutation
   is that wrong implementation, and you run it. Watch red, then restore.
   - "Revert the hunk" proves the hunk is reachable, not that the test pins the property.
   - Nudging a threshold or a constant proves the test reads that value, nothing more.
   - Fixtures must include the hostile cases (other spellings, the other platform's
     behaviour, inputs the implementation does not normalise), not only the ones it already
     handles. No mutation can expose a fixture class that was never there.
   - Always include **deleting the wiring call**.
   - Test through the **production composition**, not a hand-built one.
   - Fakes and fixtures must match what the real producer emits. A test that mocks the seam
     it claims to prove proves nothing.
2. **Every green names its commit.** Each pass or fail figure in the report quotes the log
   line and the command, and is run at the **final head**. Re-run after your last commit;
   never copy a figure forward from an earlier log. Confirm the suite actually ran:
   - the scheduled task count matches;
   - nothing was skipped by `skipIf` or served from cache;
   - the runner didn't stop at the first red;
   - no "build failed, so tests were skipped";
   - it isn't a typecheck that exits 0 on broken code.

   Compare counts to the known baseline reds. Show any red you call "baseline" red on the
   base revision.
3. **Sweeps print their search and its scope.** "No remaining X", "every caller", "nothing
   else" are claims. Back each one with the exact command and where it looked: all repos
   and packages, case-insensitive, multiline, generated code, docs that quote the string.
   Or narrow the wording to what you checked.
4. **Fix the class, not the line.** When you fix a defect, especially one a reviewer cited:
   - name its class;
   - enumerate every producer and consumer of the predicate with a search, scope stated;
   - fix every site, or list the ones left;
   - ask what state or path the fix newly makes reachable (fails open? leaks in the new
     error message? double-applies on retry?), because fixes are where the next blocker
     comes from.
5. **Name the edge classes.** For each clause that touches paths, time, processes or
   storage, cover each class or point to the brief line that excludes it:
   - letter case and Unicode form;
   - time zone;
   - the other OS;
   - permission-denied (EACCES) vs not-found (ENOENT);
   - concurrent runs;
   - a kill between durable steps;
   - re-runs.
6. **Unknown is not success.** Keep `refused`, `indeterminate` and `success` apart. An
   unreadable thing is not an absent thing. A retry that didn't retry, or a rollback that
   didn't check, must not report success.
7. **Disclose in the durable record.** Behaviour changes, widened inputs, `partial` and
   `refused` rows all go in the PR body or commit, which land. The completion report
   doesn't land.

## Never put these in the diff

Most of these are found by the scanner below.

- **Placeholders.** `TODO`/`FIXME` standing in for required behaviour; `// ...`; `// rest of
  the implementation`; `throw new Error("not implemented")`; `todo!()`; a hard-coded return
  where it should compute; a new field nothing reads.
- **Getting to green dishonestly.**
  - `.skip`, `.only`, `xit` or `#[ignore]`;
  - an exact assertion loosened (`toEqual` → `toBeDefined`, `==` → `>=`) or deleted;
  - a test deleted without a named replacement;
  - mocking the unit under test;
  - special-casing the test's input in product code.
- **Hiding failure.**
  - an empty `catch` or `except: pass` with no stated reason;
  - `.catch(() => {})`;
  - catch-and-return-a-default that makes failure look like success;
  - `|| true` on a step meant to work;
  - `as any` or a suppression to silence a check you could satisfy.
- **Structural shortcuts.**
  - a skeleton where the brief asked for the behaviour;
  - one worked case plus "the rest follow the same pattern";
  - a config flag in place of the behaviour itself.

When one of these is genuinely right (a real abstract method, a platform-conditional skip),
put the reason on the same line. The scanner's `slop-scan: allow` pragma still lists the
line for the reviewer.

## Never put these in the report or shipped prose

Shipped prose means PR body, commit messages, changesets, docs, help text and code comments.
Overclaiming there was the single most frequent finding.

| Pattern | Write instead |
|---|---|
| A universal or coverage claim ("every caller", "no X remains", "nothing else", "no regressions") with no enumeration behind it | The search and its scope, or an enumerating test, or narrower wording |
| A comment or doc describing behaviour the code lacks ("fails loudly", "is retried") | Make it true, or delete it. Fix every place that repeats the claim, not just the first |
| A pass/fail figure with no command and no commit | The command, its output, and the head SHA it ran at |
| "should work", "works as expected", "all tests pass", "fully tested" | Command, counts, baseline comparison, or mark it `[intent]` |
| "Status: complete" while a loss or gap sits further down | A headline that matches the ledger: `N of M done`, gaps named |
| A defect filed as "not this PR's problem" | Show it is pre-existing on the base revision, or own it |
| "Let me know if…", "and so on", "for brevity", "out of scope" without a brief quote | Do it, enumerate it, or quote the brief line that defers it |

## Only the brief can shrink scope

- "Out of scope" is a claim; its evidence is a quote from the brief.
- Follow-ups are for work outside the ledger. A ledger row can only reach a terminal status.
- A decision the brief didn't make that isn't a gate: choose, record `[intent]`, carry on.
  If it is irreversible or touches what the brief protects, it is a gate: write the memo
  and carry on with every row that doesn't depend on it. Never rule on a gate yourself.

## Stopping

- **Don't stop at a non-gate.** In an unattended run, questions have nowhere to go.
- **If you must stop early** (budget, context, or a gate that blocks everything left), stop
  at a clean breakpoint. Commit, update the ledger, and write the resume point at the top:
  `stopped: 5 of 7 rows terminal; resume at C6 (step 2: the SIGKILL proof)`. Never squeeze
  the remaining rows into stubs.
- **On resume or after compaction,** re-read the brief and the ledger before anything else.
  If committed progress exists, continue it. Don't restart.

## An honest partial is a good outcome

"5 of 7 done, C6 partial (here is what remains), C7 blocked at G1" costs the reader one
glance. "Done", when 5 of 7 are done, costs a full review round to discover, and after that
every claim in the report has to be re-checked. Reporting the gap is the job. Hiding it is
the failure.

## Before you write the completion report

1. **Scan your diff and your draft report.**
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/slop_scan.py" --base <base-ref> --head HEAD \
     --report <draft-report.md> --report <pr-body.md>
   ```
   Use `--worktree` instead of `--head HEAD` to include uncommitted and untracked files.
   - Fix every `high` hit, or justify it on the line.
   - Answer every `sweep-claim` with its search and scope, or narrow the wording.
   - A `green-provenance` hit means re-run the figures at the head and cite the SHA.
2. **Re-run the figures at the final head.** Paste the counts with the SHA.
3. **Reconcile the ledger.** The row count still equals the locked count, and every row is
   terminal. In the report, write `N of M done` with the breakdown by status.
4. **Verify each claim.** For every claim, write the question that would refute it ("would
   this test still pass with the wiring call deleted?"), answer it with a command, and paste
   the output. A claim you can't back becomes `[intent]` or is deleted.
5. **Put evidence before narrative.** Each clause's section opens with the command, the
   output and the commit. The prose comes after.
6. **Write the PR body from the head**, with every disclosure in it. Write the completion
   report last, because its appearance may be the done signal.

## Quick check

- The premise was verified on the base. The ledger was locked at step 0, the final row count
  equals the locked count, and every row is terminal.
- Each test cited as proof went red under a *named* wrong implementation, including a
  deleted wiring call, run through production wiring. The report says which mutations ran.
- Every figure names the head SHA, and the suite demonstrably ran.
- Every sweep claim carries its search and scope.
- Every fix lists the sites of its class and what it newly makes reachable.
- The scanner is clean at `high`, or each hit is justified on its line.
- Behaviour changes and gaps are in the PR body. The headline status matches the ledger.
