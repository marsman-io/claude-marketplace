---
name: task-analysis
description: >-
  Decomposes a single user goal into an ordered tree of subgoals and leaf operations governed by explicit PLANS (sequence / conditional / parallel / iterative), and produces the baseline DX metrics you will later optimize against. Models dev-tool tasks end-to-end ACROSS surfaces (docs → install → CLI auth → SDK call → dashboard verify) because real work crosses the seam. Use when you need a grounded, observed baseline before any redesign. Triggers on "task analysis", "hierarchical task analysis", "HTA", "break down this task", "how many steps to first call", "count the decision points", "time to value", "decompose the goal". NOT for judging whether a newcomer can learn each step (→ cognitive-walkthrough), defining the single ideal route (→ golden-path), or inventorying what breaks (→ failure-state-matrix).
---

# Task Analysis

Hierarchical Task Analysis decomposes one user goal into a numbered tree — subgoals branching down to atomic operations at the leaves — where every parent node carries an explicit PLAN that says how its children combine (in sequence, conditionally, in parallel, or iteratively). The PLAN is the most-skipped and highest-value part: it is where hidden branches, retries, and "go back to the dashboard and copy the key" detours surface, and it is what stakeholder guesses always omit. Ground the tree in real observed behavior — a recording, a session transcript, your own timed run — not in how the team wishes the tool worked. The output is a baseline: step count, decision count, and DX-specific friction metrics that every later skill optimizes against. This skill DIAGNOSES; it produces a model and metrics, it does not edit product code — you intervene.

## When to use

**Do**
- Use as the first pass on a goal, to get a defensible baseline before any other evaluation.
- Model the whole goal end-to-end across surfaces; treat each surface transition as a real node.
- Capture both a novice path and an expert path when they diverge.
- Accept an in-repo target OR a pasted artifact (a `--help` dump, an OpenAPI spec, a quickstart URL, recorded terminal output). "Not in repo" is normal.

**Don't**
- Don't invent steps from memory or the README; cite the observed source for each leaf.
- Don't judge whether steps are learnable or well-named here — that is cognitive-walkthrough.
- Don't decompose past the stopping rule; infinite depth is a smell.

## Procedure
1. State the goal as one user-meaningful outcome and the persona (novice or expert).
2. Pick the grounding source and cite it (file:line, pasted block, or URL) for every leaf.
3. Decompose top-down: number the root `1`, subgoals `1.1`, operations `1.1.1`. Operations live only at leaves.
4. Write a PLAN line under every parent: sequence / conditional / parallel / iterative, naming the trigger for conditionals and the exit for iterations.
5. Walk the tree end-to-end and mark each surface transition and each copy-paste handoff as its own node.
6. Apply the stopping rule per branch: stop expanding when P×C×W (probability the detail matters × cost of getting it wrong × worth of redesigning it) drops below threshold.
7. Tally the metrics table from the finished tree.

## Output
```
GOAL (1): <one-line outcome>  | persona: novice|expert  | source: <cite>

1  <subgoal>            PLAN 1: do 1.1 then 1.2; if <cond> do 1.3   [sequence|conditional|parallel|iterative]
1.1  <subgoal>          PLAN 1.1: ...
1.1.1  <operation>      // leaf, cite source
1.1.2  <operation>      // leaf  [SURFACE TRANSITION: CLI → dashboard]
1.2  <operation>        // leaf  [COPY-PASTE HANDOFF: API key]
...

Metrics baseline
| Metric                                   | Novice | Expert |
|------------------------------------------|--------|--------|
| Step count (leaf operations)             |        |        |
| Decision count (conditional branches)    |        |        |
| Context-switches between surfaces        |        |        |
| Copy-paste handoffs                      |        |        |
| Distinct credentials / config files touched |     |        |
| Time-to-first-hello-world (TTFHW)        |        |        |
| Observed error rate                      |        |        |
| Frequency of this task                   |        |        |
```

Failure mode: an HTA built from stakeholder intent instead of observed behavior is fiction with numbers — it will baseline a path no real user walks.

Sources: Annett & Duncan (Hierarchical Task Analysis); NN/g task analysis.
