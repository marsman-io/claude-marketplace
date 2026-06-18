---
name: explanation-doc
description: >-
  Produce an explanation — the understanding-oriented Diátaxis page that answers "why" a tool, SDK, CLI, REST API, MCP server, or system is shaped the way it is: the mental model, the design decisions and their trade-offs, the history, the alternatives that were rejected. Discursive and reflective; readable away from the keyboard; builds the cognition that makes tutorials, how-tos, and reference finally click. Accepts pasted notes, design docs, or external sources — "not in repo" is normal. Triggers on "explain why", "design rationale", "mental model", "background / conceptual doc", "understanding-oriented", "why does it work this way", "architecture explanation", "concept guide". NOT for step-by-step "do this" sequences (use how-to-recipe or tutorial-scaffold), NOT for exhaustive parameter description (use reference-from-spec), NOT for deciding which mode a topic belongs to (use docs-diataxis-audit).
---

# Explanation Doc

Explanation is the mode that builds a mental model — the page a developer reads to understand *why* the tool is shaped the way it is, so the other three Diátaxis modes finally click. It is understanding-oriented: it clarifies and illuminates a topic, makes connections between concepts and to the wider ecosystem, and discusses the reasons — design decisions, historical accident, technical constraints — that the task-bound modes have no room for. It takes a higher, broader view and may admit more than one opinion. It is the easiest mode to skip and the one whose absence makes everything else feel arbitrary. Your posture is generative: write the explanation a thoughtful reader would thank you for, even though it never tells them what to do.

## When to use
- **Do** write explanation when a reader keeps asking "but *why*?" — why this abstraction, why this default, why not the obvious alternative.
- **Do** use it to lay out a mental model: the concepts and how they relate, in prose plus a small concept sketch.
- **Do** be honest about trade-offs — name what was given up and which alternatives were rejected and why.
- **Don't** write a numbered "do this" sequence — that's a task; use **how-to-recipe** or **tutorial-scaffold**.
- **Don't** enumerate every flag, field, or parameter — that's information; use **reference-from-spec**.
- **Don't** decide *which* mode a page should be — route that through **docs-diataxis-audit** first.

## Procedure
1. **Frame the topic as a question worth answering.** State it as "Why does X work this way?" or "How should I think about Y?" — not as a feature name. The question is the spine.
2. **Lay out the mental model.** Name the core concepts and how they relate. Prose first, then a small sketch. Link to **reference-from-spec** for exhaustive detail; do not repeat it here.
3. **Explain the design decisions and trade-offs.** For each significant choice, say what it buys and what it costs. Honesty is the value — hidden trade-offs are why readers distrust docs.
4. **Record the alternatives considered.** What else was on the table, and why it lost. This is often the single most useful section and the one most often missing.
5. **Make connections.** Tie the topic to prior art, adjacent surfaces (SDK / CLI / dashboard / installer), and the wider ecosystem. End by pointing at the how-to and reference that *act* on this understanding.
6. **Keep instructions out.** When you feel the urge to write "do this", stop and link to a how-to instead.

## Output
```markdown
# Understanding the <surface> execution model
<!-- or: "Why <component> works the way it does" -->

## The question this answers
> Why does <surface> <do the surprising thing> instead of <the obvious thing>?

If you have ever wondered <restate the reader's confusion>, this page is the
background — not a set of steps. Read it away from the keyboard.

## The mental model
<surface> is built around three ideas: <concept A>, <concept B>, and <concept C>.
<2–4 paragraphs of prose explaining how they relate and why the relationship matters.>

```text
        <concept A> ──owns──▶ <concept B>
             │                    │
          emits               consumes
             ▼                    ▼
        <event / artifact> ──▶ <concept C>
```

(For the full set of fields and options on each, see the reference — this page
stays conceptual.)

## Why it's designed this way
- **Decision: <choice>.** Gains <benefit>. Costs <what it makes harder>.
- **Decision: <choice>.** Gains <benefit>. Costs <what it makes harder>.
- **Constraint: <external/technical limit>.** Forced <consequence>; we leaned into it by <approach>.

## Alternatives we considered / what we gave up
- **<Alternative 1>** — rejected because <reason>; it would have meant <cost>.
- **<Alternative 2>** — partially adopted as <where it survives>; dropped elsewhere because <reason>.
- **What we gave up:** <capability or simplicity sacrificed> in exchange for <what we got>.

## Connections & further reading
- Prior art / influences: <link or name>.
- Adjacent surfaces: <how this relates to the CLI / SDK / dashboard>.
- To act on this understanding:
  - Do it → <how-to link>
  - Learn it from zero → <tutorial link>
  - Look up the details → <reference link>
```

Failure mode: drifting into instructions (a numbered "do this" sequence) or flattening into a parameter list — the moment it tells the reader what to DO or merely lists what EXISTS, it has abandoned the understanding it was meant to build and become a how-to or reference.
Sources: Diátaxis — Explanation (https://diataxis.fr/explanation/); Diátaxis compass / understanding-oriented (cognition + acquisition) (https://diataxis.fr/).
