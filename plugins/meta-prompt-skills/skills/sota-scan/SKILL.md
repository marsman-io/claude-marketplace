---
name: sota-scan
description: Benchmark this project against the state of the art in its space — produce a scorecard, a standing relative to top peers, and a ranked gap list where every gap names a real competing project as proof. Triggers on "how does this compare to the best", "sota scan", "benchmark against competitors", "what are we missing vs top projects", "competitive gap analysis of this repo". Three depth tiers (quick / standard / exhaustive). NOT for code review, NOT for generic best-practice advice, NOT for market sizing or business strategy.
---

# SOTA scan

Compare this project against the leading projects in its space and report the
gaps. The discipline that makes it useful: **every gap names a real project as
evidence.** No generic advice — if you can't point to a peer that does it
better, it's not a gap, it's an opinion.

## Depth tiers

State which tier you're running and why.
- **quick** — surface comparison against the obvious top 3–5 peers. Fast read.
- **standard** (default) — full scorecard against a fair peer set. Regular use.
- **exhaustive** — deep pass for a launch or pitch; widen the peer set, read
  their docs/changelogs, justify each score.

## Procedure

1. **Identify the space + peers.** Determine what this project actually is, then
   list the leading projects solving the same problem. Sort peers by *approach*,
   not by popularity — compare like with like, not against a random leaderboard.

2. **Read this project.** Glob/grep the repo for what it does and doesn't do —
   features, docs, tests, DX, positioning. Cite files.

3. **Compare dimension by dimension.** For each dimension (capabilities, docs,
   DX, performance, polish, positioning), score this project against the peer set
   and note who sets the bar.

4. **Rank the gaps.** Order by leverage. Each gap entry must name the specific
   peer project that does it better, and how.

5. **Next steps.** A short, prioritized to-do list — the highest-leverage gaps
   first, each tied to its proof.

## Output

```
Project: <name> — <one-line what-it-is>
Tier: <quick | standard | exhaustive>
Peer set: <projects, grouped by approach>

Verdict: <one line> — Score: <NN%>
Standing: <where this sits relative to peers>

Gaps (ranked by leverage):
  1. <gap> — proof: <peer project> does <X>. <how to close it>
  2. ...

Next steps:
  - <highest-leverage gap, as an action>
```

If a claimed strength can't be backed against a real peer, drop it. A flattering
scorecard with no named proof is the failure mode.
