---
name: project-impact-trace
description: Trace the blast radius of a proposed change against a product work constraint cascade. Input — which constraint is being moved, by how much. Output — every dependent path + artifact affected, with review / verification cost. For adjust/replan phase. Use to answer "is this a small change or a hidden replan?" before agreeing to it.
---

# Trace project change-request impact

Read `${CLAUDE_PLUGIN_ROOT}/docs/Constraint-based project management.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` (adjust phase).

## Procedure

Given a target constraint (intent, user path, data shape, API contract, UI behavior, evidence bar, context boundary) and a proposed change:

1. **Find direct consumers.** Read the intent note / issue / plan / diff / dependency map. What downstream user paths, files, tests, screenshots, prompts, docs, or deployment surfaces depend directly on this constraint?

2. **Classify each consumer:**
   - **Re-derives automatically** — downstream work that adjusts from existing code or tests without new product judgment (e.g., a snapshot updates after copy changes).
   - **Re-plans manually** — work that requires a new prompt, acceptance decision, or review pass.
   - **External / hard commitments** — promises to users, saved data, public APIs, payment behavior, privacy, legal / compliance, or release commitments. Cannot be unilaterally moved.

3. **Find transitive consumers.** Downstream of downstream. The change might fan out 3-4 levels — a data-shape change affects a UI state, which affects a screenshot, which affects a demo path.

4. **Estimate migration cost — and whether you can actually verify it.**
   - Number of user paths / files / tests / docs / screenshots affected
   - Per-class breakdown (auto / manual / hard commitment)
   - Approximate effort (review passes + verification updates + prompt / context changes)
   - **Verifiability**: can you confirm the whole fan-out is correct in one focused pass, or does it spread across more surface than you can check before accepting? For a solo builder the usual "hidden replan" signal is not a contract — it's a change that silently outruns your verification budget, so you accept it on faith.

5. **Identify alternative paths.** Could re-pinning a different constraint absorb this change at lower cost? Could de-scoping a droppable behavior insulate the rest? Could a smaller evidence path test the same intent?

## Output

```
Target constraint: <name>
Proposed change: <description>

Direct consumers (<N> total):
  - Auto-rederives (<N>):  <list>
  - Manual replan (<N>):  <list>
  - Hard commitments (<N>):  <list>

Transitive consumers: <N> additional paths / artifacts

Migration cost estimate:
  - Review passes: <estimate>
  - Verification updates required: <list>
  - Prompt / context changes: <list>
  - Product disruption: <by user path / artifact>
  - Verifiable in one pass? <yes | no — fan-out exceeds what you can check before accepting>
  - Verdict: <"true adjust — few consumers, no hard commitments, verifiable in one pass" | "hidden replan — hard commitments to re-negotiate AND/OR fan-out outruns your verification budget" | "intermediate">

Alternative paths to reduce blast radius:
  - <alternative 1>: <effect>
  - <alternative 2>: <effect>
```

The cost classification is the deliverable. A change is a hidden replan when it touches hard commitments you can't unilaterally move *or* when it fans out across more surface than you can verify before accepting it — both mean "small ask, large unseen cost." Name it as such.
