---
name: docs-diataxis-audit
description: >-
  Classifies every existing documentation page into exactly one of the four Diátaxis modes — tutorial, how-to, reference, explanation — flags pages that MIX modes (the signature documentation failure), and finds the missing quadrants per surface, grounded in the Diátaxis compass (action vs cognition, acquisition vs application). Read-only: it diagnoses, it does not rewrite. Use to audit a docs site, a docs/ tree, or pasted pages for mode hygiene and coverage gaps. Triggers on "diataxis audit", "documentation audit", "classify the docs", "what kind of doc is this", "tutorial vs how-to vs reference", "are these docs mixing modes", "docs coverage gaps", "missing documentation", "doc taxonomy". NOT for writing the actual pages or splitting them (you do that after the audit), nor for prose-quality line edits (→ style-conformance) or API completeness checks (→ doc-surface-drift).
---

# Docs Diátaxis Audit

Diátaxis says there are exactly four kinds of documentation — tutorial (learning-oriented lesson), how-to guide (goal-oriented recipe), reference (information-oriented description), and explanation (understanding-oriented discussion) — and each serves a different user need at a different moment. The framework's central claim, quoted directly: "Crossing or blurring the boundaries described in the map is at the heart of a vast number of problems in documentation." The signature failure is therefore mode-mixing: a single page that tries to teach AND list every parameter AND explain the design rationale serves none of those needs well. This skill CLASSIFIES every page against the compass and DIAGNOSES the mixes and the gaps; it does not split, merge, or rewrite pages — you do that, page by page, after reading the verdict. Treat a pasted docs URL, a sitemap, or a `docs/` tree as a first-class target; "not in the repo" is normal and fine.

## When to use

**Do**
- Audit an existing docs set (site, `docs/` tree, or pasted pages) to classify each page into one Diátaxis mode.
- Hunt for mode-mixing — the page that teaches a lesson AND dumps a parameter table AND philosophizes.
- Map coverage: which surfaces (CLI / SDK / REST / MCP / dashboard / installer) are missing a whole quadrant.
- Produce a prioritized split-and-fill plan before anyone touches prose.

**Don't**
- Rewrite, split, or merge pages here — this is read-only diagnosis; act on the verdict afterward.
- Grade sentence-level prose, tone, or grammar (→ style-conformance).
- Check whether every endpoint/flag is documented at all (→ doc-surface-drift).
- Define the single ideal onboarding path (→ golden-path).

## Procedure
1. **Gather the inventory.** Enumerate every page: walk the `docs/` tree, parse the sitemap, or take the pasted URLs/markdown. Record a stable identifier (path or URL) for each.
2. **Detect the mode per page** from textual signals, assigning the compass coordinates (action vs cognition × acquisition vs application):
   - **Tutorial** (action + acquisition): imperative numbered lesson, "we will build…", a guaranteed concrete result, hand-holding, no choices offered.
   - **How-to** (action + application): goal-oriented, "to do X, do Y", assumes competence, addresses a real task, offers conditional branches.
   - **Reference** (cognition + application): flat describe-only structure — parameter tables, flags, schemas, return values; consistent, exhaustive, no narrative.
   - **Explanation** (cognition + acquisition): discursive "why/background", design rationale, trade-offs, history; nothing to type.
3. **Flag mode-mixing.** Mark any page exhibiting MORE THAN ONE mode and name the specific blended modes (e.g. "tutorial + reference: a getting-started lesson interrupted by a full config table"). These are the priority defects.
4. **Build the quadrant-coverage matrix** per surface: rows = surfaces, columns = the four modes, cells = ✓ (present, cite the page) / gap (missing) / cite. Reveals whole quadrants no surface offers.
5. **Prioritize fixes.** Split mixed pages first (highest harm, quoted boundary claim applies), then fill missing quadrants on the highest-traffic surfaces. Output a ranked verdict, not a flat list.

## Output
```
## Per-page classification

| Page (path/URL)              | Detected mode | Signals                                              | Mixing? (which modes)        | Recommended action                          |
|------------------------------|---------------|------------------------------------------------------|------------------------------|---------------------------------------------|
| docs/getting-started.md      | Tutorial      | numbered steps, "you will build", guaranteed result  | + Reference (config table)   | Split: move config table → reference page   |
| docs/cli/deploy.md           | How-to        | "to deploy to staging, run…", branches by env        | clean                        | Keep as-is                                  |
| docs/sdk/api.md              | Reference     | flat method table, params, returns, no narrative     | clean                        | Keep; cross-link from how-to                |
| docs/concepts/auth-model.md  | Explanation   | "why tokens expire", trade-offs, no commands         | + How-to (embedded curl)     | Split: extract "rotate a token" → how-to    |
| <pasted URL>/quickstart      | Tutorial      | hand-held lesson                                     | + Explanation (why-asides)   | Move rationale → explanation; keep lesson   |

## Quadrant-coverage matrix

| Surface    | Tutorial            | How-to              | Reference           | Explanation         |
|------------|---------------------|---------------------|---------------------|---------------------|
| CLI        | ✓ getting-started   | ✓ cli/deploy        | gap                 | gap                 |
| SDK        | gap                 | ✓ sdk/usage         | ✓ sdk/api           | ✓ concepts/auth     |
| REST API   | gap                 | gap                 | ✓ openapi ref       | gap                 |
| MCP server | gap                 | gap                 | gap                 | gap                 |
| Dashboard  | ✓ tour              | gap                 | n/a                 | gap                 |
| Installer  | gap                 | ✓ install guide     | ✓ flags ref         | gap                 |

(✓ = present, cite the page · gap = missing · n/a = not applicable to surface)

## Verdict (prioritized)
1. SPLIT (do first): getting-started.md and auth-model.md mix modes — each violates the Diátaxis boundary and serves neither need well.
2. FILL high-traffic gaps: REST API has no tutorial or how-to; this is the most-trafficked surface — add both.
3. FILL coverage holes: MCP server has zero docs across all four quadrants — scaffold reference first, then a how-to.
4. Defer: dashboard explanation (low impact).
```

Failure mode: relabeling pages with mode tags while leaving the mixed pages un-split — a page tagged "tutorial" that still carries a full reference table hasn't been fixed, only labeled; the boundary the framework warns about is still crossed.

Sources: Diátaxis framework — https://diataxis.fr/ (Daniele Procida); the four modes (tutorials, how-to guides, reference, explanation) and the two-axis compass (action ↔ cognition, acquisition ↔ application); boundary-crossing failure claim quoted from https://diataxis.fr/.
