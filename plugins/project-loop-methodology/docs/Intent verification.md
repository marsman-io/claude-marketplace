# How to know the agents built what you meant

You delegated the build to a semi-black box. You can't read every line it
produced, you have no QA team, and the agent will tell you it's done
whether or not it is. So the central question of building this way isn't
"is the code good?" — it's *"does the thing in front of me do what I
actually wanted?"* That question has a discipline, and it is the most
important PM skill an indie builder has.

## Intent is the source of truth, not the code

When a human team builds, you can ask "why did you do it that way?" and
get a reason. A black box has no such conversation — its only honest
account of itself is its *behavior*. So you verify against two things and
not a third: the **intent** you stated, and the **behavior** you can
observe. You do not verify by reading the source and nodding, because
reading source you didn't write, at the speed delegation runs, is exactly
where false confidence comes from. If a claim about the build can't be
checked against stated intent or observed behavior, it isn't verified —
it's hoped.

## Acceptance criteria are a refusal mechanism

The leverage is almost all *before* generation. Before you hand a task to
an agent, write down what would make it correct — as concrete,
behavioral statements: given this, when that, then this observable thing
is true. A good criterion names a state you can see without asking the
agent what it meant: a response field, a screen, a stored value, an error
message, a redirect.

Their real job is not to describe success. It's to let you *refuse* a
result. A diff that technically runs but adds three behaviors nobody
asked for should be rejectable on sight, and criteria are what give you
the standing to reject it. Without them, every plausible-looking result
gets accepted, because "it seems to work" is the only bar you have left.

Write a few, not many — for a small task, three to seven: the happy path,
at least one failure path, at least one boundary or permission case. The
failure and boundary cases matter more than the happy path, because the
happy path is the one the agent already optimized for.

## Write criteria for the scariest thing first

Not every unknown is equal. Some assumptions, if wrong, sink the whole
feature; others are cosmetic. Rank what you're about to build by *how
badly a wrong answer hurts × how unsure you are it's right*, and spend
your verification on the top of that list. Build the thinnest slice that
tests the scariest assumption, prove it, and only then go wider.

The trap is the opposite instinct: the scary thing is unpleasant to look
at, so you write careful criteria for the easy, safe parts (the parts
that were going to be fine) and wave the dangerous one through. Verifying
the safe path *feels* like diligence and isn't. If you only have the
attention to deeply check one thing, check the one that would hurt most
to get silently wrong.

## The builder cannot grade its own work

The agent that wrote the code is the worst possible judge of whether the
code meets the intent — it will grade against its own interpretation,
which is the very thing in question. So the check has to come from
outside that interpretation: from the criteria you wrote *before* it
started, from behavior you observe yourself, or from a separate pass that
sees only the intent and the result, never the building agent's account
of what it did. "The tests pass" is not verification when the same agent
wrote both the code and the tests; it's the box certifying itself.

## Two failure modes: gap and drift

A built thing can miss intent in two directions, and they hide
differently.

- A **gap** is asked-for behavior that isn't there. Gaps are loud — a
  criterion is unmet, a path is missing. You find them by walking your
  criteria.
- **Drift** is behavior that's there but nobody asked for — an extra
  field, a silent default, a side effect, a scope the agent decided to
  expand into. Drift is quiet and far more dangerous, because nothing in
  your criteria points at it. You find drift only by asking the inverse
  question: *what does this do that I never requested?*

Checking for gaps is necessary. Checking for drift is what separates real
verification from a checklist.

## Vibe-checking has one honest use

Clicking around to get a feel for whether the thing works is legitimate
in **discovery** — when you're still building intuition about how it
should behave and don't yet have criteria worth writing. It is a disaster
as your standing QA: it's subjective, it doesn't repeat, and it rewards
confirmation. The mature move is to graduate — the moment a behavior
matters enough to protect, convert the vibe into a written criterion you
can check the same way every time.

## The loop

Verification isn't a final gate; it's the feedback edge of the build
loop. State intent → write criteria for the riskiest part → delegate →
check the result against the criteria *and* for drift → on a gap or
drift, decide whether to re-spec or accept → repeat. The output of a
failed check is rarely "the agent is bad." It's usually "my intent wasn't
specified tightly enough to be buildable" — which you fix by sharpening
the criteria, not by re-rolling the prompt and hoping.
