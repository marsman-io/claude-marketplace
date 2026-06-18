# Project lifecycle

A delegated product project is not a static task. It passes through
phases, and the questions that matter — and the answers that work —
shift with each. The four lenses (project loop, outcome altitude,
project cascade, priority budget) still apply at every phase, but they
read very differently when intent is being captured vs. when an agent
has already produced a diff.

Naming the phase first lets the right procedure run. Asking "what is
the blast radius of this change?" before the intended behavior is named
wastes the loop. Asking "what is the intended outcome?" after the diff
exists may still matter, but only if the artifact no longer makes that
outcome inspectable.

## The five phases

### 1. Charter

The idea exists; a delegation plan does not. The decisions are
first-order: what problem are we solving, for whom, what should become
true, what must not break, and what evidence will prove the result?

**What dominates**: identifying intent (what should become true for the
intended user), naming hard pins, and scoping the soft inputs the plan
will tune. There is no "plan vs reality" yet — both sides are
abstraction.

**Failure mode — intent-without-bounds**: a prompt or issue that names
many wishes but no acceptance shape. Without scope, pins, and evidence,
the agent must guess which parts matter.

### 2. Plan

Intent exists; the builder is working out how to delegate or sequence
the work. The decisions are about whether the abstraction holds under
contact with the codebase, available context, integration surface, and
verification options. This is where most "we did not realize" moments
surface: the existing API shape is different, the screen is doing two
jobs, or the agent needs a narrower prompt.

**What dominates**: testing the intent by planning against it. Identify
which constraints can actually be met, which cannot, and what the plan
asks the agent to infer.

**Failure mode — over-plan**: a large task breakdown for intent that
has not been validated. The cost of changing a heavy plan discourages
the builder from noticing that a smaller experiment would teach more.

### 3. Execute

The plan is in motion or the agent has produced work. The decisions are
about *monitoring for drift* — where is the artifact diverging from
intent, and which divergences matter? Some drift is fine; some is the
early signal that the agent solved the wrong problem.

**What dominates**: cross-artifact observation. Read the issue, prompt,
diff, tests, screenshots, logs, and demo behavior together. The PM job
is no longer "make the plan" but "see the pattern the artifact does not
explain by itself."

**Failure mode — per-task management**: managing each TODO, failing
test, or changed file individually rather than seeing the pattern. If
three symptoms all trace to the same missing intent constraint, the
finding is "the agent was never given the product boundary," not "three
bugs."

### 4. Adjust

A specific in-flight change request has arrived — scope expand, scope
cut, prompt revision, implementation swap, UI change, data-shape change.
The decisions are about *blast radius and tradeoffs*: what does this
change cost in scope, evidence, risk, or review? Does it preserve
intent? Is the change worth the disruption?

**What dominates**: impact tracing. The lens is not "what should the
product be?" — that was answered in Charter — it is "what breaks if we
move this?"

**Failure mode — small-feeling changes that are not**: a "small copy
change" that alters the user's decision model, or a "quick schema
change" that forces migrations and test rewrites. Failing to trace
impact means absorbing more disruption than the builder intended.

### 5. Replan

The work has drifted significantly from intent, or the underlying
context has shifted so much that the current plan cannot be patched.
You are not making a small change; you are remaking the delegation. The
decisions are about *preservation*: which parts of the original intent
still apply, which parts of the produced work still carry value, and
what migration path moves from "current artifact" to "intended product"?

**What dominates**: triage. Distinguishing the work that is still
load-bearing from the work that became plausible but irrelevant.

**Failure mode — start over from scratch**: replanning from a blank page
wastes the discovery already paid for. Most replanning is fixable
surgically — re-pin one or two constraints, collapse a broad scope into
one user path, or replace an ambiguous prompt with a sharper one.

## How each lens reads per phase

The lenses do not change; the procedures do. The same **constraint** lens
runs `project-constraint-build` in Charter and `project-impact-trace` in Adjust.

| Lens         | Charter                        | Plan                              | Execute                          | Adjust                            | Replan                            |
|--------------|--------------------------------|-----------------------------------|----------------------------------|-----------------------------------|-----------------------------------|
| Outcome      | name the intent / who benefits | first artifacts match intent?     | where has behavior drifted?      | does this change move toward intent? | what was the original intent?   |
| Intent verify| write the acceptance criteria  | criteria cover failure + boundary?| built thing: gaps + drift?       | does the change still meet criteria? | re-derive criteria, re-check    |
| Cascade      | model the constraints          | test the delegation plan          | find broken dependencies         | trace blast radius                | collapse / re-pin constraints    |
| Priority     | name the work mode             | allocate attention across 5 mechanisms | cross-issue drift             | what does this change spend?      | systemic priority overspending   |
| Project loop | what is the first test?        | iterate the plan fast             | where did we stop looping?       | is this worth a loop?             | merge multiple loops              |

## Detecting the phase

Heuristic — what evidence shows up in the artifacts?

- **No agreed intent, no acceptance shape, no delegation plan** -> Charter
- **Intent exists, prompt / issue / plan being written, scope fluid** -> Plan
- **Agent work in motion or diff produced, tests / screenshots / logs present** -> Execute
- **Single requested change, baseline intent intact, focused tradeoff conversation** -> Adjust
- **Plan being remade, "the original approach no longer works" said aloud, broad re-prompting or re-baselining** -> Replan

A project can be in **multiple phases at once**: one user path is in
Execute while another is back in Charter because its intent was never
named. Phase per workstream, not per repository.

## Why this taxonomy exists

Without phase awareness, a PM critic asks the Charter questions of work
that is already in Execute. The result is a useless answer: "you should
name the intent" may be true at Charter, but in Execute the sharper
question is which artifact stopped carrying that intent.

Each agent in this plugin starts by detecting phase, then composes the
skill set that matches the phase. The skills are the verbs (one
procedure each); the agents are the workflows (compose skills, detect
phase, branch).
