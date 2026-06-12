---
name: launch-readiness-walk
description: Walk the four founder surfaces for PRESENCE + CROSS-SURFACE COHERENCE at the detected launch phase — landing, pricing, onboarding, analytics. Reports each surface present/absent and each boundary coherent/incoherent, with artifact cites. Checks that the surfaces tell the same story to the same visitor; does NOT judge the quality of any one surface (pricing depth -> pricing-page-lens, landing conversion -> conversion-intent-lens). Assumes the launch phase has been detected. For pre-launch/soft-launch/launch/post-launch.
---

# Walk the four surfaces for presence and coherence

Read `${CLAUDE_PLUGIN_ROOT}/docs/Launch readiness.md`. Assumes the launch phase (pre-launch / soft-launch / launch / post-launch) has been detected and the four surfaces are named per `Founder surfaces.md`.

## Procedure

### 1. Establish presence

For each surface, locate it in-repo (glob/grep) or accept a pasted artifact / URL. A surface that exists but cannot be *reached* by a visitor (a pricing page nothing links to, an onboarding flow that dead-ends before first value) counts as absent.

- **Landing** — the arrival page and its promise. `index.html`, `app/`/`pages/` home or marketing route, `*.astro|tsx|vue|svelte` under `marketing/`/`landing/`/`home/`, or pasted markup / URL.
- **Pricing** — tiers and the path to checkout. `pricing`/`plans` route or component, a tiers config, or pasted table / Stripe products / URL.
- **Onboarding** — signup → first value. `auth/`/`signup`/`onboarding`/`welcome` routes, first-run / empty-state UI, or a pasted walkthrough.
- **Analytics** — does any of it get recorded. `track(`, `posthog`/`mixpanel`/`gtag`/`segment`/`plausible` calls, or a pasted snippet / list of configured events.

For each: present / absent / present-but-unreachable, with the cite (or note "external — asked for artifact").

### 2. Walk the boundaries for coherence

Coherence lives *between* surfaces, not inside one. Walk each boundary and check the same promise, names, and primary action survive:

- **Landing -> Pricing** — does the headline's promised outcome match what the tiers are named/sold for? Does the landing CTA match the pricing CTA?
- **Pricing -> Onboarding** — do the tiers the visitor can pick all exist on the signup side? Does a "free"/"start" CTA match what onboarding actually asks for (e.g. no surprise card-wall)?
- **Analytics across all transitions** — is each boundary above actually emitting an event (page view, signup, activation, checkout)? An untracked transition is an incoherence at launch.

For each boundary: coherent / incoherent, with the disagreeing artifacts cited.

### 3. Read through the phase

Weight findings by the detected phase: presence is the headline pre-launch; core-path coherence soft-launch; the whole path at launch (untracked/card-wall = blocking); the leakiest boundary read against live data post-launch.

**Hand off depth, don't absorb it.** Pricing-quality questions -> `pricing-page-lens`. Landing-conversion questions -> `conversion-intent-lens`. This walk reports presence + coherence only.

## Output

```
Phase: <pre-launch | soft-launch | launch | post-launch>
Target: <product / launch / surface set>

Presence:
| Surface    | Status                        | Evidence                                  |
|------------|-------------------------------|-------------------------------------------|
| Landing    | present                       | app/(marketing)/page.tsx hero + CTA       |
| Pricing    | present-but-unreachable       | Pricing.tsx exists, no nav/footer links   |
| Onboarding | present                       | app/onboarding/* signup -> first run      |
| Analytics  | absent                        | no track( calls on any transition         |

Cross-surface coherence:
| Boundary              | Status      | Evidence                                              |
|-----------------------|-------------|-------------------------------------------------------|
| Landing -> Pricing    | incoherent  | hero promises "team workspace", tiers named "for solo"|
| Pricing -> Onboarding | incoherent  | CTA says "Start free", signup asks for card first     |
| Analytics (all)       | incoherent  | no signup/checkout events — funnel is invisible       |

Out of scope (handed off):
  - Pricing quality -> pricing-page-lens
  - Landing conversion -> conversion-intent-lens

Single leakiest gap for this phase:
  <one boundary or missing surface to fix first>
```

The doc says: a ready launch survives one stranger walking the path out loud with no surprise at any boundary. If presence is fine but a boundary disagrees, the boundary is the finding.
