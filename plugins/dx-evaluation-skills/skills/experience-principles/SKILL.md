---
name: experience-principles
description: >-
  Distills 3–6 crafted, opinionated, TESTABLE principles that settle design trade-offs across every surface — a DX contract and quality bar, distinct from values and style. Each principle must pass four tests: specific (names your domain's trade-offs, not "be delightful"), chooses a side (its opposite is a coherent alternative someone could pick — if the opposite is absurd, it is a slogan, cut it), short (3–7 words, "X over Y"), and testable (pairs with concrete behaviors that decide real reviews). Produces principles that double as code-review acceptance criteria and feed heuristic-evaluation. Use to define or critique the experience bar. Triggers on "experience principles", "ux contract", "design principles", "dx contract", "quality bar for the experience", "what does good look like here". NOT for judging a surface against generic usability heuristics (→ heuristic-evaluation) or inventorying error states (→ failure-state-matrix).
---

# Experience Principles

Experience principles are a small set — 3 to 6 — of crafted, opinionated, testable statements that settle the trade-offs your tool faces on every surface. They are not values ("we care about developers") and not style ("use sentence case"); they are a contract that decides arguments. The discipline is in the four tests, and the decisive one is "write the opposite": state the inverse of your candidate and ask whether a competent team could rationally choose it. If the opposite is a real alternative ("imperative over idempotent" — plenty of tools live there), you have a principle. If the opposite is absurd ("be confusing"), you have a slogan; cut it. Each survivor must also be specific to your domain, short (3–7 words, framed "X over Y"), and testable via concrete behaviors that decide real reviews. This skill DEFINES and critiques the bar; it does not edit product code — you intervene. The output doubles as a code-review acceptance checklist and as input heuristics for heuristic-evaluation.

## When to use

**Do**
- Run all four tests on every candidate and cut the ones that fail; show your work.
- Force every principle into "X over Y" and write its opposite explicitly.
- Pair each with 2–3 concrete behaviors, including at least one "do NOT do this".
- Turn each into a checklist line that a reviewer can apply to a diff.
- Accept a pasted artifact (existing design docs, a style guide, a values page). "Not in repo" is normal.

**Don't**
- Don't ship more than 6; a long list is values, not a contract.
- Don't keep a candidate whose opposite is absurd — that is a slogan.
- Don't restate Nielsen's heuristics — those are the generic floor; principles are your domain's chosen trade-offs.

## Procedure
1. Gather the recurring trade-offs the tool keeps re-litigating (cite where they showed up).
2. Draft candidates as "X over Y", drawing on high-value DX patterns: idempotent over imperative; errors teach the fix; same mental model on every surface; copy-paste must just work; safe by default, powerful on request; upgrades never surprise; observable by default; works headless / agent-first.
3. For each candidate run the four tests: specific? chooses a side (write the opposite)? short (3–7 words)? testable?
4. Cut every candidate that fails any test; keep 3–6.
5. For each survivor write the one-line rationale, 2–3 concrete behaviors (incl. a "do NOT"), and the checklist item it becomes.

## Output
```
| # | Statement (3–7 words, X over Y) | Opposite (coherent? Y/N) | One-line user rationale | Concrete behaviors (2–3, incl. a "do NOT") | Code-review checklist item |
|---|---------------------------------|--------------------------|-------------------------|--------------------------------------------|----------------------------|
| 1 | Idempotent over imperative      | Y                        |                         | - re-run is a no-op  - … - do NOT … |                  |
| 2 | Errors teach the fix            | Y                        |                         |                                            |                            |

Cut (failed a test):
- "<candidate>" — failed: <specific|opposite|short|testable> because <why>
```

Failure mode: a principle whose opposite no one would ever choose is a feel-good slogan that quietly approves every design and rejects none.

Sources: NN/g design principles; DesignSystems.one (the four tests / "write the opposite").
