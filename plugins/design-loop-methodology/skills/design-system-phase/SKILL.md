---
name: design-system-phase
description: Detect which lifecycle phase a design system is in — bootstrap, apply, audit, tweak, or refactor. Examines the project for tokens, components, screens, change patterns, and version metadata to infer phase. Invoke before any other lens skill so the right procedure runs. Triggers on "what phase is this", "detect lifecycle", "is this bootstrap or mature", "where are we in the lifecycle".
---

# Detect design system lifecycle phase

Read `${CLAUDE_PLUGIN_ROOT}/docs/Design system lifecycle.md` for the canonical phase definitions before applying this procedure.

## Procedure

1. **Scan for the token system.** Glob for `tokens.{json,css,ts}`, `theme.{ts,css}`, `design-tokens.*`, `colors.{js,ts}`, or a `tokens/` directory. Read the largest one to gauge maturity (line count, token count).
2. **Count consumer screens/components.** Glob for `*.{tsx,jsx,vue,svelte}`. Count files that import from the token files (`grep -l <token-import-path>`).
3. **Sample recent change activity.** `git log --oneline --since="6 months ago" -- <token-file>` and same for major components. Frequent token changes = apply; infrequent = audit/mature.
4. **Scan for drift markers.** grep for `"deprecated"`, `"migration"`, `"v2"`, `"TODO: remove"`, `"@deprecated"` in tokens + components.
5. **Check semver/version metadata.** Read `package.json` version or any `CHANGELOG`. Sub-1.0.0 + recent changes = apply; 1.x stable = audit; pending major bump = refactor.

A repo can be in multiple phases at once. Subsystems differ — name phase per subsystem if they diverge.

## Output

```
Phase: <bootstrap|apply|audit|tweak|refactor>
Subsystem (if scoped): <name>
Evidence:
  - <file:line or git-log finding>
  - <second observation>
Confidence: <high|medium|low>
```

If multiple phases coexist:
```
Phase (system-level): <e.g. audit>
Phase exceptions:
  - <subsystem>: <phase> — <reason>
```
