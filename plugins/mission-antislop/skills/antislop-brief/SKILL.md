---
name: antislop-brief
description: Read-only substance check on a brief that an agent will run unattended (a mission prompt, a background-task spec, a long-horizon work order, or a fix-up brief after a review). It finds every spot where an agent could satisfy the words cheaply and miss the intent, and writes the replacement line for each. It rebuilds the scope ledger the agent will build, then checks: the premise holds on the base; every prescribed proof can fail; clauses state properties, not mechanisms; cross-cutting invariants and edge classes are named; scope is countable; deferral needs authority; gates exist; the brief dictates no conclusion; a repair brief sweeps the defect class. Use it after drafting a brief and before launch, alongside any structural linter. Triggers on "check this brief for slop", "is this mission prompt slop-proof", "harden this brief", "will an agent cut corners on this spec", "antislop the brief", "tighten the acceptance criteria before launch", "check this fix-up brief". NOT a structural or template-compliance linter (it checks what the sections say, not whether they exist), NOT for auditing finished work (use antislop-audit), NOT for interactive tasks where the user is present to steer.
---

# Anti-slop brief check

Much mission slop is decided before launch. In the review record behind this plugin
(`${CLAUDE_PLUGIN_ROOT}/docs/Mission slop.md`), several of the costliest runs trace straight
to their briefs:

- a prescribed proof that could not fail;
- a mechanism prescribed instead of a property, then bypassed by the case it never named;
- a function the brief named that did not exist on the base;
- an instruction to *claim* the change was safe to merge;
- a one-line spec, and a bundle of about eight deliverables, which took six and eleven
  review rounds.

The cleanest runs had briefs that required reproducing the problem on the base first,
targeted one seam, and named the wrong implementation each proof had to kill.

A structural linter asks whether the sections are there. This skill asks whether they say
anything an agent cannot satisfy cheaply. A brief can pass every structural check and fail
all of these. The patterns are in `${CLAUDE_PLUGIN_ROOT}/docs/Slop patterns.md` § Brief-side.

## Procedure

### 1. Read the brief as the executing agent

Read the brief and everything it pulls in: its template, the inputs it names, the contract
or ADR it cites, and for a fix-up brief, the review it answers. Read for loopholes, not
intent. When a sentence has two readings, the agent takes the one that is less work.

### 2. Rebuild the scope ledger

Build the ledger the executing agent will build (antislop-execution step 0): one row per
deliverable or clause, in the brief's words, with the line it comes from. Split compound
clauses ("X and Y") into rows, because the weaker half is the one that ships alone.

- If you cannot number the deliverables, the brief fails **S2**. Report that first, because
  nothing downstream can be checked.
- Write the count. A single-owner ledger over about 12 rows, or rows that share no seam,
  is probably two briefs (**S12**).

### 3. Verify the premise on the base

Where you have the repo, check that every symbol, path, flag and command the brief names
exists and behaves as stated on the base revision (`git grep`, `git show <base>:<path>`). A
bug the brief asserts should be reproducible there. Anything that doesn't resolve is an
**S14** fail. If you can't check it, the brief must make the agent check it first ("verify
on the base before changing anything; if it is not real, say so with evidence and change
nothing for it").

### 4. Run the substance checks

Decide **PASS** or **FAIL** for each check. Every FAIL quotes the brief's words and gives a
replacement line the author can paste. "Be more specific" is not a finding.

| # | Check | Fails when… | A passing line looks like |
|---|---|---|---|
| S1 | **Demonstrable done** | The goal is a direction ("improve", "support", "clean up"), not an end state someone can observe. | "Done = `tool sync --dry-run` on a workspace with a stale lock exits 3 and names the holder; shown in the report with its output and commit." |
| S2 | **Countable scope** | Deliverables can't be enumerated, or an open quantifier lets the agent choose the count: "etc.", "as needed", "where appropriate", "all relevant", "any necessary". | Every item named and numbered. "All callers" becomes the list, or the exact search (and its scope) that defines it. |
| S3 | **Properties, not mechanisms** | A clause prescribes *how* (a mechanism that can be delivered exactly and still bypassed), or uses a verb a wrong implementation also satisfies: handle, support, ensure, robust, properly, gracefully, clean, harden. | The guarantee, plus the input that breaks a wrong version: "No path outside the root is accepted, whatever its case, Unicode form or symlinks; a second writer gets `E_LOCKED` and the holder's bytes are unchanged." |
| S4 | **Each proof can fail** | The proof is "add tests" or "verify it works"; or it holds by construction (a check that passes only when the configuration it checks is present); or it is a mock of the seam under test; or it names no wrong implementation it must kill; or its mutation only nudges a threshold or constant (that proves the test reads the value, not that it pins the behaviour); or its fixtures sample only the cases the intended implementation already handles (a hunk revert can't expose a fixture class that was never there). | "Proof: a test through the production wiring with two real writers. It must go red under (a) the guard removed and (b) the wiring call deleted. Mutations executed, outputs in the report §C1." |
| S5 | **Invariants and edge classes named** | Nothing says unknown ≠ success, unreadable (EACCES) ≠ absent (ENOENT), or independence from time zone, letter case and OS. Concurrency, order independence, partial failure, re-runs and a crash between durable steps go unmentioned. Silence licenses the happy path. | Each class is required for a named clause or excluded by name: "Crash between steps 2 and 3: required (SIGKILL proof). Concurrency: excluded, single writer by design (ADR-12)." |
| S6 | **Deferral needs authority** | There's no explicit non-goals list, or nothing says only that list authorises deferral. Or there's no rule for defects found along the way that predate the change, so scope grows round after round, or shrinks, at whoever's suggestion comes last. | "Non-goals: X, Y. Anything not listed is in scope; a follow-up may hold only work outside the numbered clauses. A defect you find that predates this change: fix it here only if a clause depends on it; otherwise record it with `file:line` and evidence that it predates the change." |
| S7 | **No cheaper reading** | A phrase has two readings and one is less work: "update the docs" (one page, or every page quoting the string?), "add validation" (types, or runtime?), "migrate" (copy, or copy then delete?). | Choose the reading in the brief: "every doc quoting `--old-flag` (`git grep -n -- '--old-flag'` across all packages and docs)". |
| S8 | **Gates exist and stop rules are clear** | Gates aren't enumerated; or it says "no gates" with an irreversible step in scope; or it says "ask if unsure" (there is no one to ask); or it doesn't say what to do at a non-gate decision. | "Stops: G1 (irreversible migration), G2 (live infra). Every other decision: choose, mark `[intent]`, continue." A zero-gate brief says why none is needed. |
| S9 | **Partial contract** | It doesn't define how to report unfinished work, so the only shapes left are "done" and silence. | "If you stop early, report `X of Y` with each clause's status and the resume point. An honest partial is acceptable; an inflated done is not." |
| S10 | **Evidence format** | The proof format is unspecified, or "tests pass" is accepted without a command, counts, the commit, and the baseline. | "Per clause: command, output excerpt, and the commit SHA it ran at (the final head). Test results as counts against the named baseline reds, never 'all green'. Every sweep claim prints its search and scope." |
| S11 | **No template residue** | Unfilled `<…>`, `TBD`, `???`, author-facing comments, or contradictory instructions (template text left beside the real one). | Fill or delete it. Resolve contradictions in the brief. |
| S12 | **Size fits one run** | Too many rows for the budget, rows bundled across unrelated seams, or a spec too thin to number. Late rows become stubs; thin specs reopen scope every round. | One seam per brief. Split the bundle, or order the rows and say which may be `partial` if the budget runs out. |
| S13 | **Settled decisions listed** | Design choices already made aren't stated, so the agent re-opens them, or quietly picks the cheaper architecture. | "Settled, don't re-open: single-writer lock file (ADR-12); no schema change." |
| S14 | **Premise holds on the base** | A named symbol, path, flag or command doesn't exist on the base, or the asserted bug doesn't reproduce there (step 3). | Correct the name. Or: "Step 0: reproduce on the base with `<command>`; if it does not reproduce, write that up with evidence and stop this clause." |
| S15 | **No dictated conclusion** | The brief tells the agent what to *conclude* or claim ("say it is safe to merge", "state there are no regressions") rather than what to *show*. | "Show the evidence for each clause. Merge readiness is decided by review, not stated by the author." |
| S16 | **Repair briefs sweep the class** | A fix-up brief lists the reviewer's cited lines but not the defect classes, so the repair closes exactly those lines. Or it doesn't ask what new state the fix makes reachable. | "For each finding: name its class, enumerate every producer and consumer with `<search>` (scope stated), fix all sites or list the ones left, and say what the fix newly makes reachable." |

### 5. Spot-check the catalogue

Skim `docs/Slop patterns.md` § Brief-side for anything the checks didn't catch, such as a
proof that can only be shown through an internal call, or a "verify" step with no
observable output. Add those as findings.

## Output

```
BRIEF: SLOP-PROOF | NEEDS REWRITE — N fails

Ledger preview (M rows): C1 <…> · C2 <…> · …
Premise on base: <checked: all resolve | S14 fails: … | not checked: no repo>

| check | verdict | brief says | replace with |
|-------|---------|------------|--------------|
| S4    | FAIL    | "add a test that the runner is healthy with the flag set" (§5 C2) | "test must go red when the flag is dropped AND when the runner ignores it; mutations executed" |
| …     |         |            |              |
```

End with the three fails most likely to produce slop, ranked by how much work the cheap
reading would skip. This check is read-only by default; apply the rewrites only when asked.
