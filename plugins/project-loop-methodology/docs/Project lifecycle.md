# Project lifecycle

A project is not a static plan. It passes through phases, and the
questions that matter — and the answers that work — shift with each.
The four lenses (project loop, outcome altitude, project cascade,
priority budget) still apply at every phase, but they read very
differently in a chartering-stage project vs. one mid-execution vs. one
that's in trouble and being replanned.

Naming the phase first lets the right procedure run. Asking "what's the
critical path?" of a project that doesn't have an agreed scope yet
wastes the loop. Asking "what's the blast radius of this change?" of a
project that hasn't started yet is incoherent.

## The five phases

### 1. Charter

The idea exists; a plan does not. The decisions are first-order: what
problem are we solving? for whom? what are the hard constraints (a
deadline, a contract, a regulation)? what is the scope envelope? who
owns this?

**What dominates**: identifying intent (what should become true for
which stakeholder), naming the hard pins, scoping the soft inputs that
the plan will tune. There is no "plan vs reality" yet — both sides are
abstraction.

**Failure mode — charter-without-bounds**: producing a 40-page brief
that names every option without committing to any. Charters that don't
commit to *scope* and *priority* defer the hard decisions into Plan,
where they cost more.

### 2. Plan

Charter exists; team is working out how to deliver it. The decisions
are about whether the abstractions hold under contact with estimates,
dependencies, and capacity. This is where most "we didn't realize"
moments surface: the team you expected isn't available, the upstream API
isn't ready, the design discovery takes longer than budgeted.

**What dominates**: testing the charter by *planning against it*.
Identifying which constraints the team can actually meet, which they
can't, and what the planner is asking for that wasn't in the charter.

**Failure mode — over-plan**: a 200-line Gantt chart for a project
whose intent isn't yet validated. The cost of replanning a heavy plan
discourages the planning team from surfacing problems. Plans should
match the certainty they're describing.

### 3. Execute

Plan is in motion. The team is doing the work. The decisions are about
*monitoring for drift* — where is the project diverging from plan, and
which divergences matter? Some drift is fine; some is the early signal
of project failure.

**What dominates**: cross-team / cross-workstream observation. The
project is now a portfolio of activities; the PM job is no longer "make
the plan" but "see the patterns the team can't see from inside their
work."

**Failure mode — per-task management**: managing each blocker
individually as it arrives rather than seeing the patterns. If three
blockers all trace to the same upstream team, the finding is "that
team's capacity is wrong," not "three blockers."

### 4. Adjust

A specific in-flight change request has arrived — scope expand, scope
cut, timeline shift, resource change. The decisions are about *blast
radius and tradeoffs*: what does this change cost in time, scope, or
cost? does it preserve intent? is the change worth the disruption?

**What dominates**: impact tracing. The lens isn't "what should the
project be?" — that was answered in Charter — it's "what breaks if we
move this?"

**Failure mode — small-feeling changes that aren't**: a "small scope
addition" that requires three weeks of architecture changes is not an
adjustment. Failing to trace impact means absorbing more disruption
than agreed.

### 5. Replan

The project has drifted significantly from plan, or the underlying
context has shifted so much that the current plan can't be patched.
You're not making a small change; you're remaking the plan. The
decisions are about *preservation*: which parts of the original
charter still apply? which parts of the executed work still ladder to
intent? what's the migration path from "current state" to "new plan"?

**What dominates**: triage. Distinguishing the work that's still
load-bearing from the work that's become irrelevant.

**Failure mode — start over from scratch**: replanning from a blank
page wastes the discovery the team has already paid for. Most
replanning is fixable surgically — re-pin one or two constraints,
collapse three workstreams into one, re-baseline the dates.

## How each lens reads per phase

The lenses don't change; the procedures do. The same `project-cascade`
lens runs `constraint-build` in Charter and `impact-trace` in Adjust.

| Lens         | Charter                        | Plan                              | Execute                          | Adjust                            | Replan                            |
|--------------|--------------------------------|-----------------------------------|----------------------------------|-----------------------------------|-----------------------------------|
| Outcome      | name the intent / who benefits | first deliverables match intent?  | where has scope drifted?         | does this change move toward intent? | what was the original intent?   |
| Cascade      | model the constraints          | test the plan                     | find broken dependencies         | trace blast radius                | collapse / re-pin constraints    |
| Priority     | name the portfolio type        | allocate budget across 5 mechanisms | cross-initiative drift          | what does this change spend?      | systemic priority overspending   |
| Project loop | what's the first test?         | iterate the plan fast             | where did we stop looping?       | is this worth a loop?             | merge multiple loops              |

## Detecting the phase

Heuristic — what evidence shows up in the artifacts?

- **No agreed scope, no team, no plan** → Charter
- **Charter exists, team active, plan being written, dates fluid** → Plan
- **Plan committed, work in motion, regular status updates, fixed dates** → Execute
- **Single change request, plan baseline intact, focused tradeoff conversation** → Adjust
- **Plan being remade, "the original plan is no longer valid" said aloud, re-baselining** → Replan

A project can be in **multiple phases at once**: workstream A is in
Execute while workstream B is in Replan because B's upstream just
slipped. Phase per workstream, not per project.

## Why this taxonomy exists

Without phase awareness, a PM critic asks the Charter questions of a
project in Execute. The result is a useless answer: "you should name the
intent" is true at Charter, useless when the intent is named and the
question is which workstream to expedite.

Each agent in this plugin starts by detecting phase, then composes the
skill set that matches the phase. The skills are the verbs (one
procedure each); the agents are the workflows (compose skills, detect
phase, branch).
