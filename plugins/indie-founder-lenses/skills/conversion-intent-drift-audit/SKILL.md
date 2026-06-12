---
name: conversion-intent-drift-audit
description: Audit conversion-altitude drift across MANY landing / marketing pages on a mature site. Pairs landing-altitude-naming on each page with cross-page pattern detection — which pages that should name an outcome now lead with a feature grid? which campaign pages drifted to a different altitude than the home page? where did a CTA pile-up turn an outcome page into an action page? For mature-site phase.
---

# Cross-page conversion drift audit

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a Conversion Lens.md` (mature-site phase).

## Procedure

1. **Enumerate target pages.** Glob for marketing / landing / campaign pages and routes in the project (`marketing/`, `landing/`, `(marketing)/`, home and alt-landing routes). If pages live outside the repo, accept a pasted set or a list of URLs.
2. **For each, name the current altitude and the intended altitude.** The intended altitude is *what the page should be organized around given who lands there*; the current is *what it actually leads with*. Run `landing-altitude-name` per page.
3. **Find the drift patterns:**
   - Which pages that *should* name an outcome now lead with a feature grid?
   - Which campaign / alt-landing pages drifted to a different altitude than the main page, so the same product reads differently per entry point?
   - Which pages accreted competing CTAs until an outcome page now reads as an action page?
   - Which never had a stated visitor at all — default = feature altitude, accidentally?
   - Which pages have *more* altitude clarity than expected (positive drift worth copying)?
4. **Surface the systemic pattern**, not per-page findings. Per-page drift is uninteresting; *root causes that produce drift across the site* are the finding (e.g. "every new campaign page starts from the feature-grid template").

## Output

```
Pages audited: <N>

Drift patterns:
  1. <pattern>: <N pages> — <example: "campaign pages lead with a feature grid while home leads with the outcome">
  2. <pattern>: <N pages> — <example: "outcome heroes buried under a CTA bar that reads action-first on skim">
  ...

Root causes:
  - <pattern → cause>: <e.g., "new pages are cloned from the feature-grid template; nobody re-grounds them on who lands">
  - …

Recommended next step:
  Which ONE page to re-ground first (highest-leverage fix), with file:line / route and what to change about its organizing altitude.
```

The audit's value is in the pattern, not the per-page list. If the report becomes a long list of individual pages, you've under-aggregated — re-cluster. Name the single highest-leverage page to re-ground; don't hand back a site-wide rewrite plan.
