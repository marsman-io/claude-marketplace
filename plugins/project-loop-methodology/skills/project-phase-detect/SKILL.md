---
name: project-phase-detect
description: Detect which lifecycle phase agentic product work is in — charter, plan, execute, adjust, or replan. Examines available artifacts (intent notes, prompts, issues, plans, diffs, tests, screenshots, logs, demos, acceptance notes, and optional Linear/Jira/roadmap artifacts) to infer phase. Invoke before any other PM lens skill so the right procedure runs. Triggers on "what phase is this project", "is this in execute or replan", "where are we in the product work lifecycle".
---

# Detect project lifecycle phase

Read `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` for the canonical phase definitions before applying this procedure.

## Procedure

1. **Scan for project-defining artifacts.** Glob/grep the workspace for:
   - Intent / brief / one-pager / PRD / RFC / proposal documents (`intent`, `brief`, `PRD`, `RFC`, `proposal`, `acceptance`)
   - Delegation artifacts (prompts, agent plans, TODO lists, issue descriptions, Linear/GitHub issues if present)
   - Produced-work artifacts (diffs, changed files, PR descriptions, screenshots, test output, logs, demos)
   - Adjustment artifacts (follow-up prompt, scope-change note, "actually make it..." request, bug report)
   - Retro / post-mortem / replan notes

2. **Read the most recent artifact for each type** to assess maturity.

3. **Sample recent change activity.** If the workspace is git-tracked, `git log --since="2 weeks ago" -- <project-area>` to gauge active vs. dormant. Frequent edits to intent / prompt / plan files = Plan phase; frequent product diffs with stable intent = Execute; broad rewrites to prompt + plan + implementation = Replan.

4. **Look for phase markers** in artifact language:
   - "intent", "what should become true", "acceptance", "definition of done" -> Charter / Plan
   - "plan", "approach", "todo", "agent will" -> Plan
   - "implemented", "diff", "screenshot", "test output", "demo" -> Execute
   - "change this", "scope change", "actually", "follow-up", "blocker" -> Adjust
   - "start over", "new approach", "original plan no longer works", "re-baseline" -> Replan

5. **Phase per user path.** A product area can be split — one user path in Execute, another in Charter because its intent was never named. Surface this if true; don't force a single phase.

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
