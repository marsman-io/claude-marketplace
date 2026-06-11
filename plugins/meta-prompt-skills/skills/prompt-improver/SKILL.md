---
name: prompt-improver
description: Improve an existing prompt, skill, or agent — sharpen intent, activation triggers, scope guards, structure, output contract, and strip AI tells. Picks a mode first — auto (improve and return, no human round) or interactive (propose, get direction, iterate). Triggers on "improve this prompt", "make this skill better", "refine this prompt", "tighten this skill's triggers", "review and improve this SKILL.md". NOT for writing a prompt from scratch, NOT for humanizing prose (use humanizer), NOT for building a book skill (use book-to-skill).
---

# Prompt improver

Take a prompt that already exists and make it sharper — without churning what
already works. The discipline: **minimal diff, maximal lift.** A rewrite that
reads nicer but changes behavior is a regression, not an improvement.

## Pick the mode first

Decide which mode you're in before touching anything — this is the skill's
phase-gate.

- **auto** — return a finished, improved version with a changelog; no
  back-and-forth. Default when the ask is one-shot ("improve this and give it
  back"), when running in a batch, or when the target is low-stakes.
- **interactive** — propose changes with rationale, get the user's direction,
  iterate until they're satisfied. Default when intent is ambiguous, the prompt
  is high-stakes, or the user signals they want to refine together.

If it's genuinely unclear, ask once — "auto (finished version back) or
interactive (we refine together)?" — then commit. Don't re-ask each round.

## What "better" means — the dimensions

Diagnose along these. Only change a dimension that's actually weak; cite the line
that's weak and say why.

1. **Intent** — does it name what it must make true, including when to refuse or
   return "couldn't verify"? A prompt that always answers has no acceptance bar.
2. **Activation** — does the `description` trigger on the right phrasings? Are
   there 3–5 realistic ones?
3. **Scope guards** — are there 3–4 NOT-for clauses naming adjacent tasks it must
   *not* fire on? Check for collisions with sibling skills.
4. **Structure** — is the procedure ordered and free of rule-of-three padding,
   dead sections, and restated steps?
5. **Output contract** — is the output format explicit enough to be repeatable?
6. **Evidence** — does it force citation / real examples and refuse to fabricate?
7. **Tells** — AI-slop in the wording. For prose-heavy prompts, defer to the
   `humanizer` catalog rather than duplicating it.

## Procedure

1. **Read the target in full.** For a SKILL.md, read frontmatter *and* body.
2. **Pick the mode** (above).
3. **Diagnose.** Mark each dimension strong / weak with a one-line, line-cited
   reason.
4. **Improve the weak ones.** Preserve voice and everything already strong. Prefer
   the smallest edit that fixes the dimension over a rewrite.
5. **Deliver by mode:**
   - *auto* — output the improved prompt + a changelog (dimension → what changed
     → why). Done.
   - *interactive* — present the diagnosis + proposed diff + rationale, ask
     "apply all / pick some / redirect?", iterate. Pin decisions so you don't
     re-litigate them next round.
6. **Validate** (for skills/agents): run the activation test — 5 phrasings of the
   real request should fire; 3 unrelated requests should stay silent. Report
   results; fix triggers until it passes.

## Output

```
Target: <file / prompt>
Mode: <auto | interactive>

Diagnosis:
  Intent        <strong | weak: reason @line>
  Activation    <...>
  Scope guards  <...>
  Structure     <...>
  Output        <...>
  Evidence      <...>
  Tells         <...>

Changes: <dimension — what — why>   (auto: applied | interactive: proposed)
Activation test: <5 fire? / 3 stay silent?>
```

If every dimension is already strong, say so and change nothing. "No improvement
needed" is a valid result — don't manufacture edits to look busy.
