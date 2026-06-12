# What "launch ready" actually means

A solo founder asks "is it ready to launch?" and hears it as a question
about one thing — usually the product, sometimes the landing page. But a
launch isn't a moment on one surface. It's the first time a stranger runs
the *whole* path: they arrive, they understand the offer, they decide to
pay, they sign up, and somewhere a system records that any of it
happened. Readiness is a property of that path holding together end to
end, not of any single screen being polished.

So this doc encodes one idea: **launch readiness is presence plus
coherence across the four founder surfaces — read at the phase you're
actually in.** It does not judge whether the pricing is *good* or the
landing page *converts*; other lenses own that depth. It asks the prior
question those lenses assume: are the four surfaces all there, and do they
tell the same story to the same stranger?

## The four surfaces, as a path

The four surfaces are named once in `Founder surfaces.md`; this lens reads
them as an ordered path a single visitor walks:

1. **Landing page** — they arrive and learn the promise: who it's for,
   what changes, the one action to take.
2. **Pricing** — they decide what to pay and why.
3. **Onboarding** — they sign up and reach first value.
4. **Analytics / event wiring** — the founder finds out any of it
   happened.

Presence is the cheap half: does each surface exist in some form the
visitor can actually reach? A pricing page nobody links to is absent even
if the file is in the repo. An onboarding flow that dead-ends before first
value is present-but-broken, which reads as absent to the visitor.

## Coherence is the half founders miss

Each surface can be individually fine and the launch still not ready,
because the surfaces disagree. Coherence is whether the *same* promise,
the *same* names, and the *same* primary action survive from one surface
to the next:

- The landing headline promises one outcome; the pricing tiers are named
  for a different one. The visitor arrives wanting A and is asked to buy
  B.
- The landing call-to-action says "Start free"; onboarding immediately
  asks for a card. The action the page promised isn't the action the next
  surface performs.
- Three plans are named on the pricing page; onboarding only knows about
  two. The tier the visitor picked doesn't exist on the other side.
- The landing page's hero CTA, the pricing CTA, and the signup button are
  three different verbs for the same step. The path reads as three
  products, not one.
- Every surface is built, and the analytics wiring tracks none of the
  transitions between them — so the founder will launch blind to exactly
  the handoffs most likely to leak.

A coherent launch is one where a visitor never has to *re-understand* the
product when they cross a surface boundary. Incoherence is almost always
invisible from inside one surface — it only appears when you walk the
boundary between two. That walk is what this lens does.

## The four launch phases, and how readiness reads in each

"Ready" is not one bar. The same surface gap is fatal in one phase and
irrelevant in another. This lens detects which of four phases the launch
is in, then reads readiness through that phase:

- **Pre-launch.** Nothing is public yet; surfaces are being assembled.
  Readiness here means *presence* — does each of the four surfaces exist
  in at least a first form, and is the path walkable start to finish? A
  missing surface is the headline finding. Coherence gaps are worth
  naming but not yet blocking; the surfaces are still moving.

- **Soft-launch.** A small, known audience can reach the path (a waitlist,
  a few invites, a beta). Now *coherence on the core path* is the bar:
  does the one visitor who arrives get a single consistent story from
  landing through first value? Presence is mostly settled; the findings
  shift to cross-surface disagreement and to whether analytics can even
  see the soft cohort move through.

- **Launch.** The path is open to cold traffic at volume. Readiness means
  *the whole path holds under strangers* — every surface present, the
  promise coherent end to end, and the analytics wiring actually emitting
  on each transition so the founder isn't flying blind on day one. This is
  the phase where an untracked checkout or a card-wall behind a "free" CTA
  is a launch-blocking finding, not a polish note.

- **Post-launch.** Traffic is flowing and the question changes from "is it
  ready" to "where is the path *leaking*." Readiness here is read against
  evidence: which surface transitions have events, which transitions show
  drop, and which incoherence the live funnel is now confirming. The
  finding points at the leakiest boundary, not at the existence of
  surfaces that traffic has already proven exist.

The phase doesn't change *what* the four surfaces are. It changes which
gap is the headline and which is noise.

## Why this is a perception pass, not a one-time checklist

The design-loop methodology frames all product work as a **perception
cycle — perception, abstraction, action, feedback** — rather than a
one-time gate, and pairs it with a **lifecycle** view where the same
surface reads differently depending on how mature the work is. This lens
borrows both moves directly (the lens itself stays a single read-only
diagnostic — it is not a loop or an orchestrator). The four phases above
are a launch-shaped lifecycle: the same four surfaces, read against rising
stakes. And readiness is not a box you tick once — it's the *perception*
step of that cycle. You check presence
and coherence, you act on the leakiest gap, you watch the analytics
feedback, and you check again. Post-launch is just pre-launch's question
asked with evidence instead of guesses.

That's why this lens diagnoses and hands off rather than fixes. It is the
perception pass: it tells you which surface is absent, which boundary is
incoherent, and at this phase which of those is the one that matters —
then hands pricing depth and landing-conversion depth to the lenses that
own them.

## The procedure

When you're actually assessing launch readiness, work in this order:

1. **Detect the phase** — pre-launch / soft-launch / launch / post-launch.
   It sets which gap is the headline.
2. **Establish presence** — locate each of the four surfaces (in-repo or
   pasted). A surface that exists but can't be reached is absent.
3. **Walk the boundaries for coherence** — landing→pricing, pricing→
   onboarding, and analytics across all transitions. Coherence lives on
   the boundary, not inside a surface.
4. **Read findings through the phase** — a coherence gap that's a note in
   pre-launch is a blocker at launch.
5. **Hand off depth** — pricing-quality questions go to the pricing lens,
   landing-conversion questions go to the conversion-intent lens. This
   lens reports presence and cross-surface coherence only.
6. **Name the single leakiest gap** for the current phase as the next
   step. Not a launch plan — the one boundary to fix first.

## The test

A ready launch survives a single stranger walking it out loud. Imagine one
visitor narrating the path: "I landed and I think this is for me… the
price for that is here… I clicked start and now I'm…". If at any boundary
the narration stutters — they expected one thing and got another, or the
product asks them to re-learn what it is — that's the incoherence. If the
founder couldn't tell you afterward where the visitor dropped, that's the
analytics gap. Readiness is when that walk is boring: no surprises at any
boundary, and a record of every step.
