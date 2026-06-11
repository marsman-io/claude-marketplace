# meta-prompt-skills

A flat collection of standalone meta-prompt skills — each one a cleaned port of
a battle-tested community prompt, formatted as a proper Claude Code skill that
auto-routes on its own triggers. Unrelated to the `*-loop-methodology` plugins
in this marketplace; they share only the repo.

No agents, no shared docs. Each skill stands alone — install the plugin and the
skills fire on the phrasings in their descriptions, or invoke one directly.

## Skills

| Skill | Does | Fires on |
|---|---|---|
| `humanizer` | Strip AI tells from prose — two passes (voice, tells) + a self-audit. | "humanize this", "make this sound less like AI", "de-slop this draft" |
| `video-distill` | Turn a video / transcript into layered, retainable notes — concepts, analogies, critical pass, framework, memory anchors. | "summarize this video", "distill this talk", "turn this video into notes" |
| `sota-scan` | Benchmark a project against top peers; every gap names a real competing project as proof. Three depth tiers. | "how does this compare to the best", "sota scan", "competitive gap analysis" |
| `session-mine` | Mine recent session transcripts for corrections you keep making; promote the recurring ones to memory rules or skills. | "mine my sessions", "what corrections do I keep making", "turn my repeated feedback into rules" |
| `clarify-deep` | Gather context first, then ask a few deep, blind-spot-revealing clarifying questions before acting. | "ask me clarifying questions first", "clarify before you build" |
| `book-to-skill` | Turn a non-fiction book's repeatable method into one or two installable skills (diagnose / apply), with activation tests. | "turn this book into a skill", "make a skill from `<book>` by `<author>`", "skillify `<book>`" |
| `prompt-improver` | Improve an existing prompt/skill across 7 dimensions; picks **auto** (improve and return) or **interactive** (propose → refine) mode first. | "improve this prompt", "make this skill better", "tighten this skill's triggers" |

## Provenance

Each skill is interpolated from a harvested example meta-prompt — community
posts (r/claudeskills, "How to AI", and others) and the
[`sota-scan`](https://github.com/MerlijnW70/sota-scan) repo — rewritten into the
skill format: a triggering `description` with NOT-for guards, and a body that is
the procedure. Credit to the original authors; these are cleaned, self-contained
ports.

## Layout

```
.claude-plugin/plugin.json
skills/
  humanizer/SKILL.md
  video-distill/SKILL.md
  sota-scan/SKILL.md
  session-mine/SKILL.md
  clarify-deep/SKILL.md
  book-to-skill/SKILL.md
  prompt-improver/SKILL.md
README.md
```

## Install

```
/plugin install meta-prompt-skills@claude-marketplace
```

## License

MIT.
