# Intent as a PM lens

## Intent

When solving a real project problem, do not begin with the deliverable,
the sprint plan, the OKR template, or the tooling. Begin by asking what
should become true for the stakeholders the project serves. What outcome
do they need? What capability do they unlock? What pain do they avoid?
What decision do they make differently? A good project direction starts
with intent: the desired change in the stakeholder's situation. From
there, constraints — time, budget, headcount, compliance, dependencies,
existing systems — become useful boundaries rather than the source of the
plan.

Once the intent and boundaries are clear, explore multiple possible plans
before committing to one. The answer might be a build, a buy, a fork, a
deprecation, a process change, a partnership, a smaller version, or
declining to do the project at all. Strong PMs do not simply decorate a
solution or fill in a Gantt template; they shape the possibility space
around a purpose, then make deliberate choices that move stakeholders
toward the intended outcome.

## Constraints

Constraints are not obstacles to delivery; they are the material delivery
works with. A strong PM pays attention to what must be true before
deciding what to build, in what order, by when: stakeholder availability,
team capacity, dependency latency, regulatory requirements, contractual
deadlines, brand commitments, budget envelope, opportunity costs, and
failure modes that the organization will not tolerate. These constraints
define the actual problem space, separating wishful planning from a plan
that survives contact with real teams, real customers, and real
calendars.

Constraint-based PM means learning to ask: What must this project
support? What must never happen? What conditions will it be delivered
under? What tradeoffs are already fixed? What can still vary? Once those
boundaries are clear, scope, sequencing, milestones, and stakeholder
contracts become more grounded — they are responses to the shape of the
problem rather than arbitrary choices.

## The PM knob framework

Many real project decisions feel overwhelming because they contain too
many possible options. A knob framework turns the problem into a small
set of meaningful variables. Each knob represents something the PM can
adjust:

```
Knob 1: Scope
How much of the problem are we trying to solve?

Knob 2: Speed
How fast does it need to deliver?

Knob 3: Quality
What level of polish / reliability does the outcome require?

Knob 4: Cost
What's the budget envelope — money, headcount, opportunity?

Knob 5: Risk tolerance
What happens if we ship something that doesn't work? How big is the bet?

Knob 6: Coordination overhead
How tightly does this depend on other teams / vendors / systems?

Knob 7: Stakeholder engagement
How much access / signoff do we need at each milestone?
```

The knobs are **interdependent**. Moving one moves others:

```
More scope
→ longer timeline
→ more coordination
→ more risk of mid-flight surprise

More speed
→ less polish
→ more rework later
→ less stakeholder review

Less risk tolerance
→ more validation
→ smaller scope per release
→ longer overall timeline
```

The framework gives you something to reason with. A vague problem like:

```
How should we run this initiative?
```

becomes:

```
We need a project with:
  Knob: Scope — medium (one customer segment, two surfaces)
  Knob: Speed — fast (3-month delivery)
  Knob: Quality — operational (good enough for one segment)
  Knob: Cost — low (one team, no new hires)
  Knob: Risk — medium (we can ship a smaller version if we have to)
  Knob: Coordination — low (don't need other teams)
  Knob: Stakeholder engagement — light (CEO check-in monthly)
```

That is a much more useful starting point. It gives the team something
to plan against.

## The altitude question

The PM equivalent of the design "altitude" question: how is the project
organized — and is that organization aligned with stakeholder intent?

- **Output altitude** — organized around what got shipped. Release notes,
  burndown charts, completion lists. "We delivered X."
- **Activity altitude** — organized around what people are doing. Sprint
  boards, calendar, Gantt charts. "Here is what the team is working on."
- **Outcome altitude** — organized around what should become true.
  OKRs, business value, stakeholder change. "Here is what changed for the
  customer."
- **Status altitude** — organized around current condition. Health
  dashboards, RAG status, blocker logs. "Here is where we are right now."

The canonical gap: a project organized at output or activity altitude
when stakeholder intent sits at outcome altitude. The team ships and
moves; the stakeholder says "but did anything change for our customer?"
That gap is invisible if you only look at activity dashboards. The
altitude question makes it visible.

A confirmed alignment between current altitude and intent altitude is a
valid finding. Not every project is misaligned.
