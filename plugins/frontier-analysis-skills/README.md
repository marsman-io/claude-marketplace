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
   file walks). No frontier tokens are burned framing the question.
2. **Think expensive** — make *one* focused reasoning call against the gathered
   evidence. The expensive model judges; it does not go hunting.
3. **Capture durably** — the verdict is written down as a durable artifact: a
   rule plus a test. You spend the frontier call once and enforce its judgment
   forever, cheaply, without paying again.

## Skills

| Skill | Does | When to reach for it |
|---|---|---|
| `seam-conformance` | Gather the implementations behind one interface, then make one frontier call judging whether they *behave* the same — error semantics, ordering, partial-failure, idempotency — not just typecheck the same. Freezes the verdict as a conformance table + test. | "do these implementations actually agree", "behavioral conformance across implementations", "one throws and another returns null", "conformance table for these adapters" |
| `layer-trace` | Trace one operation end-to-end across layers cheaply, then spend one frontier call finding where its error gets swallowed, re-typed vaguer, or loses its root cause at a hop. Bounded to a single operation so the whole chain fits context. | "works but the error is useless", "the failure loses its root cause crossing boundaries", "why is this error so vague by the time it surfaces", "trace where this operation drops its cause" |
| `contract-drift` | Diff an HTTP boundary against its schema source of truth (Zod / JSON Schema / OpenAPI / protobuf) cheaply, then make one frontier call to find routes that hand-roll a shape, cast loosely, or return undeclared fields — and producer/consumer pairs that silently disagree. Pins the result as a test. | "where did this contract drift", "does this route match the schema", "find boundaries that bypass validation", "which consumers diverged after the contract change" |
| `boundary-judgment` | Assemble the evidence on whether the boundary between two specific modules sits in the right place, then spend one frontier call on the judgment a grep can't make — and produces an argued verdict plus the smallest fix, not a rewrite. | "is this boundary in the right place", "should I split/merge these two modules", "this dependency points the wrong way", "which module should own X" |
| `invariant-capture` | Surface the unstated invariant a subsystem silently relies on cheaply, then make one frontier call to confirm it truly holds — and bank it as a one-line rule plus a characterization test that fails if it's violated. The "spend once, enforce forever" capture move. | "what is this code silently assuming", "capture the unwritten invariant", "bank what we just learned into a rule and a test", "what load-bearing assumption has no test" |

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
