# Constraint-based project management for agentic product work

Constraint-based PM is a way to run product work by describing
**relationships** between intent, scope, fidelity, risk, evidence,
context, and integration surface instead of treating the agent's task as
a fixed-point command.

In traditional task terms, instead of saying:

```
Build feature X
by Friday
with the current codebase
```

you define rules like:

```
intent >= "a new user can finish onboarding without asking what to do next"
scope <= one route + one persisted preference
quality >= usable on mobile and desktop
evidence >= screenshot + happy-path test + manual demo
risk <= reversible without data migration
context includes current component pattern and prior failed attempt
```

The planning process solves for those relationships and produces a
concrete delegation or review plan that satisfies them.

## Core idea

A project is modeled as a set of constraints:

```
User outcome A is mandatory
Behavior B is mandatory
Nice-to-have C is droppable
Data contract D must not change
Manual review time <= one focused pass
Verification must include the intended user path
```

The builder then figures out the sequencing, scope, and agent context
that satisfies those rules.

## Hard vs soft constraints

A **hard constraint** must be satisfied:

```
must preserve existing saved data
must work in the current deployment environment
must not expose private user content
must keep the public API contract stable
must satisfy the acceptance criterion in the issue
```

A **soft constraint** is preferred but negotiable:

```
prefer the smallest diff
prefer to reuse the existing component
would like the agent to cover the edge case in this pass
ideally keep the change easy to revert
```

When pressure rises, the builder decides which soft constraints to
relax. The hard ones stay.

## Intrinsic size

Some work has natural duration or complexity even when an agent is fast:

```
understanding an unfamiliar data model requires context
visual polish requires screenshots or a browser pass
schema changes require migration thinking
auth and permissions require explicit verification
ambiguous intent requires a clarification or a smaller bet
```

Good planning combines external urgency with intrinsic complexity that
cannot be wished away by delegation.

## Priorities

Some constraints matter more than others:

```
matching the intended user outcome is non-negotiable
shipping every nice-to-have can flex
using the first implementation approach is droppable
keeping the change reviewable is more important than broad scope
```

When the plan has to break something, this priority order tells it
*which* constraint to relax. Without explicit priorities, the agent or
the builder relaxes whichever constraint is least visible, which is
usually the wrong one.

## The classic PM triangle

The familiar scope/time/cost/quality triangle still exists, but "cost"
often means attention, context, review effort, and risk:

```
fix scope + speed -> review depth varies, usually shrinks
fix scope + review depth -> speed varies, usually slows
fix speed + review depth -> scope varies, usually shrinks
fix everything -> quality breaks silently
```

Pretending you can fix all four is the canonical project failure.
Naming which three you've fixed and which one is the absorbing buffer is
the constraint-based move.

## Dependencies as relationships

Most agent tasks treat dependencies as an ordered list ("edit A, then
B"). A constraint-based view treats them as relationships:

```
UI B requires API A's response shape, not all of API A
test C can start once the behavior contract is named
copy D depends on the product intent, not the component implementation
demo path E breaks if auth state F changes
```

This surfaces *what part* of each upstream dependency matters and *when*,
which usually opens a smaller, safer path than a broad rewrite.

## Important concepts

### Pinned constants

Some values must not move regardless of what else changes. These are the
project's hard constraints made explicit: user trust, data safety,
public API contracts, existing design conventions, deployment limits,
accessibility floors, payment behavior, legal or compliance boundaries.
Name them up front. When something has to give, it cannot be one of
these.

### Failure modes at the extremes

For each soft input, name what breaks at min and max:

- **Scope too small** -> artifact does not satisfy intent
- **Scope too big** -> diff becomes unreviewable and hidden assumptions multiply
- **Speed too high** -> agent guesses, verification thins out
- **Speed too low** -> momentum dies and context goes stale
- **Context too low** -> agent optimizes for the wrong shape
- **Risk too high** -> small prompt becomes large product blast radius
- **Review too low** -> plausible output ships without product judgment

Knowing the extremes lets you find the safe operating range.

## Constraint-based PM vs task-list PM

Task-list PM says:

```
Here is the issue.
Do these steps.
Mark it done.
```

Constraint-based PM says:

```
Here is the intent.
Here are the hard constraints.
Here are the soft inputs we are tuning.
The implementation path emerges from the constraints; the checklist is a
projection, not the model.
```

The issue list is a projection of a constraint model, not the model
itself. Treating the list as the model is the canonical failure mode
that leads to agent-built work nobody believes.

## In practice

A constraint-based product plan usually defines:

```
hard pins (user trust, data, API, deployment, accessibility)
soft inputs (scope, fidelity, evidence, context, risk, integration, review)
priority ordering when something has to give
dependency relationships, including which PART of each upstream matters
critical-path identification
verification budget per pass
failure-mode trigger conditions
```

The goal is not "perfect prediction." It is "a plan that remains useful
after a capable black box has made choices on your behalf."
