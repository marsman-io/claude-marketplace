# Solving an agentic product problem means moving around the triangle

A good PM process for an indie builder is not just analytical,
intuitive, or operational. It needs all three.

When approaching a real agentic product problem — a vibe-coded feature,
an agent-built diff, a confusing UI change, a failing demo path, or a
black-box implementation that may not match intent — it helps to move
between three modes of thinking: **direct perception**, **systemic
thinking**, and **embodied action**. Each mode reveals something
different. Each also has a failure mode when used alone.

## 1. Direct perception: look at the artifact itself

Start by noticing what is actually there.

Before reaching for frameworks or the agent's explanation, inspect the
artifact: the diff, the screen, the route, the prompt, the issue, the
test output, the log, the demo path. What does the product now lead
with? What changed? What stayed untouched? Where does the implementation
seem to understand the intent, and where does it seem to have guessed?

This is the mode of observation, intuition, and presence. It is
especially important with agents because many misses are *felt* before
they are explained. A summary can sound complete while the product
still fails the use case. Tests can pass while the interaction says the
wrong thing.

Direct perception keeps you close to reality, not the agent's report
about reality.

**Failure mode — impressionism.** If you only rely on what something
feels like, you risk mistaking your own anxiety, mood, or favorite
narrative for truth.

## 2. Systemic thinking: make a model

Once you have observed, step back and model.

What pattern explains what you are seeing? Is this an intent problem? A
context problem? A scope problem? A data-model leak? A verification
problem? A prompt that specified output but not outcome? A design
surface where the implementation is correct but the hierarchy is wrong?

This is the mode of frameworks, abstractions, constraint maps, and
altitude naming. It turns scattered observations into something you can
reason about.

Systemic thinking helps avoid treating symptoms as causes. Instead of
"the agent wrote bad code," you might realize that the prompt never
specified the intended user. Instead of "the UI feels off," you might
realize the screen is organized around implementation state when the
intent is a decision the user needs to make.

**Failure mode — over-abstraction.** If you only think in models, you
can become detached from the artifact. You may produce elegant
explanations that do not improve the product.

## 3. Embodied action: intervene and watch what happens

Agentic product problems are not solved only by thinking. They are
solved by making a small move and observing the result.

Rewrite one acceptance criterion. Add one screenshot check. Cut one
scope branch. Re-pin one hard constraint. Ask the agent to verify the
demo path. Run the flow yourself. Change one prompt paragraph. Remove a
feature that is pretending to be priority. Watch what happens.

This is the mode of experiment, feedback, and iteration. It turns ideas
into contact with reality.

Embodied action is where PM judgment becomes useful to a solo builder.
Many answers only appear once you make a move. The act of intervening
exposes what the product and the agent are actually sensitive to, which
is rarely what the task summary implied.

**Failure mode — thrashing.** If you only act, you may keep prompting,
patching, and reshuffling without understanding why. You can chase agent
reactions, optimize locally, and mistake activity for progress.

## The best product process moves between all three

Strong product judgment usually moves around the triangle:

**Notice reality → model it → intervene → observe feedback → revise the model.**

Or more simply:

**perception → abstraction → action → feedback.**

You look closely at what the agent actually produced. You form a model
of what is happening. You make a small intervention. You observe what
the intervention reveals. Then you update your understanding.

The key is not to pick one mode as the "right" way to PM. The key is to
keep circulating.

When you feel lost, return to perception: *what is actually present in
the artifact?*

When the work feels messy, move to abstraction: *what model explains
this mismatch?*

When the thinking gets stuck, move into action: *what is the smallest
intervention that will teach me something?*

Agentic product work becomes clearer when it is seen, modeled, and
tested. Good PM judgment comes from the movement between these modes,
not from any one of them alone.
