# Pricing as a Decision Surface

A pricing page is not a list of plans. It is the **decision surface**
where a visitor with a problem decides what to pay, and why — which tier
fits them, what the next tier buys, and whether the price is anchored to
anything they understand. Most pricing pages are written as catalogs.
This doc reframes pricing as a *decision* to be designed, and gives the
vocabulary the pricing lens uses to critique it.

The reframe borrows directly from **constraint-based design / project
management** (see the sibling `Constraint-based project management.md`
in `project-loop-methodology`, and `Constraint-based design.md` in
`design-loop-methodology`). That body of work models a system not as a
fixed command but as a set of **relationships** — values that are
**pinned** (must not move) and values that **flex** (preferred, but
negotiable when pressure rises). This doc takes that one idea — *pinned
vs flexes* — and recasts it onto pricing. It does not copy the parent;
the parent is about scope, fidelity, risk, and review effort on an agent
task. Here the constraints are tiers, prices, gates, and the path to
checkout, and the "pressure" is a stranger deciding whether to pay.

## The core move: pinned vs flexes, on a pricing page

Every pricing page is, whether the founder said so or not, a set of
constraints. Some of them are **pinned** — load-bearing decisions that
the whole page leans on, that must not silently drift. Some of them
**flex** — knobs the founder is free to tune as they learn what converts.

A healthy pricing page knows which is which. A drifting one has let a
pin quietly become a flex (the anchor moved and nothing else was
re-decided) or frozen a flex into a pin (a price set on day one is now
treated as untouchable for no reason anyone remembers).

**Typically pinned** (move one of these and the rest of the page has to
be re-decided):

```
the named buyer each tier is for
what the anchor tier is anchored to (a competitor, a cost, the next tier)
the single primary action per tier (the CTA)
what is given away free vs what is the first paid gate
the promise the landing page already made about price
```

**Typically flexing** (tune these as you learn, without re-deciding the
page):

```
the exact dollar amounts
how many tiers
which features sit on which tier
billing period framing (monthly vs annual default)
the order and grouping of the feature rows
```

The point is not that the left column is forbidden to change. It is that
**changing a pin is a re-decision of the whole surface, and changing a
flex is a tweak.** A pricing page that treats a pin like a flex — moving
the anchor and calling it "just a copy change" — is the canonical
drift this lens exists to catch.

## What "decision surface" means

A catalog answers *what do you sell?* A decision surface answers *which
one is for me, and what do I lose by picking the cheaper one?* The
difference shows up in five places:

### 1. The named buyer per tier

A tier exists for someone. "Pro" is not a buyer; "a freelancer billing
clients" is. When every tier is for "you," the visitor has to do the
sorting the page should have done. **Pinned**: who each tier is for. If
that moves, the gating and the CTAs usually have to move with it.

### 2. The anchor

A price means nothing alone. It means something *against* a reference —
the tier above it, a competitor's plan, the cost of doing it manually,
the salary of the person it replaces. A page with no anchor leaves the
visitor to guess whether \$29 is cheap or dear. **Pinned**: what the
anchor tier anchors to. Quietly losing the anchor (it was a struck-out
"\$99" last month, now it's just "\$49") is a pin silently becoming a
flex.

### 3. The first paid gate

The most important line on the page is the one between free and paid —
*what is the first thing a visitor must pay to do?* If that gate sits on
a feature nobody reaches in their first session, the page converts
nobody. If it sits on the core value, the free tier is a demo, not a
giveaway. **Pinned**: where the free→paid gate falls.

### 4. The single primary action per tier

Each tier should have exactly one thing it wants the visitor to do.
Three equally-weighted buttons is no decision designed at all — the page
has pushed the decision back onto the visitor. **Pinned**: one primary
action per tier. (Borrowed from the budget framing in the sibling
plugins: a mechanism that does two jobs is the finding. A CTA that is
both "start free" and "talk to sales" with equal weight is doing two
jobs.)

### 5. Coherence with the promise upstream

Pricing does not begin at the pricing page. The landing page already
made a promise about who this is for and, often, roughly what it costs
("simple pricing," "free to start," "\$X/mo"). If the pricing page
contradicts it — a "free" CTA that lands on a card wall, a "simple"
promise meeting four tiers and an add-on grid — the decision breaks at
the boundary. **Pinned**: the price promise the landing page made.

## Failure modes at the extremes

Recast from the parent's "failure modes at the extremes." For each
flexing knob, name what breaks at min and max:

- **Too few tiers** -> distinct buyers are forced into one box; some
  overpay and churn, some underpay and the founder leaves money on the
  table.
- **Too many tiers** -> the decision surface becomes a spreadsheet; the
  visitor can't tell which is for them and bounces.
- **Price too low** -> the anchor implies the product is trivial;
  upgrade has nowhere to go.
- **Price too high** with no anchor -> the visitor has no reference to
  judge it against and assumes it's not for them.
- **Free tier too generous** -> nobody reaches the paid gate; the free
  tier *is* the product.
- **Free tier too thin** -> nobody experiences value before the gate;
  the free tier is a paywall with extra steps.
- **Gates too granular** -> the page reads as nickel-and-diming; trust
  drops before the decision is even made.

Knowing the extremes is how you find the safe operating range — and how
the lens decides whether a flex is mistuned or a pin has been broken.

## Pricing vs a price list

A price list says:

```
Here are the plans.
Here are the prices.
Pick one.
```

A decision surface says:

```
Here is who each tier is for.
Here is what the anchor is anchored to.
Here is the one gate between free and paid.
Here is the single thing we want you to do next.
The price is a flex; the decision design is the pin.
```

The list is a *projection* of the decision model, not the model itself.
Treating the list as the model — tuning dollar amounts while the buyer,
the anchor, and the gate go unnamed — is the failure this surface exists
to prevent.

## In practice

A pricing page critiqued as a decision surface resolves to:

```
pinned constraints (buyer per tier, anchor, free→paid gate, one CTA per
  tier, the upstream price promise)
flexing knobs (amounts, tier count, feature placement, billing framing,
  row order)
which pins have silently drifted into flexes (the drift finding)
which flexes have frozen into pins for no remembered reason
failure-mode triggers at the extremes
```

The goal is not a "correct" price. It is a pricing page whose *decision*
still holds after the founder has tuned the flexes a dozen times —
where the pins are intact and a visitor can still tell, in one read,
which tier is theirs and why.
