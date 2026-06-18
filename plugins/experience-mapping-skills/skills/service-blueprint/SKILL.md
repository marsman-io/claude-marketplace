---
name: service-blueprint
description: >-
  Maps the ORG side of a journey (same phases, company perspective) to expose what
  happens behind the scenes and trace a developer-visible failure — a 500, a cryptic
  CLI error, an MCP timeout — to its backstage ROOT CAUSE (expired token, schema
  drift, registry outage), separated by the line of visibility into what the
  developer can observe (API responses, exit codes, dashboard, logs, status page)
  vs what they can't (services, queues, schedulers, MCP runtime, release pipeline).
  Use when you need to connect a frontstage symptom to its internal mechanism, one
  scenario per blueprint. Triggers on "service blueprint", "frontstage backstage",
  "trace this failure to its root cause", "what happens behind the scenes when",
  "blueprint the upgrade flow", "line of visibility", "why does this error happen".
  NOT for the user-facing emotion narrative of the journey (use journey-map), and
  NOT for the product-agnostic baseline (use experience-map).
---

# Service Blueprint

A service blueprint is the company-side counterpart to a journey map: same phases, but it looks down through the developer's experience into the machinery that produces it. For a dev tool the frontstage is mostly automated and self-service — human support is the exception, not the rule — so the real value is the chain below the line of visibility: which backstage service, queue, scheduler, MCP runtime, or release pipeline actually produced the symptom the developer saw. It exists to trace a concrete failure (a 500, a cryptic CLI exit code, an MCP timeout) to a concrete root cause (expired token, schema drift between SDK and API, package-registry outage). Without it, teams fix symptoms at the surface and the cause re-fires. One scenario per blueprint — first-integration and upgrade are different machines.

## When to use

**Do**
- Use when a specific developer-visible failure needs its backstage cause located.
- Use to map dependencies between surfaces and services (draw the arrows).
- Use one scenario; pick first-integration OR upgrade OR debug, not all three.

**Don't**
- Don't put emotions or quotes here — that's the journey map's job.
- Don't merge scenarios; a second scenario is a second blueprint.
- Don't omit the three divider lines; they are the structure, not decoration.

## Procedure
1. Pick ONE scenario and reuse the journey-map phase columns (Discover…Operate/Debug…Upgrade). Cite the journey map or scenario doc.
2. Top lane — Physical/Digital Evidence: every artifact the developer touches (CLI output, API responses, schemas, docs, installer prompts, log lines). Cite each (paste the line, the response body, the URL).
3. Draw the LINE OF INTERACTION, then Developer Actions (what the dev does at each phase).
4. Draw the LINE OF VISIBILITY, then Frontstage: automated/self-service responses (the API gateway returning a code, the docs site, the dashboard render); mark human support as exception only.
5. Draw the LINE OF INTERNAL INTERACTION, then Backstage: services, queues, MCP server runtime, build/release pipeline that execute the work.
6. Add Support Processes: auth/token issuance, rate limiting, package registry, telemetry, on-call.
7. Draw dependency arrows between cells; a double-headed arrow = codependency (SDK version ⇄ API version). Add a Metrics row (latency, error rate, MTTR) per phase.
8. For the target failure, trace the arrow chain from the Evidence cell down to the Backstage/Support cell that is the root cause; state it.

## Output
```
Scenario: <one>   Phases →  Discover | Install | Authenticate | First-success | Integrate | Operate/Debug | Upgrade
Source: <cite>

| Physical/Digital Evidence | CLI out / API resp / schema / docs / installer prompt / log line (cite each)        |
———————————————————————————— LINE OF INTERACTION ——————————————————————————————
| Developer Actions         | ...                                                                                 |
———————————————————————————— LINE OF VISIBILITY ———————————————————————————————
| Frontstage (automated;    | gateway code / dashboard render / docs serve   [human support = exception]          |
|  self-service)            |                                                                                     |
———————————————————————————— LINE OF INTERNAL INTERACTION —————————————————————
| Backstage                 | services / queues / scheduler / MCP runtime / build-release pipeline                |
| Support Processes         | token issuance / rate limiting / package registry / telemetry / on-call             |
| Metrics                   | latency | error rate | MTTR  (per phase)                                            |

Dependency arrows: SDK vX ⇄ API vY (codependency); CLI → token issuer →; ...
Root-cause trace for <failure>: Evidence <symptom> → Frontstage <code> → Backstage <service> → ROOT CAUSE <expired token | schema drift | registry outage>
```
*If there are no divider lines, no dependency arrows, or the failure isn't traced to a named backstage cause, it's a journey map in disguise — redo steps 4-8.*
