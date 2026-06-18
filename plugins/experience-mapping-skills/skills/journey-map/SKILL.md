---
name: journey-map
description: >-
  Maps ONE developer actor, ONE scenario, ONE goal across the adoption funnel
  (discover → install → authenticate → first-success → integrate → operate/debug
  → upgrade → advocate), with a Channel/Touchpoint lane that names which surface is
  in play at each step AND the HANDOFFS between surfaces (docs→CLI→dashboard) —
  because that's where multi-surface developer experiences break — plus an emotion
  line plotted against concrete signals (auth setup, cryptic errors, version
  mismatch). Use when you need to find where a real developer's experience snaps
  in a single linear narrative. Triggers on "journey map", "map the developer
  journey", "onboarding journey", "where does the developer experience break",
  "emotion curve across our tool", "first-run experience map", "trace the adoption
  funnel". NOT for the product-agnostic baseline workflow (use experience-map), and
  NOT for the org-side backstage view of the same journey (use service-blueprint).
---

# Journey Map

A journey map follows ONE actor (first-time integrator, platform SRE, evaluator) through ONE scenario toward ONE goal, phase by phase across the adoption funnel. For a multi-surface dev tool the load-bearing lane is Touchpoints & Channels: it names which surface (CLI, SDK, REST, MCP, dashboard, docs, installer) the developer is on at each step and — critically — the HANDOFFS between them. Journeys rarely break inside a surface; they break at the seams (docs say one thing, the CLI flag is named another; auth set up in the dashboard isn't picked up by the SDK). Pairing those handoffs with an emotion line anchored to concrete signals (time-to-first-call, a cryptic error, a version mismatch) turns vague "onboarding is rough" into a located, fixable rupture. One actor, one scenario, one map — branches get their own.

## When to use

**Do**
- Use after you have a baseline (experience-map) and a real actor + scenario to trace.
- Use to locate the seam where confidence collapses (usually a surface handoff).
- Use verbatim quotes and concrete signals; anchor every emotion dip to evidence.

**Don't**
- Don't blend two actors or two scenarios into one map — split them.
- Don't map alternate routes inline; a branch is a separate journey map.
- Don't go product-agnostic here (that's experience-map) or org-side (service-blueprint).

## Procedure
1. Fix the header: Actor (one role) / Scenario (one situation) / Goal + Expectations / tool version + date. Cite where the actor comes from (interview, persona doc, pasted transcript).
2. Lay phases as columns across the funnel: Discover → Install → Authenticate → First-success → Integrate → Operate/Debug → Upgrade → Advocate. Drop phases that don't apply; don't invent extras.
3. Fill Actions per phase (what the actor does), citing the surface action (a `--help` line, an endpoint, a docs URL, a pasted command).
4. Fill Mindset with verbatim quotes (interview, issue, review). No quote → mark "(inferred)".
5. Name Touchpoints & Channels per phase AND draw the handoff arrows between surfaces (docs→CLI→dashboard). Flag each handoff as smooth or broken with evidence.
6. Plot the Emotion line as a value per phase anchored to a concrete signal (auth setup time, a cryptic error text, version-mismatch message). Cite the signal.
7. Footer: Opportunities / Insights / Ownership (team) / Metrics (the DX KPI per phase).

## Output
```
Actor: <one role>   Scenario: <one situation>
Goal & expectations: <...>   Version: <x.y.z>   Date: <YYYY-MM-DD>   Source: <cite>

Phases →   Discover | Install | Authenticate | First-success | Integrate | Operate/Debug | Upgrade | Advocate
| Actions               | ...      | ...     | ...          | ...           | ...       | ...           | ...     | ...      |
| Mindset (verbatim)    | "..."    | "..."   | "..."        | "..."         | "..."     | "..."         | "..."   | "..."    |
| Emotion line (signal) | 🙂 (cite)| 😐      | 😣 auth      | 😀 1st call   | 😐        | 😠 cryptic err| 😟 drift| 😀       |
| Touchpoints & Channels| docs     | installer→CLI ⚠handoff | dashboard→SDK ⚠ | CLI    | SDK/REST  | logs→dashboard| upgrade | docs/social |

Footer:
  Opportunities: ...        Insights: ...
  Ownership: <phase → team>  Metrics: <phase → DX KPI, e.g. time-to-first-successful-call>
```
*If there is more than one actor or scenario on the page, or the emotion dips have no cited signal, it isn't a journey map — split it and redo steps 1 and 6.*
