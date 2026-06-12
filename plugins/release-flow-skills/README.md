# release-flow-skills

The home for release-flow skills — the small, user-invoked procedures
around git, pull requests, and the release lifecycle that you reach for
when you're about to ship.

These are skills, not agents: install the plugin and invoke one directly.
The first skill is `changelog-from-diff`. More release-flow skills will
land here over time.

## Skills

| Skill | Does | Invoke with |
|---|---|---|
| `changelog-from-diff` | Turn a git diff into a clean, grouped changelog / release-notes entry. Emits the artifact to stdout; never rewrites history. | `/changelog-from-diff` (user-invoked) |

`changelog-from-diff` is the only skill shipped today; more release-flow
skills will land in this table over time.

## Layout

```
.claude-plugin/plugin.json
README.md
skills/
  changelog-from-diff/SKILL.md
```

## Install

```
/plugin install release-flow-skills@claude-marketplace
```

## License

MIT.
