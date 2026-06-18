---
name: cross-surface-synthesis
description: Composes the outputs of the other experience-mapping skills into one master matrix that reveals which surfaces support each user goal and exactly where the experience fragments — a job that forces hopping CLI→dashboard→API with a copy-paste handoff in the middle is a fragmented job, and this matrix names the seam that breaks it. Use when you need the strategic picture across all surfaces rather than any single map. Triggers on "cross-surface synthesis", "master matrix", "which surfaces support each job", "where is the experience fragmented", "jtbd by surface matrix", "pull the maps together", "where does the experience break between surfaces". NOT for building any single map — for the surface catalog use touchpoint-inventory, for the system graph use ecosystem-map, for naming use concept-terminology-audit, for structure use surface-information-architecture.
---

# Cross-Surface Synthesis

This is the master artifact: it composes the outputs of the other mapping skills into one matrix that answers the strategic question none of them answers alone — which surfaces support each user goal, and WHERE does the experience fragment. A job is fragmented when completing it forces the user to hop across surfaces with a manual handoff in the middle: mint a token in the dashboard, paste it into the CLI, then poll the REST API for status. Each such hop is a seam, and seams are where users churn, file support tickets, and write brittle glue scripts. The individual maps feed this one: the inventory says what surfaces exist, the concept audit says whether they speak the same language, the ecosystem map says whether the loops close. Synthesis reads them where available and degrades gracefully where they don't — it can bootstrap a lightweight version from a quick JTBD pass and a glance at the surfaces.

## When to use

**Do** use to produce the strategic JTBD-by-surface picture and to rank the most fragmented jobs by the seam that breaks them; run last, after the other maps where possible.

**Don't** use to build any single map — route to touchpoint-inventory, ecosystem-map, concept-terminology-audit, or surface-information-architecture for those.

## Procedure

1. Fix ONE product. One target per invocation.
2. Read available upstream outputs: `jtbd-map` (jobs/rows), `touchpoint-inventory` (surface columns + owners), `concept-terminology-audit` (seam evidence where names disagree), `ecosystem-map` (broken loops). If an output is missing, bootstrap a lightweight version — list 5-8 jobs or use the lifecycle phases (discover → install → authenticate → first-success → integrate → operate/debug → upgrade → rollback) — and note it as bootstrapped.
3. Set rows = jobs-to-be-done (or lifecycle phases). Set columns = CLI / SDK / REST API / MCP / Dashboard / Docs, plus Failure-states and Owner.
4. Fill each cell: ✓ supported, ⚠ fragmented (works but with a manual handoff or drift), ✗ gap. Add a one-phrase note per non-✓ cell, cited.
5. For each ⚠ job, name the seam: the exact surface→surface handoff that breaks it (e.g. dashboard→CLI token copy-paste).
6. Rank jobs by fragmentation severity (number/cost of seams). List the top fragmented jobs with their breaking seam.
7. Cite cells from upstream artifacts or directly (`file:line`, pasted, URL).

## Output

```
# Cross-Surface Synthesis — <product>  (source maps: jtbd[y/bootstrapped] · inventory[y/n] · terminology[y/n] · ecosystem[y/n])

## Master matrix  (cell = ✓ supported · ⚠ fragmented · ✗ gap)
| Job-to-be-done / phase        | CLI | SDK | REST | MCP | Dash | Docs | Failure-states            | Owner     |
|-------------------------------|-----|-----|------|-----|------|------|---------------------------|-----------|
| Authenticate                  | ⚠   | ✓   | ✓    | ✗   | ✓    | ⚠    | token name mismatch       | Platform  |
| First successful deploy       | ✓   | ✓   | ✓    | ⚠   | ✓    | ✓    | MCP can't poll status     | DevRel    |
| Debug a failed run            | ✓   | ⚠   | ✓    | ✗   | ⚠    | ✗    | no log link from dash     | **none** ⚠|
| Upgrade across major version  | ⚠   | ✗   | ✓    | ✗   | ✗    | ⚠    | migration notice CLI-only | **none** ⚠|

## Most fragmented jobs (ranked) — and the seam that breaks each
1. Authenticate — SEAM: Dashboard mints token, user copy-pastes into CLI env (env-var name disagrees per concept-terminology-audit). 
2. Debug a failed run — SEAM: Dashboard shows failure but no deep link to logs; user hops to CLI then API. Owner: none.
3. Upgrade — SEAM: migration notice appears only in CLI deprecation warning; SDK/dashboard users never see it.
```

Failure mode: the matrix is filled per surface in isolation so every column looks well-supported, but the seams between surfaces — the copy-paste handoffs where the job actually breaks — were never named, so a green-looking matrix certifies a fragmented experience.
