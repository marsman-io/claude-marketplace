---
name: session-mine
description: Mine recent Claude Code session transcripts for corrections the user keeps making, and turn the recurring ones into proposed memory rules or skills. Triggers on "mine my sessions", "what corrections do I keep making", "find my recurring fixes", "turn my repeated feedback into rules", "what do I keep telling you to do differently". Reads ~/.claude/projects/*/*.jsonl. NOT for summarizing a single conversation, NOT for general analytics or usage stats.
---

# Session mine

Find the corrections the user makes again and again, then propose durable rules
so they stop having to. The value is in the *recurring* signal — a one-off
nitpick is noise; the same correction across many sessions is a rule waiting to
be written.

## Procedure

1. **Locate transcripts.** Session logs are JSONL under
   `~/.claude/projects/<encoded-path>/*.jsonl`, one file per session. List them
   by recency (`ls -t`). Confirm scope with the user if it matters: this project
   only, or across all projects. Say how many sessions you actually found — if
   they asked for "last 50" and only 12 exist, name that; don't imply coverage
   you didn't have.

2. **Scan for correction signals.** In each transcript, read user turns for the
   shape of a correction:
   - explicit reversal — "no", "instead", "actually", "not like that", "I said"
   - re-instruction — "always", "never", "stop doing", "remember to"
   - rework — undo / revert / "redo this", or the user re-doing your output by hand
   - repeated preference — the same stylistic or process ask restated

3. **Cluster by underlying rule.** Group raw corrections into the *rule* behind
   them, not the surface words. "use straight quotes" and "drop the curly quotes"
   are one rule. Count distinct sessions per cluster — frequency across sessions,
   not within one.

4. **Apply a threshold.** Only promote a cluster that recurs across **≥3
   sessions** (or the user's chosen bar). Below that, list it as a "watch" item,
   not a rule.

5. **Propose the durable form.** For each promoted cluster, draft the artifact:
   - a one-line **memory / CLAUDE.md rule** for a behavioral preference, or
   - a **new skill** sketch if the correction is a repeatable procedure.
   Quote one or two real transcript excerpts as evidence per cluster.

## Output

```
Sessions scanned: <N> (scope: <this project | all projects>)

Recurring corrections (≥ threshold):
  1. <rule, one line> — seen in <k> sessions
       evidence: "<short quote>" (<session/date>)
       propose: <CLAUDE.md rule | skill name + one-line purpose>
  2. ...

Watch list (below threshold):
  - <correction> — <k> session(s)
```

Don't invent patterns to hit a count. "Nothing recurs above threshold yet" is a
valid result.
