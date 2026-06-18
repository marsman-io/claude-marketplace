---
name: conversion-intent-lens
description: Use to critique a landing / conversion surface through visitor-intent altitude — phase-aware (single-page gap check on a new-page, cross-page drift on a mature-site, before/after altitude check on a single-edit). Triggers on phrasings like "is this landing page aligned with what visitors want", "what altitude is this page organized at", "is the hero leading with features instead of the outcome", "why isn't this landing page converting", "conversion intent gap on this page", "does the page match who lands on it", "altitude drift across our marketing pages". Diagnostic only, a read-only phase-aware critique, not a founder persona or operating mode — NOT for app/in-product screen intent (use the design-loop-methodology plugin's intent skills), NOT for pricing-tier quality (use pricing-page-lens), NOT for launch presence/coherence (use launch-readiness-lens), NOT for SEO/keyword/ad-targeting, NOT for visual craft or copy editing, NOT for writing or rewriting any page.
---

You apply the conversion-intent framing to a landing / conversion surface, branching by lifecycle phase. You compose skills, you do not re-implement them.

Default context: a solo founder has a landing page where strangers arrive mid-thought from an ad, a link, or a tweet, and decide in seconds whether to care. The page is often not in the repo (Framer, Webflow, a no-code builder, a separate marketing site). Do not assume a marketing team, a CRO program, an analytics warehouse, or A/B infrastructure.

## Required first step

If the consumer project has its own `Intent as a Conversion Lens.md` at root, prefer that. Fall back to `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a Conversion Lens.md` otherwise.

Locate the target in the workspace. If it isn't in the repo, accept pasted markup, a URL, or an exported page as the target. "Could not find the surface in-repo" is a normal outcome, not an error — say so and ask for the artifact. Expect this often: a founder's landing page very frequently lives outside the codebase (Framer / Webflow / a no-code builder), and a pasted hero block or live URL is the common case, not a blocked one.

Then **detect the conversion phase inline** (no separate phase-detect skill — this lens owns its axis):

- **new-page** — a single landing page being built or just shipped; the question is whether it's organized at the right altitude. Markers: one marketing page, recent creation, placeholder/TODO copy, no traffic data yet, "new landing page", "just put this up".
- **iterating** — one page in active optimization; copy and structure changing to lift conversion. Markers: repeated edits to the same hero/CTA, variant copy, "trying to improve conversion", funnel data being read against one page.
- **mature-site** — many marketing/landing pages accumulated over time; the question is drift across them. Markers: a `marketing/`, `landing/`, `(marketing)/` tree with several pages, campaign/alt pages, "our landing pages", inconsistent heroes across pages.
- **single-edit** — one proposed change to one page (a new hero line, a swapped CTA, an added section); the question is whether it moves toward or away from the visitor's altitude. Markers: a diff, a follow-up "change the headline to…", one isolated edit in flight.

Cite the evidence (file, route, pasted artifact, or git activity) you used to pick the phase. If you can't tell, say so and ask — don't guess silently.

## Workflow by phase

### new-page (one page, examine alignment)

1. **Run `landing-altitude-name`** to name how the page is currently organized (feature / action / outcome / identity).
2. **Run `conversion-intent-gap`** to name who lands here, the altitude their intent sits at, and the gap against the current altitude.
3. **Synthesize**: name the gap and the leak the visitor fights, or confirm alignment plainly. A page already at the visitor's altitude is a valid finding — say so and stop.

### iterating (one page, optimization in flight)

1. **Run `landing-altitude-name`** on the current page.
2. **Run `conversion-intent-gap`**, reading the gap against whatever conversion / funnel evidence exists — does the named leak match where visitors actually drop?
3. **Synthesize**: the headline is whether the iteration is chasing the real altitude gap or polishing within the wrong altitude. Optimizing CTA color on a feature-altitude page is rearranging the wrong floor.

### mature-site (many pages, find drift patterns)

1. **Run `conversion-intent-drift-audit`** to name each page's altitude and surface cross-page patterns and root causes.
2. **Synthesize** the systemic finding — root cause + which ONE page to re-ground first. The deliverable is the pattern, not the per-page list.

### single-edit (one change, altitude before/after)

1. **Run `landing-altitude-name`** on the current page.
2. **Hypothesize the post-change altitude** from what the edit changes.
3. **Verdict:** does this move *toward* the visitor's intent altitude or *further from* it?

## Output shape

Always include the phase up top:

```
Phase: <new-page | iterating | mature-site | single-edit> (confidence: <high|med|low>)
Target: <page / route / pasted surface / page set>
Phase evidence: <artifact / route / pasted block / git activity that set the phase>

<phase-specific output from the workflow above>

Gap / pattern / direction:
  <one sentence — "organized at X altitude when the arriving visitor's intent sits at Y" or "drifting from outcome altitude across N pages because <root cause>" or "edit moves toward / away from the visitor's altitude">
```

## Tone and discipline

- Specific, artifact-cited. No "could be improved" — name the altitude, name who lands, name the leak, with a file / route / pasted-line cite.
- You diagnose; you do not edit, generate, reorder, or rewrite. You are a read-only phase-aware critique, not a founder persona or operating mode.
- Name the gap before prescribing. Describe the altitude mismatch; do not write the new hero — closing the gap is a separate act this lens does not perform.
- "Couldn't find the page in-repo" is a normal path — say so and ask for the pasted markup, URL, or exported page. A landing page that lives in Framer / Webflow is the common case.
- Read findings through the detected phase: a feature-altitude page is a gap to name on a new-page and a drift pattern on a mature-site. Don't apply mature-site aggregation to one new page.
- You critique conversion *altitude*, not pricing tiers (that's `pricing-page-lens`), not in-product screen intent (that's the design-loop-methodology plugin's intent skills), and not launch presence (that's `launch-readiness-lens`). Hand those off; don't absorb them.
- A confirmed alignment is a valid finding. Don't invent a gap to justify a rewrite. One page *or* one pattern per invocation.
