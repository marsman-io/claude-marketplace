---
name: installer-upgrade-audit
description: Review of how a tool installs, upgrades, migrates config/state, checks compatibility, and rolls back — modeled as an explicit, auditable STATE MACHINE. Use when you have an installer/updater (in-repo source, an install script, a migration registry, or pasted upgrade logs) and need to judge whether upgrades are idempotent, user data is protected, and rollback is safe. Triggers on "installer review", "upgrade flow audit", "migration safety", "rollback review", "is the upgrade safe", "compatibility matrix", "does the upgrade protect user files". NOT for per-command CLI behavior of the installed tool (→ cli-conformance), NOT for the installed tool's runtime error UX (→ failure-state-matrix).
---

# Installer & Upgrade Audit

An installer is the one piece of software that runs with permission to move, rewrite, and delete the user's files — so the only safe way to reason about it is as an explicit state machine where every stage is observable and every destructive step is reversible. The failures that matter are not crashes; they are the silent ones: a migration re-run that double-applies, an upgrade that wipes a user-owned config, a rollback that deletes a file it never created. This skill walks one install/upgrade flow against that state machine and reports where a stage is missing, irreversible, or destructive-without-consent. It diagnoses; it does NOT edit the installer or its product code. You read the install script, the migration registry, the state journal, or pasted upgrade logs, find the gaps, and hand back the artifacts — then a human intervenes.

## When to use

**Do** use when:
- You have one install/upgrade flow to audit — installer source, an install/update script, a migration registry, or pasted upgrade output/logs.
- You need a cite-backed verdict on idempotency, user-data protection, compatibility gating, and rollback safety.
- "Not in repo" is fine: an install script URL or a pasted migration table is a valid target.

**Don't** use when:
- The concern is how the installed tool's individual commands behave (→ cli-conformance).
- The concern is the installed tool's runtime failure/recovery UX (→ failure-state-matrix).

## Checklist

Verify each. Cite the proof (`file:line`, a pasted log line, or the migration-registry entry). "Couldn't verify from the artifact" is a valid finding.

**State machine**
- [ ] The pipeline EXISTS and each stage is observable (logged/inspectable): detect → policy → prompt/confirm → plan → preflight → install → migrate → compatibility-check → verify → switch → record → rollback.
- [ ] No stage is fused into another in a way that hides a destructive step (e.g. install that silently migrates with no plan/preflight).

**Detection & state**
- [ ] Idempotent: fresh install, reinstall with a matching manifest (= no-op), and upgrade with a pending migration each behave correctly and predictably.
- [ ] A persistent install-state / JOURNAL exists, so an already-applied migration is NEVER re-run.
- [ ] Checksum drift on an already-applied step is tolerated/reconciled, not treated as fatal.
- [ ] Global vs. local/per-project scopes are distinct and don't clobber each other.

**Policy & confirmation**
- [ ] Upgrade modes (manual / auto / snooze / ignore-this-version) are persisted across runs.
- [ ] Destructive actions are VISIBLE before they run via `--dry-run`/preview (which files move, which are removed, which configs get rewritten) AND require confirmation.

**Migration**
- [ ] Migrations are typed, registry-driven actions (e.g. move-managed, remove-managed, rewrite-config, mark-user-owned) — not ad-hoc inline `mv`/`rm`.
- [ ] User data protected BY DEFAULT: user-owned files are declared and never wiped; a tool-managed file that differs from expected is BACKED UP before removal and reported.
- [ ] Stale tool-managed files are removed when a feature is retired (no orphan accumulation).
- [ ] CRLF and Windows path-separator edge cases are handled in config rewrites and path comparisons.

**Compatibility**
- [ ] An explicit matrix (tool version × runtime/OS/host × dependency versions) is consulted BEFORE the upgrade runs.
- [ ] Platform migration happens before version upgrade (don't upgrade onto an unsupported runtime).
- [ ] A delta / partial-upgrade path exists that preserves local config instead of forcing a clean reinstall.

**Verify / switch / rollback**
- [ ] A post-install verification hook runs.
- [ ] The atomic switch to the new version happens ONLY after verify passes.
- [ ] Rollback restores modified/created paths and NEVER deletes files it didn't itself create or modify.
- [ ] Rollback is best-effort but LOUD when incomplete (it tells the user exactly what it couldn't restore).
- [ ] A verify-failure and a switch-failure each auto-trigger rollback.
- [ ] A manual rollback command exists.
- [ ] A structured (JSONL) audit log records every step.
- [ ] An update lock guards against concurrent installs.

## Procedure

Gather the surface cheaply first, then walk the checklist once.
1. Map the state machine: read the installer/updater entrypoint, the migration registry, and the state-journal format (or take the install script / pasted logs). Mark which of the twelve stages you can actually find.
2. Trace ONE upgrade end to end against the journal: what is detected, what is planned, what is migrated, what is recorded — and prove a re-run is a no-op.
3. Walk the checklist groups, recording ✓ / ✗ / partial with citations, then mentally run each rollback-test row below and note whether the code would survive it.

This audit is partly AUTOMATABLE: a CI test can drive the installer through fresh/reinstall/upgrade/rollback against a scratch root and assert the journal prevents double-apply, that user-owned files survive, and that rollback restores exactly the paths it touched and nothing more.

## Output

```
## Install/upgrade decision tree + state machine
detect → policy → prompt/confirm → plan → preflight → install → migrate
  → compatibility-check → verify → [pass] switch → record   [fail] → rollback
(annotate each arrow: present? observable? reversible? — cite file:line)

## Compatibility matrix
| Tool version | Runtime/OS/host | Dependency versions | Supported? | Gate consulted before upgrade? |
|--------------|-----------------|---------------------|------------|--------------------------------|
| 2.x | Linux/macOS | node ≥ 18 | yes | yes (file:line) |

## Migration registry
| Path | Action type | Backup? | User-owned? | Reversible? |
|------|-------------|---------|-------------|-------------|
| ~/.toolrc | rewrite-config | yes | no | yes |
| ~/.tool/custom/ | mark-user-owned | n/a | YES | n/a |

## Rollback test matrix
| Scenario | Expected | Verdict | Evidence |
|----------|----------|---------|----------|
| fresh install | clean install, journal recorded | ✓/✗ | … |
| reinstall (matching manifest) | no-op | … | … |
| upgrade with pending migration | applied once, recorded | … | … |
| locally-modified managed file | backed up before removal | … | … |
| unknown file under a tool dir | left untouched | … | … |
| user-owned file under a wiped dir | preserved | … | … |
| failed-apply → rollback | restores touched paths only | … | … |
| global vs local scope | isolated | … | … |
| Windows path separators | handled | … | … |
| CRLF config | handled | … | … |
```

Failure mode of this method: certifying a state machine from the happy-path install log alone — the dangerous stages (drift reconciliation, partial-failure rollback, user-owned-file protection) only execute on the messy upgrade, so any rollback-matrix row not exercised against a dirty scratch root is an assumption wearing a checkmark.
