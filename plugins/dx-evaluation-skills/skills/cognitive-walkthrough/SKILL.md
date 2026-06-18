---
name: cognitive-walkthrough
description: >-
  Inspects the learnability of a predefined correct action sequence by asking FOUR questions at every step; a step passes only if all four are "yes", and any single "no" is a learnability failure. Measures the first-use / walk-up-and-use experience specifically. For dev tools the "control" is a command, flag, function signature, or env var — not a button — so discoverability means `--help`/quickstart/error hints, affordance means naming (`tool sync` vs `tool apply`), and feedback means stdout, exit codes, or an observable created resource. For an MCP server the "user" is an AGENT: can the model pick the right tool from its name+description+schema, and parse the result. Use when assessing newcomer success on a known-correct flow. Triggers on "cognitive walkthrough", "will a new user know what to do", "learnability review", "walk through this flow as a newcomer", "first-use experience", "is this discoverable", "can an agent figure out which tool to call". NOT for building the metric baseline (→ task-analysis) or principle-level critique against usability heuristics (→ heuristic-evaluation).
---

# Cognitive Walkthrough

A cognitive walkthrough is a task-based learnability inspection: you fix one correct action sequence and, at each step, ask the four questions a first-time user's mind silently asks. A step passes only when ALL FOUR are "yes"; a single "no" is a learnability failure with a location and a cause. It targets first use — the moment of no prior training — which is exactly when dev-tool adoption is won or lost. Reframe the four questions for developer surfaces: the action is a command/flag/signature/env-var, discoverability lives in `--help`, the quickstart, and error suggestions, affordance lives in naming and argument shape, and feedback lives in stdout/stderr, exit codes, and resources the user can observe. Run it per surface AND across the seam — especially the step where a key is copied from the dashboard into the CLI. For an MCP surface the user is a model: Q2/Q3 ask whether it can select the right tool from name+description+schema, Q4 whether the returned result is parseable and actionable. This skill DIAGNOSES learnability; it does not edit product code — you intervene.

## When to use

**Do**
- Fix the persona, task, correct action sequence (lift it from task-analysis), and step granularity BEFORE walking — state them.
- Run a separate pass per surface, then a pass dedicated to the cross-surface seam steps.
- For an MCP target, evaluate as the agent: judge name+description+schema sufficiency, not human screens.
- Accept a pasted artifact (a `--help` dump, an OpenAPI spec, a tool schema, recorded output). "Not in repo" is normal.

**Don't**
- Don't critique against general principles here — that is heuristic-evaluation.
- Don't change the action sequence mid-walk; a different path is a different walkthrough.
- Don't mark a step "pass" without a cited reason for each yes.

## Procedure
1. State setup: persona, task, the correct action sequence, step granularity.
2. For each step, ask Q1–Q4 and answer Y/N with a cited why (file:line, pasted block, exact message, or schema field).
3. Q1: will the user try to achieve the right result (is the right subgoal in their head)?
4. Q2: will they notice the correct action is available (discoverability — `--help`/quickstart/error hint/tool list)?
5. Q3: will they associate that action with the result they want (naming/affordance/signature)?
6. Q4: after acting, will they see that progress was made (stdout/exit code/created resource/parseable return)?
7. Pass only if all four are yes; otherwise mark Fail, assign severity, and write one recommendation.
8. Repeat across the seam: re-walk the steps that cross surfaces.

## Output
```
Setup: persona=<…>  task=<…>  sequence source=<HTA cite>  granularity=<…>

| Task | Step# | Step description | Q1 Y/N + why | Q2 Y/N + why | Q3 Y/N + why | Q4 Y/N + why | Pass/Fail | Severity | Recommendation |
|------|-------|------------------|--------------|--------------|--------------|--------------|-----------|----------|----------------|
|      | 1     |                  |              |              |              |              | (all-yes=Pass) |     |                |
```

Failure mode: a walkthrough run by someone who already knows the tool quietly answers every question "yes" — expert eyes cannot see the first-use cliff.

Sources: NN/g cognitive walkthrough; Wharton, Rieman, Lewis & Polson.
