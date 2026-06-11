---
name: project-phase-detect
description: Detect which lifecycle phase a project is in — charter, plan, execute, adjust, or replan. Examines available project artifacts (charters, plans, status reports, change requests, retro docs, OKRs, Jira/Linear/Asana state) to infer phase. Invoke before any other PM lens skill so the right procedure runs. Triggers on "what phase is this project", "is this in execute or replan", "where are we in the project lifecycle".
---

# Detect project lifecycle phase

Read `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` for the canonical phase definitions before applying this procedure.

## Procedure

1. **Scan for project-defining artifacts.** Glob/grep the workspace for:
   - Charter / brief / one-pager / PRD documents (`charter`, `brief`, `PRD`, `RFC`, `proposal`)
   - Plan artifacts (Gantt, roadmap, milestone list, sprint backlog)
   - Status artifacts (status report, weekly update, RAG dashboard, burndown)
   - Change-request artifacts (CR doc, scope-change ticket, exec-ask thread)
   - Retro / post-mortem / replan docs

2. **Read the most recent artifact for each type** to assess maturity.

3. **Sample recent change activity.** If the workspace is git-tracked, `git log --since="3 months ago" -- <project-area>` to gauge active vs. dormant. Frequent edits to the plan = Plan phase; frequent status updates with stable plan = Execute; plan being rewritten = Replan.

4. **Look for phase markers** in artifact language:
   - "agreed", "approved", "kickoff" → Plan complete, Execute starting
   - "scope change", "CR-", "blocker", "exec ask" → Adjust
   - "re-baseline", "new plan", "the original plan no longer" → Replan
   - "retro", "post-mortem", "lessons learned" → Replan or post-Execute

5. **Phase per workstream.** A project can be split — one workstream in Execute, another in Replan because its upstream slipped. Surface this if true; don't force a single phase.

## Output

```
Phase: <charter | plan | execute | adjust | replan>
Workstream (if scoped): <name>
Evidence:
  - <file:line or artifact name with finding>
  - <second observation>
Confidence: <high|medium|low>
```

If multiple phases coexist:
```
Phase (project-level): <e.g. execute>
Phase exceptions:
  - <workstream A>: replan — <reason>
  - <workstream B>: charter — <reason>
```
