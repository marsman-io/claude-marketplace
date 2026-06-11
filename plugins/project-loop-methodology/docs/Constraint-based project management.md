# Constraint-based project management

Constraint-based PM is a way to run projects by describing
**relationships** between scope, time, cost, quality, risk, and
dependencies — instead of fixed-point commitments.

In traditional PM terms, instead of saying:

```
Ship feature X
by March 31
with 4 engineers
costing $200k
```

you define rules like:

```
scope >= MVP (must include A, B; may include C, D)
ship_date <= contractual deadline of April 15
cost <= budget envelope of $250k
quality >= "supports the one customer segment we promised"
risk <= "we can ship without C if A and B are solid"
A and B can ship together; C depends on B; D depends on C
```

The planning process solves for those relationships and produces a
concrete plan that satisfies them.

## Core idea

A project is modeled as a set of constraints:

```
Deliverable A is mandatory
Deliverable B is mandatory
Deliverable C is desired but droppable
Deliverable D depends on C
Total cost <= $X
Total time <= Y weeks
Quality must support compliance audit
```

The planner then figures out the sequencing, scope, and resource
allocation that satisfies those rules.

## Hard vs soft constraints

A **hard constraint** must be satisfied:

```
ship by contractual deadline of April 15  (legally binding)
must pass SOC 2 audit                       (compliance)
data residency stays in EU                  (regulatory)
```

A **soft constraint** is preferred but negotiable:

```
ideally finish before end of Q2
prefer to use the existing team
would like exec sponsor available for every milestone
```

When time is limited, the team decides which soft constraints to relax.
The hard ones stay.

## Intrinsic size

Some work has natural duration:

```
contractual review takes ~2 weeks regardless of urgency
new hires take 6+ weeks to ramp
security review needs the calendar windows it needs
end-of-quarter freezes are unavoidable
```

Good project planning combines external rules with intrinsic durations
that cannot be compressed.

## Priorities

Some constraints matter more than others:

```
shipping at all is non-negotiable
shipping ON TIME is preferred but can flex 1-2 weeks
shipping with deliverable C is desired but droppable
shipping with full polish is the most droppable
```

When the planner has to break something, this priority order tells it
*which* constraint to relax. Without explicit priorities, the project
relaxes whichever constraint is loudest, which is usually the wrong one.

## The classic PM triangle

The famous scope/time/cost/quality triangle is the canonical example of
interdependent constraints:

```
fix scope + time → cost varies (probably grows)
fix scope + cost → time varies (probably grows)
fix time + cost → scope varies (probably shrinks)
fix everything   → quality breaks silently
```

Pretending you can fix all four is the canonical project failure. Naming
which three you've fixed and which one is the absorbing buffer is the
constraint-based move.

## Dependencies as relationships

Most project plans treat dependencies as fixed orderings ("A before B").
A constraint-based view treats them as relationships:

```
B requires A's API contract  (not all of A)
B can start when A reaches checkpoint X
B's deadline shifts if A's checkpoint X slips
B can run partially in parallel with A's late stages
```

This is the difference between sequential planning and critical-path
planning. It surfaces *what part* of each upstream dependency you need
and *when*, which usually opens parallelism that a sequential plan
hides.

## Important concepts

### Pinned constants

Some values must not move regardless of what else changes. These are the
project's hard constraints made explicit: regulatory deadlines, customer
commitments, executive promises, brand obligations. Name them up front.
When something has to give, it cannot be one of these.

### Failure modes at the extremes

For each soft input, name what breaks at min and max:

- **Scope too small** → deliverable doesn't meet stakeholder intent
- **Scope too big** → timeline collapses, team burns out
- **Speed too high** → quality cliff, rework debt
- **Speed too low** → opportunity cost, stakeholder confidence erodes
- **Cost too low** → resourcing failure, key people leave
- **Risk too low** → over-validation, never ship
- **Risk too high** → ship-and-pray, large blast radius if wrong

Knowing the extremes lets you find the safe operating range.

## Constraint-based PM vs schedule-based PM

Schedule-based PM says:

```
Here is the Gantt chart.
This task takes 5 days, then this one takes 3.
Total: 28 working days, ship March 31.
```

Constraint-based PM says:

```
Here are the hard constraints.
Here are the soft inputs we're tuning.
The plan emerges from the constraints; the dates are derived, not
declared.
```

The Gantt chart is a *projection* of a constraint model, not the model
itself. Treating the chart as the model is the canonical project failure
mode that leads to plans nobody believes.

## In practice

A constraint-based project plan usually defines:

```
hard pins (regulatory, contractual, brand)
soft inputs (scope, speed, quality, cost, risk, coordination, engagement)
priority ordering when something has to give
dependency relationships, including which PART of each upstream
critical-path identification
slack budgets per phase
failure-mode trigger conditions
```

The goal is not "predictable delivery." It is "a plan that remains valid
under changing conditions" — projects whose model survives contact with
the real world.
