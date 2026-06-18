---
name: how-to-recipe
description: >-
  Produce a how-to guide — a task-oriented recipe that gets an already-competent user from a goal they already have to a named outcome, fast, including the conditional branches real work demands. Use when writing "How to <verb> <object>" docs for a CLI, SDK, REST API, MCP server, dashboard, installer, or runbook, where the reader knows what they want and roughly how the tool works and just needs the steps. Triggers on "write a how-to", "how-to guide", "recipe", "task guide", "how do I <do X>", "steps to accomplish", "runbook for". NOT for teaching a newcomer the ropes (use tutorial-scaffold), NOT for explaining why or how something works (use explanation-doc), NOT for cataloguing every flag and field (use reference-from-spec).
---

# How-To Recipe

A how-to respects an expert's time. The reader already knows what they want and roughly how the tool works; your job is to get them to a named result efficiently, including the branches real usage forces. Start from the goal, not from the tool. Write a sequence of actions, not a body of knowledge — every line either moves the reader toward the outcome or tells them which fork to take. Acknowledge real-world variation: multiple valid options, the thing that commonly goes wrong, the conditional that splits the path. Do not teach concepts and do not be exhaustive; link out for the first, defer to reference for the second.

## When to use
**Do** use when the reader has a concrete goal ("deploy a build", "rotate a key", "migrate the schema") and enough background to follow imperative steps without hand-holding.
**Do** use when real usage branches and you must say "if X, do Y; otherwise Z".
**Don't** use to bring a beginner up to speed or guarantee a safe first success — that's `tutorial-scaffold`.
**Don't** use to explain how the system works under the hood or why a design exists — that's `explanation-doc`.
**Don't** use to enumerate every command, flag, parameter, or return field — that's `reference-from-spec`.

## Procedure
1. **Name the goal.** Title it `How to <verb> <object>` — a result the reader already wants. If you can't phrase it as a verb on an object, it's not a how-to.
2. **State preconditions.** List what must already be true (access, installed tooling, prior state) under "Before you start". Do not teach how to satisfy them; link out.
3. **Write the action sequence.** Numbered imperative steps, each one real action with a fenced command or code block. Order them as the reader executes them.
4. **Branch where real usage branches.** Add at least one conditional ("if you're on a managed instance, do A; if self-hosted, do B"). Name the common failure and its fix inline.
5. **Cut the teaching.** When a step needs a concept explained, link to an explanation doc instead of explaining. When it needs the full option list, link to reference.
6. **End at the goal.** Close with a "Verify" step that confirms the outcome, then "Related" links to adjacent how-tos.

## Output
```markdown
# How to <verb> <object>

Get <outcome> in <N> steps. This assumes you already <baseline competence>;
for first-time setup see [Getting started](../tutorial/getting-started.md).

## Before you start

You'll need:
- <access/role>, e.g. an API token with `deploy:write` scope
- `<tool> >= <version>` installed and on your `PATH`
- <prior state>, e.g. a passing build on the target branch

## Steps

1. **<First action>.**
   ```bash
   <cli-or-sdk-or-curl command>
   ```

2. **<Second action>.** If <condition A>, run the first; otherwise the second:
   ```bash
   # managed / hosted
   <command for path A>
   ```
   ```bash
   # self-hosted
   <command for path B>
   ```
   > If you see `<common error string>`, <one-line fix or link>.

3. **<Third action>.**
   ```bash
   <command>
   ```
   Tune `<flag>` to taste — see [Reference: <command>](../reference/<command>.md) for all options.

## Verify

Confirm the goal is achieved:
```bash
<check command, e.g. status query>
# expected: <observable success signal>
```

## Related
- [How to <adjacent task>](./how-to-<adjacent>.md)
- [How to roll back <object>](./how-to-rollback-<object>.md)
- [Explanation: how <subsystem> works](../explanation/<subsystem>.md)
```

Failure mode: starting from "let's learn about X" or pausing to explain how something works — the moment it teaches rather than directs, it has become a tutorial or an explanation, and the competent reader who just wanted the steps is now wading through theory.
Sources: Diátaxis, How-to guides — https://diataxis.fr/how-to-guides/.
