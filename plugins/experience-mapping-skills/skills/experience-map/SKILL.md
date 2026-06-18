---
name: experience-map
description: >-
  Builds the product-agnostic baseline ("parent" experience map, NN/g) of how a
  developer accomplishes a goal TODAY — across DIY, gluing OSS, a competitor API,
  or hand-rolled scripts — BEFORE your CLI/SDK/REST/MCP surfaces enter the picture,
  so you can see the white space where your tool should slot in and which generic
  pain (auth sprawl, glue code, version drift) it must kill. Use when you need to
  understand the broader workflow and competitive baseline rather than critique a
  specific surface. Triggers on "experience map", "how do developers solve this
  today", "product-agnostic baseline", "map the broader workflow before our product",
  "where does our tool fit", "white-space analysis", "what's the status quo for
  this task". NOT for a specific persona+product journey through your own surfaces
  (use journey-map), and NOT for critiquing a single surface's DX (use
  dx-evaluation-skills).
---

# Experience Map

An experience map is the product-AGNOSTIC "parent" map (NN/g): it charts how a developer reaches a goal TODAY — duct-taping OSS, calling a competitor's API, copy-pasting curl, writing throwaway scripts — with NO product and NO persona in the frame. It matters because it surfaces the white space: the generic, recurring pain (auth sprawl across three CLIs, brittle glue code, version drift between SDK and API) that exists regardless of vendor. That pain is exactly what your CLI/SDK/REST/MCP should kill. Skip this and you design a product against an imagined workflow instead of the real one — and you build features into space a competitor already owns. The output is a baseline you measure every later journey-map against.

## When to use

**Do**
- Use at the start of discovery, before any of your surfaces exist or are decided.
- Use when comparing the status quo (DIY vs OSS vs competitor) to find where to enter.
- Use when the goal is broad ("get telemetry into a dashboard"), not a single tool.

**Don't**
- Don't name your own product anywhere on the map — that defeats the baseline.
- Don't attach a persona; this is role-agnostic (use journey-map for one actor).
- Don't critique a `--help` dump or an OpenAPI spec line-by-line (that's DX evaluation).

## Procedure
1. State the developer GOAL in one product-neutral sentence (e.g. "ship a change and verify it in production"). Cite the source: a pasted brief, an issue, a URL.
2. Inventory the options developers use TODAY: DIY, gluing OSS, a competitor API/SDK, hand-rolled scripts. Cite each (a repo, a docs URL, a pasted snippet). "Not in our repo" is normal — note it.
3. Lay out chronological PHASES as columns: Need → Evaluate options → Integrate → Operate. Keep phases generic to the goal, not to any tool.
4. For each phase fill rows: Actions (what they do), Thoughts (questions/doubts, verbatim where you have a quote), Emotions/friction (where it grinds — auth, glue, drift).
5. Mark every friction with evidence: a quote, a log line, a forum URL, a stack trace. No cite, no friction.
6. Collapse the friction into 3-7 generic pain points, then name the WHITE-SPACE opportunity each implies (which surface should own it) — without designing the surface.

## Output
```
Goal (product- & persona-agnostic): <one sentence>   Source: <cite>
Options surveyed today: DIY | gluing OSS | competitor API | scripts (cite each)

| Lane              | Need            | Evaluate options | Integrate        | Operate          |
|-------------------|-----------------|------------------|------------------|------------------|
| Actions           | ...             | ...              | ...              | ...              |
| Thoughts (quotes) | "..." <cite>    | "..." <cite>     | "..." <cite>     | "..." <cite>     |
| Emotions/friction | 😐 auth sprawl  | 😟 unclear fit   | 😣 glue code     | 😠 version drift |

Generic pain points (cited):
  P1 <pain> — evidence <cite>
  ...
White-space opportunities (pain → surface that should own it):
  W1 <pain P#> → CLI | SDK | REST | MCP | docs | installer  — kills <generic pain>
  ...
```
*If the output names your product, attaches a persona, or reads as prose instead of the phases×lanes matrix, it is not an experience map — redo steps 3-4.*
