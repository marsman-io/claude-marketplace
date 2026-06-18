---
name: tutorial-scaffold
description: >-
  Produce a learning-oriented Diátaxis tutorial: a guided, choice-free lesson that takes a first-timer from nothing to one concrete working result, with the exact visible feedback shown after every step so they can confirm they are on track. Grounds every decision in the Diátaxis tutorial compass (learning-oriented, action + acquisition) and the "teacher takes responsibility for the learner's success" principle. Triggers on "write a tutorial", "getting started guide", "first-time / beginner walkthrough", "guided lesson", "quickstart that can't fail", "onboarding tutorial". NOT for a competent user pursuing a specific real goal (use how-to-recipe), NOT for clarifying how/why something works (use explanation-doc), NOT for exhaustive parameter listings (use reference-from-spec).
---

# Tutorial Scaffold

A tutorial is a lesson, not documentation of a task. Its job is to give a beginner a meaningful, repeatable first experience that ends in a single concrete result and the confidence to continue. The success metric is not coverage — it is that a first-timer reaches the end with something that works. The author, not the learner, is responsible for that success: every step must be guaranteed, every result must be visible, and the learner must never be asked to decide, improvise, or understand theory. If they can fail, the tutorial has failed.

## When to use
**Do**
- Write a first contact lesson: "Build your first X with the CLI / SDK / REST API / MCP server."
- Guarantee a single, concrete, repeatable result the beginner produces by doing.
- Show exact expected output after each step so the learner self-confirms.
- Strip the path to one straight line — no decisions, no branches.

**Don't**
- Help a competent user accomplish a real-world goal → how-to-recipe.
- Explain why it works, trade-offs, or architecture → explanation-doc.
- Enumerate every flag, field, or endpoint → reference-from-spec.
- Offer alternatives, options, or "depending on your setup" — that breaks the guarantee.

## Procedure
1. Pick ONE small, concrete, motivating thing the beginner will build or produce. It must be achievable in minutes and visibly "real."
2. State minimal prerequisites once, up front. Assume nothing else; if a step needs setup, the tutorial provides it inline. Pin versions so the result is repeatable.
3. Write strictly sequential steps. Each step = one action + the exact visible result ("You should see:"). The learner confirms before moving on.
4. Ruthlessly strip choices, alternatives, and explanation. No "you could also", no "this works because", no "if you prefer". One command, one outcome.
5. End with the concrete result the learner can see ("What you built") and a single pointer onward ("Next steps") — do not branch into a menu.

## Output
```
# Build your first task with the CLI

## What you'll build
A working task that you submit from the command line and watch run to
completion — by the end your terminal will print `status: done` and a result id.

## Before you begin
You need:
- The CLI installed (version 2.x): `tool --version` prints `tool 2.x`
- A project directory you can write to

That's everything. Do each step in order; don't skip ahead.

### Step 1 — Create a working folder
```
mkdir first-task && cd first-task
```
You should see: a new empty directory; `pwd` ends in `/first-task`.

### Step 2 — Initialize the project
```
tool init
```
You should see:
```
Created config.yaml
Project initialized.
```
A file `config.yaml` now exists in the folder.

### Step 3 — Define one task
```
tool add "say hello"
```
You should see:
```
Added task #1: say hello
```

### Step 4 — Run it
```
tool run
```
You should see:
```
Running task #1...
hello
status: done   result: r_001
```

### Step 5 — Confirm the result
```
tool status r_001
```
You should see:
```
result r_001
state:  done
output: hello
```

## What you built
You created a project, defined a task, ran it, and confirmed a finished
result with id `r_001`. You did a full end-to-end cycle with the CLI.

## Next steps
Ready to apply this to a real goal of your own? See the how-to:
"Run a scheduled task."
```

Failure mode: smuggling explanation ("this works because…") or choices ("alternatively you could…") into the lesson — the instant a beginner must decide or absorb theory, the guaranteed-success contract breaks and it has drifted into a how-to or explanation.

Sources: Diátaxis — Tutorials (https://diataxis.fr/tutorials/); Diátaxis compass (https://diataxis.fr/compass/).
