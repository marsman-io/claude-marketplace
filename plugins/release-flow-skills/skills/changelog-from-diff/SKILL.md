---
name: changelog-from-diff
description: Derive human-readable changelog / release notes from the git diff + log between two refs (default last tag..HEAD; accepts explicit refs). Groups commits by type (feat / fix / perf / refactor / docs / chore), summarizes for humans, prints to stdout. Offers to prepend a new entry to CHANGELOG.md only on explicit confirmation — never rewrites or reorders existing history. Triggers on "/changelog-from-diff", "generate the changelog", "draft release notes for this tag", "what changed since the last release". NOT a commit-message linter, NOT a version bumper, NOT a release publisher, and NOT a rewriter of past changelog entries.
disable-model-invocation: true
---

# Changelog from diff

User-only skill (`/changelog-from-diff`) — it emits a release artifact, so it never auto-fires. Run it against a git repo to turn the range between two refs into release notes a human will actually read.

## Procedure

1. **Resolve the range.** If the user named explicit refs (`v1.2.0..HEAD`, `abc123..def456`, a single tag), use them. Otherwise default to **last tag..HEAD**: `git describe --tags --abbrev=0` for the lower bound, `HEAD` for the upper. If no tag exists, fall back to the repo's first commit (`git rev-list --max-parents=0 HEAD`) and say so — "no prior tag, treating as first release."

2. **Read the range.** Pull both the log and the diffstat — the log gives intent, the diff gives ground truth:
   - `git log <range> --no-merges --pretty=format:'%h%x09%s%x09%an'`
   - `git diff <range> --stat` (to sanity-check that the summaries match what actually changed; flag commits whose subject claims more than the diff shows)

3. **Group by type.** Bucket each commit by Conventional-Commit prefix when present (`feat` / `fix` / `perf` / `refactor` / `docs` / `test` / `build` / `ci` / `chore`), inferring the type from the subject + diff when the prefix is missing. Drop pure noise (merge commits, version-bump commits, `wip`, formatting-only) unless the user asks to keep everything. Surface **BREAKING CHANGE** footers and `!`-marked types into their own top bucket.

4. **Summarize for humans.** Rewrite each kept commit as one user-facing line — what changed for someone *using* the project, not the internal mechanics. Collapse a string of fixup commits on one feature into a single entry. A commit subject is a hint, not the final copy.

5. **Humanize the prose (graceful, optional).** Assemble a short release-notes **paragraph** (the human prose at the top of the notes — the narrative, NOT the grouped bullet list). If `meta-prompt-skills:humanizer` is installed, hand it *only that prose* for a de-slop pass; keep the bullets verbatim. If that plugin is absent, **skip the pass and print one line saying so** — `(humanizer not installed — release-notes prose left un-passed)`. Never hard-fail on the missing cross-plugin dependency.

6. **Print to stdout. Do not touch any file yet.** Writing is a separate, confirmed step (see Output).

## Output

Print to stdout by default:

```
## <upper ref / proposed version> — <date>   (<range>)

<one short humanized paragraph: the headline of this release>
(humanizer not installed — release-notes prose left un-passed)   # only if absent

### Breaking changes
- <user-facing line>   (<short-sha>)

### Features
- <user-facing line>   (<short-sha>)

### Fixes
- <user-facing line>   (<short-sha>)

### Other (perf / refactor / docs / chore)
- <user-facing line>   (<short-sha>)

Dropped 4 noise commits (merges, version bump, wip). Range: <lower>..<upper>, 23 commits.
```

Then, and only then, offer the file write:

```
Prepend this as a new entry to CHANGELOG.md? (y/N)
```

On explicit **yes**: insert the block at the top of `CHANGELOG.md` (below any title/preamble header, above the most recent existing entry). On **no** / no answer: stop — stdout is the deliverable.

**Never** rewrite, reword, reorder, or de-duplicate existing changelog entries; this skill only *prepends* a new one. If `CHANGELOG.md` doesn't exist, offer to create it with the single new entry. Existing history is read-only.
