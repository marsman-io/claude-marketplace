# indie-founder-lenses

Four phase-aware diagnostic lenses for the surfaces a solo founder lives
on — launch readiness, pricing, landing-page conversion, and founder
focus. Read-only critics, not implementers — each detects its own phase
and produces a structured finding you can act on.

This is **not a loop and not a methodology.** There is no orchestrator,
no shared founder lifecycle, and no founder persona. Each lens is
independent: it owns its own phase axis, reads its own grounding doc,
fires on its own triggers, and never assumes another lens has run. The
lenses share only a small surface-vocabulary doc (`Founder surfaces.md`)
so they cross-reference the same terms.

This plugin is tuned for a solo founder / vibe-coder who ships their own
product. The surfaces it critiques — a landing page, a pricing page, an
onboarding path, the analytics wiring, a half-formed backlog — often
don't live cleanly in the repo Claude Code is pointed at. Every lens
therefore accepts a pasted artifact (markup, a URL, a pasted backlog or
roadmap) as the target, and treats "couldn't find the surface in-repo"
as a normal outcome, not an error.

Agents are auto-delegated probabilistically from their `description`, so
the matching lens often fires on the phrasings below — but auto-routing
is not guaranteed. You can always invoke a lens explicitly.

## Agents (lenses)

| Agent | Critiques | Phase axis |
|---|---|---|
| `launch-readiness-lens` | presence + cross-surface coherence before/around a launch | pre-launch / soft-launch / launch / post-launch |
| `founder-focus-budget` | a founder's backlog / commitments as a finite attention budget | scoping / committed / in-flight / reprioritizing / pivoting |
| `pricing-page-lens` | a pricing page as a decision surface | draft / live / iterating |
| `conversion-intent-lens` | a landing page's intent-to-conversion gap | new-page / iterating / mature-site / single-edit |

Each lens defines and detects its *own* phases — there is no single
shared founder lifecycle and no shared phase-detect skill.

## Skills (procedures)

Each lens owns its own walks / audits and detects its own phase inline —
there is no shared phase-detect skill. The skills, grouped by lens:

| Skill | Lens | When invoked |
|---|---|---|
| `launch-readiness-walk` | launch-readiness-lens | Walk the four founder surfaces for presence + cross-surface coherence at the detected launch phase; does not judge any one surface's quality |
| `founder-work-mode` | founder-focus-budget | Name a founder's work mode — searching / growing / sustaining — before walking the budget |
| `founder-focus-walk` | founder-focus-budget | Walk the five focus mechanisms on ONE bet against the outcome it claims (revenue / retention / activation) |
| `founder-focus-squint` | founder-focus-budget | Squint test on a roadmap / backlog — which bet still leads by actual spend, which dissolves, which screams without earning it |
| `founder-focus-audit` | founder-focus-budget | Cross-bet focus-drift detection across a whole roadmap (in-flight / pivoting) |
| `pricing-constraint-map` | pricing-page-lens | Map a pricing page into PINNED vs FLEXING constraints, then check each flex against the failure modes |
| `pricing-decision-walk` | pricing-page-lens | Walk a pricing page tier by tier as a decision surface — buyer, anchor, free→paid gate, single action, price-promise coherence |
| `pricing-drift-audit` | pricing-page-lens | Audit a LIVE pricing page being tuned for pin drift — a pin silently became a flex, or a flex froze into a pin (iterating) |
| `landing-altitude-name` | conversion-intent-lens | Name a landing surface's organization altitude — feature / action / outcome / identity |
| `conversion-intent-gap` | conversion-intent-lens | Check ONE landing page's gap between the arriving visitor's intent altitude and the page's actual altitude (new-page / iterating) |
| `conversion-intent-drift-audit` | conversion-intent-lens | Audit conversion-altitude drift across MANY pages on a mature site (mature-site) |

## Founder surfaces

The one shared doc, `docs/Founder surfaces.md`, names the four founder
surfaces as stable cross-referenced vocabulary — **landing page**,
**pricing**, **onboarding**, and **analytics / event wiring** — so every
lens points at the same terms. For each surface it states what artifact
represents it, where it typically lives, and that it *may* live outside
the repo (Framer / Webflow / Stripe / Linear / Notion), which is why the
lenses accept pasted markup or a URL.

```
${CLAUDE_PLUGIN_ROOT}/docs/Founder surfaces.md
```

## Conventions all lenses enforce

- **Read-only.** No `Edit`/`Write` tools. They diagnose; you intervene. Each agent body also states it in prose, because `Bash` can write — the read-only promise is held by discipline.
- **Phase-aware, per-lens.** Every lens detects its *own* phase first, then branches. There is no shared lifecycle to interpret.
- **Doc-grounded.** Each lens reads its grounding doc before executing.
- **Artifact-cited.** No finding without an artifact reference (file:line, a pasted block, or a URL).
- **Accepts external / pasted artifacts.** Founder surfaces often live outside the repo. A pasted page, a URL, or a pasted backlog is a first-class target; "not in-repo" is a normal path, not an error.
- **Anti-persona.** A lens is a read-only phase-aware critique, not a founder persona or operating mode. It will not role-play a founder, generate the surface, or rewrite it.
- **Single target.** One surface or one pattern per invocation.
- **No invented gaps.** A confirmed alignment is a valid finding.

## Override in your workspace

Each lens prefers a consumer workspace's *own* copy of its grounding doc
when one exists at the workspace root. Drop a tuned copy of a lens's doc
(or of `Founder surfaces.md`) at your workspace root and the matching
lens will use yours instead of the plugin's. Falls back to the plugin's
`docs/` otherwise.

## Layout

```
.claude-plugin/plugin.json
README.md
agents/
  launch-readiness-lens.md
  founder-focus-budget.md
  pricing-page-lens.md
  conversion-intent-lens.md
docs/
  Founder surfaces.md
  Launch readiness.md
  Founder focus budget.md
  Pricing as a Decision Surface.md
  Intent as a Conversion Lens.md
skills/
  launch-readiness-walk/SKILL.md
  founder-work-mode/SKILL.md
  founder-focus-walk/SKILL.md
  founder-focus-squint/SKILL.md
  founder-focus-audit/SKILL.md
  pricing-constraint-map/SKILL.md
  pricing-decision-walk/SKILL.md
  pricing-drift-audit/SKILL.md
  landing-altitude-name/SKILL.md
  conversion-intent-gap/SKILL.md
  conversion-intent-drift-audit/SKILL.md
```

## Install

```
/plugin install indie-founder-lenses@claude-marketplace
```

## License

MIT.
