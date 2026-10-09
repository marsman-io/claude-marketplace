# Slop patterns

The catalogue the three skills share. There are three groups: patterns a **brief** lets in,
patterns in the **work and its evidence**, and patterns in the **completion report and
shipped prose**.

Each entry has:
- **Frequency:** a band from a review record of about 350 adversarial verdicts on about 120
  missions (see [`Mission slop.md`](Mission%20slop.md)). *Common* means about 50 or more
  units, *regular* 10–50, *rare* under 10.
- **Looks like:** a generic example.
- **Detect:** a signal you can check by reading or by command.
- **Caught by:** which skill or scanner rule catches it.

`scanner:` names a `slop_scan.py` category. `brief:Sx` names an `antislop-brief` check.

---

## Brief-side: slop decided before launch

### B1. Unprovable premise

*Regular.*

**Looks like:** the brief names a function, flag, file or bug that doesn't exist, or doesn't
behave that way, on the base revision. The agent "fixes" it anyway, or builds on it. A related
form: the brief prescribes a derivation that is itself wrong (an "empty" reason computed from
a set that wasn't the one searched). The mission does exactly what the brief says, and the
reviewer finds the brief's defect in the code.

**Detect:** every named symbol, path and command resolves on the base. Any bug the brief
asserts gets reproduced on the base before any fix.

**Caught by:** brief:S14; antislop-execution step 0 (verify before fixing).

### B2. A proof that can't fail

*Regular. This is among the costliest brief defects.*

**Looks like:** the brief prescribes a proof that holds by construction. For example, a
health check that passes only when the configuration it checks is present. Or a mocked
"success path calls X".

Strong briefs fall into this too. Some had reproduce-first rules, proof tables and mutation
rules, and still prescribed proofs at the wrong level:
- an ordering check ("the newer ranks first") for a scoring property;
- a mutation that nudges a threshold ("raise it to 1.01") or a constant ("set the prior to 1");
- fixtures that sampled only the equivalences the intended implementation computes, so a
  hunk revert could never expose the missing case.

**Detect:** for each prescribed proof, name the plausible wrong implementation. Then ask
whether the proof would stay green under it.

**Caught by:** brief:S4.

### B3. A mechanism instead of a property

*Regular.*

**Looks like:** the brief says how ("resolve both paths, then prefix-compare"), not what
("no path outside the root is accepted, whatever its spelling"). The mechanism is delivered
exactly and bypassed by the case it never named, here letter case.

**Detect:** clauses phrased as steps rather than as observable guarantees.

**Caught by:** brief:S3.

### B4. Unstated cross-cutting invariant

*Common through its downstream effects (E3, E6).*

**Looks like:** the brief never says "an unknown is not a success", "unreadable is not
absent", "independent of time zone, letter case and OS", "safe under concurrent runs" or
"order-independent". The agent builds the happy path.

**Detect:** the brief has no edge-class list, and no exclusion list either.

**Caught by:** brief:S5.

### B5. Uncountable scope

*Regular.*

**Looks like:** "update the docs", "all relevant callers", "handle edge cases as needed".
The agent chooses the count, and chooses low.

**Detect:** open quantifiers (etc., as needed, where appropriate, all relevant); clauses
that can't be numbered.

**Caught by:** brief:S2.

### B6. A cheaper reading available

*Regular.*

**Looks like:** "add validation" (types, or runtime too?), "migrate" (copy, or copy then
delete?), "fix the finding" (the cited line, or the class?).

**Detect:** for each verb, write down two readings. If one is less work, the brief has to
choose between them.

**Caught by:** brief:S7.

### B7. Dictated conclusion

*Rare, but severe.*

**Looks like:** the brief tells the agent what to claim: "say it is safe to merge in the PR
body". The agent complies, whatever the evidence says.

**Detect:** instructions about what the report should *conclude*, rather than what it
should *show*.

**Caught by:** brief:S15.

### B8. Missing or waived gates

*Rare.*

**Looks like:** "no human-attention gates in this mission" on work that has an
irreversible step. Or "ask if unsure" in an unattended run, where there is nobody to ask.

**Detect:** count the gates. A brief with zero gates states why none is needed.

**Caught by:** brief:S8.

### B9. Oversized or one-line brief

*Regular. These cost the most review rounds.*

**Looks like:** about 8 bundled deliverables (11 rounds in the record), or a one-sentence
spec (6 rounds). The late rows become stubs, or each round reopens the scope.

**Detect:** ledger size; whether the rows share a seam; whether a written brief exists at
all.

**Caught by:** brief:S12.

### B10. Repair brief scoped to the instance

*Common through its downstream effect (E7).*

**Looks like:** a fix-up brief that lists the reviewer's cited lines, not the defect
classes. The repair closes exactly those lines.

**Detect:** fix-up clauses that point at `file:line` without saying "and every other site
of this class, enumerated by <command>".

**Caught by:** brief:S16.

---

## Execution-side: the work and its evidence

### E1. Test that can't fail

*Common (~88). This is the second most frequent pattern.*

**Looks like:**
- the test mocks the seam it claims to test;
- a fixture doesn't match what the real producer emits;
- the "mutation" changes a constant the broken path never reads;
- the test builds a hand-made composition rather than the production one, so deleting the
  wiring call leaves it green.

**Detect:** name the plausible wrong implementation and execute it: break the logic, delete
the wiring call, swap the fake for the real producer's output. The test has to go red.
"Revert the hunk" proves the hunk is reachable, not that the test pins the property.

**Caught by:** antislop-execution (the evidence rules); antislop-audit step 4.

### E2. False green

*Common (~64).*

**Looks like:**
- a pass count copied from an earlier log or another commit;
- a suite that was skipped (`skipIf`), served from cache, cut off at the first red, or
  never scheduled;
- a typecheck or lint that exits 0 on broken code;
- "passed", inferred from a failure line that doesn't appear;
- a fix that isn't in the pushed branch.

**Detect:** each figure quotes a log whose header names the commit, and that commit is the
head. Confirm the suite ran: look at the scheduled task count and the skipped count.

**Caught by:** scanner:`green-provenance`, `blanket-green`; antislop-audit step 4.

### E3. Happy-path only

*Common (~85).*

**Looks like:** no test sets the time zone, varies letter case or Unicode form, runs on the
other OS, distinguishes permission-denied from not-found, runs two instances at once, or
kills the process between durable steps.

**Detect:** an edge matrix per clause. Each class is covered or explicitly excluded by the
brief.

**Caught by:** brief:S5; antislop-execution (the edge matrix).

### E4. Incomplete sweep

*Common (~63).*

**Looks like:** "no remaining references", proven by a grep limited to one package, case-
sensitive, single-line, or missing the generated client or the doc that quotes the string.

**Detect:** the report prints the search command and its scope. The auditor reruns it
wider: every repo, case-insensitive, multiline, generated code, docs.

**Caught by:** scanner:`sweep-claim`; antislop-audit step 4.

### E5. Swallowed error / unknown read as success

*Common (~62).*

**Looks like:**
- an empty catch;
- `.catch(() => null)`;
- `|| true`;
- only ENOENT handled, so EACCES reads as "absent";
- a retry that reports success without retrying;
- a rollback that prints "rolled back" and exits 0 without checking.

**Detect:** inject the failure (EACCES, a timeout, a partial write) and assert a distinct
outcome. Keep `refused`, `indeterminate` and `success` apart.

**Caught by:** scanner:`swallowed-error` (empty bodies with no stated reason are `high`);
antislop-execution.

### E6. Narrow fix

*Common (~61).*

**Looks like:** the reviewer's cited row is fixed, and the same defect is still one row,
branch or package over. One record took eight rounds on a single defect class.

**Detect:** for every fix, enumerate every producer and consumer of the predicate with a
search, and list them. The fix covers all of them, or the report names the ones left.

**Caught by:** antislop-execution (fix the class); antislop-audit step 4.

### E7. Fix creates a new defect

*Regular (≥30).*

**Looks like:** the repair fails open where the original failed closed; a restored error
path leaks a secret into its message; a "corrected" claim gets written into 66 files.

**Detect:** for each fix, ask what state or path it newly makes reachable. Review the delta,
not just the finding it closes.

**Caught by:** antislop-execution (fix the class); antislop-audit step 4.

### E8. Silent scope shrink

*Regular (~31).*

**Looks like:** a two-part clause where only the first part, often the weaker half, is
delivered and called done. Or the brief's letter is met but its intent isn't.

**Detect:** a clause-to-proof table. A row with fewer proven sub-items than its clause
names is flagged.

**Caught by:** the ledger (split compound clauses into rows); antislop-audit step 3.

### E9. Stubs, placeholders, dead fields

*Regular (~14).*

**Looks like:** `TODO` marking a skipped behaviour; `not implemented`; a schema field that
nothing reads; a placeholder left in the completion report itself.

**Detect:** scan the diff. For new fields, find a reader.

**Caught by:** scanner:`placeholder`, `marker`.

### E10. Test weakened

*Regular (~13).*

**Looks like:** `toEqual(x)` becomes `toBeDefined()`, an exact count becomes `> 0`, an
assertion is deleted, a test file is deleted. Sometimes the report calls the narrowing a
widening.

**Detect:** net assertion lines per test file; exact matchers traded for loose ones; deleted
test files.

**Caught by:** scanner:`assertion-removed`, `assertion-loosened`, `test-deleted`,
`skipped-test`.

### E11. Undisclosed behaviour change

*Regular (~10).*

**Looks like:** a refactor that widens what gets scanned, deleted or accepted, under a brief
that said nothing else changes.

**Detect:** for each changed predicate, compare the before and after input sets. Every
widening is disclosed in the PR body.

**Caught by:** antislop-execution (disclose); antislop-audit step 4.

### E12. Gate violation

*Rare (~7).*

**Looks like:** the worker decides a question the brief reserved for a human, touches live
infrastructure, or routes around a harness guard.

**Detect:** compare the brief's gates with what the run did.

**Caught by:** antislop-execution (stopping rules); antislop-audit step 3 (`GATED` needs a
memo).

---

## Report-side: completion reports and shipped prose

### R1. Overclaiming prose

*Common (~115). This is the most frequent pattern.*

**Looks like:**
- a comment says "the assertion below fails loudly" and there is no assertion;
- the PR body says "every caller now…" when one caller doesn't;
- help text promises behaviour the code doesn't have;
- a correction is made at the top of a document and not in the table row that repeats the
  claim.

**Detect:** list every universal or coverage claim in shipped text: the PR title and body,
changesets, docs, help and remedy strings, comments. Each needs an enumerating test or a
`file:line`, or it gets narrowed.

**Caught by:** scanner:`sweep-claim`; antislop-audit step 4.

### R2. Disclosure kept out of the durable record

*Regular.*

**Looks like:** a known gap or behaviour change appears in the completion report, which
doesn't land, but not in the PR body or commit, which do.

**Detect:** every `partial`, `refused` and behaviour-change item in the report also appears
in the PR body.

**Caught by:** antislop-execution; antislop-audit step 4.

### R3. Buried loss and softened severity

*Regular.*

**Looks like:** "Status: complete" at the top, and a real loss on the last line. A defect
filed under "why this is not this PR's problem".

**Detect:** the headline status matches the ledger. Each "not this PR's defect" claim is
backed by the base revision.

**Caught by:** antislop-audit steps 3 and 6.

### R4. Follow-up dumping

*Rare (4 of about 620 follow-up items).*

**Looks like:** a brief-required behaviour, sometimes one the brief explicitly forbade
skipping, is filed as a follow-up.

**Detect:** reconcile each follow-up against the ledger. Phrase-grepping for "follow-up"
mostly finds honest reporting.

**Caught by:** antislop-audit step 6.

### R5. Handoff and elision

*Rare in missions with a gate convention.*

**Looks like:** "let me know if you'd like me to…", "the rest follow the same pattern",
"and so on". This is single-response laziness carried into a report.

**Detect:** phrase scan.

**Caught by:** scanner:`handoff`, `elision`.

### R6. Unproven and blanket claims

*Regular.*

**Looks like:** "should work", "works as expected", "all tests pass", "no regressions",
with no command, counts or baseline.

**Detect:** phrase scan, then look for the evidence.

**Caught by:** scanner:`unproven-claim`, `blanket-green`, `sweep-claim`.

---

## Reviewers slop too

The same record shows the review side drifting:
- about one verdict in five admits it executed nothing;
- many review prompts paraphrased the author's claim, or forbade running tests;
- one CLEAN verdict later proved wrong.

An audit or review should label each check **[executed]** or **[static]**. It should quote
the claim it is falsifying rather than paraphrase it, and it should be allowed to run the
tests.
