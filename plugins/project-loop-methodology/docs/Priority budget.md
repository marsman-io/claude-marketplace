# How to arrive at priority clarity

Solo builders tend to treat priority as a pile of separate decisions:
should I build this next or that, is this issue urgent, what am I most
excited about right now. Made one at a time, those choices fight each
other, and you end up delegating a little of everything to your agents —
every task half-specified, nothing actually leading.

The fix is to stop thinking in decisions and start thinking in one
resource.

## Priority is a budget

You can only meaningfully attend to so many things at once. So can your
agents — they have finite context, and every task you keep in flight is
one more diff you have to read, one more behavior you have to verify and
hold in your head. Call that finite capacity the **priority budget**:
your attention, the agent context you can spend, the verification you can
afford, and the review depth you can sustain. Every task in flight draws
from the same pool. Spend too little on differentiation and everything
looks equally important (nothing leads, nothing ships clean). Spend too
much on one task and you starve everything else — including the one that
mattered.

Priority clarity isn't a setting you turn on. It's what's left over when
you've spent the budget cleanly. So the skill isn't "want it more," it's
"allocate a limited budget across a few mechanisms without overspending."

## Five mechanisms, one job each

Priority for a solo builder is spent through *how you delegate a unit of
work to an agent*. You have five mechanisms, and the discipline is that
each one does exactly one job:

- **Intent prominence** — what sits at the top of the issue, prompt, or
  acceptance note. The cheapest separator: does the intended user-outcome
  lead, or is the task just marked "urgent" with no named change?
- **Context allocation** — which files, docs, screenshots, traces, and
  prior attempts the agent receives. Context is finite per task; loading
  the whole app into a one-line fix is overspending.
- **Implementation focus** — how much surface area the agent is allowed
  to touch. A focused task that may edit three files is a different spend
  than "refactor wherever you see fit."
- **Verification coverage** — which tests, screenshots, demos, or manual
  checks prove the outcome actually happened. Proving *user behavior* is
  a bigger spend than proving the file changed.
- **Review cadence** — how closely and how often you inspect what comes
  back. Reading every line of every diff is itself a cost you're paying.

The most common failure is stacking. You put one task at the top of the
prompt AND hand it the whole codebase as context AND let it touch
anything AND demand full verification AND re-read every line on each pass.
That's five mechanisms spent on a single task, while every other task got
nothing. The "priority" one screams; the rest go silent — and you can't
tell whether it leads because it matters or just because it's loud.

One task, one mechanism — or two at most when context truly requires it.

## The mechanisms trade against each other

This is the part that turns five rules into a system. You can't move one
knob without it pulling on the others.

**Context allocation drains review cadence.** Loading rich context into
every task is your instinct, but the more context each task carries, the
more there is to read when the diff comes back — and the fewer tasks you
can actually review before you stop reading carefully. The moment you
have more richly-loaded diffs than you can read, context stops being a
signal: everything is "important enough to study" and nothing is *the*
one to study. A healthy week loads deep context onto fewer tasks than
your agents could technically run. The review attention to actually read
the output is the priority signal that survives.

**Verification coverage has exactly one meaning.** If every task gets the
same generic "tests pass," coverage now means "it ran" — i.e., nothing.
When a task *genuinely* needs proof that the user's behavior changed,
verification has no information left to carry. Spend deep verification on
the outcomes that would sink the product if they're silently wrong, not
on every task that touched a file.

**Intent prominence has exactly one meaning.** If every issue says
"critical" and none names the user change, prominence is decoration. So
when a task *genuinely* carries the outcome you're betting on, it can't
stand out. Spend prominence on the named change you can verify — not on
urgency words.

## Start from the target, not the tasks

Before you allocate, decide what kind of work mode you're in:

- A **discovery** mode (ambiguous idea, unknown user behavior) needs very
  little differentiation between bets — most tasks are small, parallel,
  roughly equal probes. Context and fast evidence matter more than broad
  implementation or deep review.
- A **delivery** mode (executing on validated behavior) needs a lot of
  differentiation at low slack — clear intent prominence, defined
  implementation focus, rising verification coverage on the paths that
  matter.
- An **operations** mode (steady-state, bugs, reliability, cleanup)
  groups tasks by area — small consistent review cadence, broad context
  reserved for the rare cross-cutting failure, most tasks flat.

Naming the work mode first means you're allocating toward a target
instead of chasing whatever feels urgent today.

## Consistency is enforcement, not a one-time decision

Allocating the budget well on one task is easy. The hard part is that
priority reads clearly only if the *same* allocation discipline holds
task over task. Solo, there's no one to keep you honest — so if each task
you spend the budget on a different whim, your work is sharp on one issue
and muddy on the next, which is worse than being uniformly mediocre.

That's why the rules belong somewhere durable — an acceptance-criteria
habit, a standing note of what each agent track is *not* allowed to
touch, a line in your `CLAUDE.md` about what verification a task must
carry before you call it done — rather than re-decided from mood every
time you open a new prompt.

## The procedure

When you're actually allocating priority across what to delegate, work in
this order:

1. Name the work mode and set how much differentiation it needs.
2. Spend intent prominence first — it's the cheapest and has no side
   effects. Make the named outcome lead the ask until the top three tasks
   read clearly.
3. If too much is crowded into "now" for prominence to differentiate,
   move that signal to context allocation (which task gets the real
   context) or to implementation focus (which task is allowed to range).
4. Pick one mechanism per task — deep context *or* deep verification,
   rarely both for the same task.
5. Hold deep verification in reserve for outcomes that would sink the
   product if wrong.
6. Hold deep review cadence in reserve for the tasks whose behavior you
   can't otherwise trust.
7. Step back. If every task is differentiated, remove your weakest
   separator and check whether priority reappears.

## The test

A clean set of priorities survives squinting. If you blur the labels, or
strip out the urgency words, you should still see the structure — what's
leading, what's secondary, what's a routine probe. If you can't, you've
under-spent (nothing leads) or overspent (every task competes for you at
once). Either way, the answer isn't to add more. It's to take something
away until one clear reading is left.
