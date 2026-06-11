# Intent as a PM lens for agentic product work

## Intent

When judging work produced by agents, do not begin with the ticket,
the implementation, the model's explanation, or the tool output. Begin
by asking what should become true for the intended user and for the
builder who delegated the work.

The builder may be the only explicit "stakeholder." That is fine. Name
two roles when possible:

- **Intent owner** — the person who knew what they wanted and delegated
  the work.
- **Intended user** — the person who must be able to understand, decide,
  complete, avoid, recover from, or trust something after the work lands.

A good product direction starts with intent: the desired change in the
user's situation. From there, constraints such as time, platform,
existing code, accessibility, model uncertainty, context limits,
deployment risk, and manual verification effort become useful boundaries
rather than a substitute for the idea.

The key product question is not "did the agent complete the task?" It
is "does the artifact now express the delegated intent?" An agent can
make a plausible change, pass tests, and still miss the product meaning.
This lens exists to expose that mismatch.

## Constraints

Constraints are not obstacles to product judgment; they are the material
the judgment works with. A strong product builder pays attention to what
must be true before deciding what to ask an agent to change: the target
user's context, the screen or workflow being touched, existing APIs,
data shape, deployment surface, quality bar, reversibility, and the
evidence available after the agent finishes.

Constraint-based PM in this setting means learning to ask:

- What must the result allow the user to do or understand?
- What must never break?
- Which assumptions did the agent have to infer?
- Which parts of the result can be verified from local artifacts?
- Which parts remain judgment calls because analytics, interviews, or a
  broad user base are unavailable?

Once those boundaries are clear, scope, sequencing, acceptance checks,
and follow-up prompts become responses to the shape of the problem
rather than arbitrary project-management ceremony.

## The PM knob framework

Many agentic product decisions feel overwhelming because the builder
has delegated to a capable but opaque worker. A knob framework turns the
problem into a small set of meaningful variables. Each knob represents
something the builder can adjust before or after delegation:

```
Knob 1: Scope
How much of the intended behavior should this pass cover?

Knob 2: Fidelity
How exact does the match to intent need to be: rough scaffold, usable
workflow, polished product surface, or production-safe behavior?

Knob 3: Evidence
What proof will count: tests, screenshots, demo path, diff inspection,
logs, acceptance checklist, or manual use?

Knob 4: Context budget
How much product intent, code context, prior attempts, and constraints
does the agent need in order not to guess?

Knob 5: Risk tolerance
What happens if the agent's interpretation is wrong? How reversible is
the change?

Knob 6: Integration surface
How many files, workflows, data contracts, prompts, or user paths does
this touch?

Knob 7: Review depth
How much human judgment is needed after the agent finishes?
```

The knobs are **interdependent**. Moving one moves others:

```
More scope
→ more integration surface
→ more hidden assumptions
→ more review depth

Higher fidelity
→ more evidence needed
→ tighter context requirements
→ less tolerance for agent improvisation

Lower review depth
→ smaller scope
→ stronger automated checks
→ more explicit acceptance criteria
```

The framework gives you something to reason with. A vague problem like:

```
Did the agents build the thing I meant?
```

becomes:

```
We delegated a change with:
  Knob: Scope — one checkout flow state, not the whole account system
  Knob: Fidelity — usable product behavior, not a throwaway scaffold
  Knob: Evidence — screenshot + happy-path test + diff inspection
  Knob: Context — issue intent, route file, existing component pattern
  Knob: Risk — medium; reversible behind one feature branch
  Knob: Integration — one route, one API call, one persisted field
  Knob: Review depth — human checks copy, flow, and edge case behavior
```

That is a much more useful starting point. It gives the builder and the
agent a shared object to inspect.

## The altitude question

The PM equivalent of the design "altitude" question: how is the work
organized, and is that organization aligned with intent?

- **Output altitude** — organized around what got produced. Commits,
  files changed, release notes, generated components. "The agent built
  X."
- **Activity altitude** — organized around what happened during work.
  prompts, task lists, agent logs, TODOs, issue transitions. "Here is
  what the agent did."
- **Outcome altitude** — organized around what should become true for
  the user. Acceptance checks, demo paths, user-visible behavior,
  before/after screenshots. "Here is what changed for the user."
- **Status altitude** — organized around current condition. Failing
  tests, blockers, known gaps, unresolved questions. "Here is where the
  work stands right now."

The canonical gap for agentic product work: the artifacts are organized
at output or activity altitude when the delegated intent sits at outcome
altitude. The agent changed files and reported progress; the builder is
left asking, "but can the user do the thing I meant?"

That gap is invisible if you only inspect the agent's summary. The
altitude question makes it visible.

A confirmed alignment between current altitude and intent altitude is a
valid finding. Not every delegated change is misaligned.
