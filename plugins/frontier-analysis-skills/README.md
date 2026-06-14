# frontier-analysis-skills

A flat collection of standalone skills for spending an expensive ("frontier")
reasoning model well on any codebase — each one a proper Claude Code skill that
auto-routes on its own triggers. Codebase-neutral: nothing here assumes a
particular language, framework, or repo. Unrelated to the `*-loop-methodology`
plugins in this marketplace; they share only the repo.

No agents, no shared docs. Each skill stands alone — install the plugin and the
skills fire on the phrasings in their descriptions, or invoke one directly.

## The shared spine

A frontier model is the most expensive tool in the box, so every skill here
spends it the same disciplined way:

1. **Gather cheap** — collect the evidence with ordinary tools (grep, reads,
   greps, file walks). No frontier tokens are burned framing the question.
2. **Think expensive** — make *one* focused reasoning call against the gathered
   evidence. The expensive model judges; it does not go hunting.
3. **Capture durably** — the verdict is written down as a durable artifact: a
   rule plus a test. You spend the frontier call once and enforce its judgment
   forever, cheaply, without paying again.

## Skills

| Skill | Does | When to reach for it |
|---|---|---|
| `seam-conformance` | Gather the call sites at an architectural seam, then make one frontier call judging whether they conform — and freeze the verdict as a rule + test. | "does this code respect the boundary", "check seam conformance", "are these call sites following the pattern" |
| `layer-trace` | Walk a request/value across layers cheaply, then spend one frontier call deciding where a layer's responsibility leaks — captured as an enforceable rule. | "trace this through the layers", "where does this responsibility leak", "is this logic in the wrong layer" |
| `contract-drift` | Diff a contract (interface, schema, API shape) against its consumers cheaply, then make one frontier call to judge real drift vs noise, and pin the result as a test. | "has this contract drifted", "do callers still match this interface", "check for schema/API drift" |
| `boundary-judgment` | Assemble the evidence on a hard design boundary call, then spend one frontier call on the judgment that actually needs reasoning — and record the decision durably. | "is this the right boundary", "should this live here or there", "make the hard call on this split" |
| `invariant-capture` | Surface candidate invariants cheaply, then make one frontier call to confirm the ones that truly hold, and turn each into a test that enforces it forever. | "what invariants hold here", "capture this invariant as a test", "lock in this guarantee" |

## Layout

```
.claude-plugin/plugin.json
skills/
  seam-conformance/SKILL.md
  layer-trace/SKILL.md
  contract-drift/SKILL.md
  boundary-judgment/SKILL.md
  invariant-capture/SKILL.md
README.md
```

## Install

```
/plugin install frontier-analysis-skills@claude-marketplace
```

## License

MIT.
