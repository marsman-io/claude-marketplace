---
name: current-future-state
description: >-
  Applies the temporal mode to a journey map — current (as-is, with the WORKAROUNDS
  developers actually use and telemetry-validated friction) vs future (to-be,
  simplified, principle-driven) — and turns the DELTA into a prioritized DevEx
  backlog scored impact × value × effort and phased into a non-breaking v1. The
  workarounds lane is the point: shell scripts wrapping a clunky CLI, hitting REST
  directly because the SDK lags, copy-pasting from issues because docs are stale —
  these reveal the real future-state requirements, and each future solution is
  pinned to the surface it lives on (CLI/SDK/REST/MCP/docs). Use when you need to
  move an experience from where it is to where it should go without breaking
  existing integrations. Triggers on "current vs future state", "as-is to-be",
  "gap analysis", "future state journey", "what should this experience become",
  "devex roadmap from the gaps". NOT for a single point-in-time snapshot (use
  journey-map).
---

# Current / Future State

This is a temporal lens on a journey map: two maps over the same phase columns — a current (as-is) state and a future (to-be) state — whose DELTA becomes a prioritized DevEx backlog. The decisive lane is Workarounds on the current map: developers silently route around friction (a shell wrapper hiding a clunky CLI, calling REST directly because the SDK is behind, copy-pasting from a GitHub issue because the docs are stale). Each workaround is a requirement the future state must absorb — ignore them and your "future" map fixes problems users don't have while leaving the real ones. Future solutions must be concrete surface changes, each tagged with the surface it lives on, and constrained by reality: backward compatibility, semver, migration paths. A v1 future state that breaks existing integrations is not shippable.

## When to use

**Do**
- Use when you have a current journey map (or can build one) and want a roadmap.
- Use telemetry to validate current friction; cite the metric, not a hunch.
- Use the workarounds lane as the primary source of future-state requirements.

**Don't**
- Don't draw a future state without first capturing real workarounds.
- Don't propose solutions that break existing integrations in v1 — note the constraint.
- Don't leave a future solution unpinned to a surface (CLI/SDK/REST/MCP/docs).

## Procedure
1. Anchor on a current journey map (same phase columns). Cite it or build it via journey-map first.
2. Current map: per phase record real Actions, Friction (with a telemetry KPI: drop-off %, time-to-first-call, error rate — cite it), and the Workarounds developers actually use (cite the script, the direct REST call, the issue thread).
3. State the design principles for the future (e.g. "auth in one step", "SDK never lags API"). Cite where they come from.
4. Future map: per phase draw the simplified flow, and for each improvement name the SURFACE it lives on (CLI/SDK/REST/MCP/docs).
5. Gap layer: for each current→future difference write a backlog row; score impact × user-value × effort (1-5 each).
6. Add Constraints to each row (backward compat, semver bump, migration path). Drop or defer anything that breaks existing integrations.
7. Phase the backlog into a shippable v1 (non-breaking) and later milestones; sort by score.

## Output
```
Phases →  Discover | Install | Authenticate | First-success | Integrate | Operate/Debug | Upgrade
Source (current map): <cite>   Future principles: <p1; p2 — cite>

CURRENT (as-is)
| Actions               | ...                                                                  |
| Friction (KPI, cited) | 😣 auth: 4 steps, 38% drop-off <telemetry cite>                      |
| Workarounds (cited)   | shell wrapper <repo> | direct REST (SDK lags) <cite> | copy-paste issue|

FUTURE (to-be)
| Simplified flow       | ...                                                                  |
| Solution → surface    | one-step auth → CLI | typed errors → SDK | example → docs | tool → MCP |

GAP / BACKLOG
| # | Phase | Change (current→future)   | Impact | Value | Effort | Score | Constraint        | Milestone |
|---|-------|---------------------------|--------|-------|--------|-------|-------------------|-----------|
| 1 | Auth  | 4 steps → 1, on CLI       | 5      | 5     | 2      | high  | keep old flow (semver minor) | v1   |
| 2 | ...   | ...                       | ...    | ...   | ...    | ...   | non-breaking      | v1/v2     |

v1 (non-breaking): #1, ...   Later: #...
```
*If the current map has no workarounds lane, the friction has no cited telemetry, or any future solution isn't pinned to a surface, it isn't a current/future-state map — redo steps 2 and 4.*
