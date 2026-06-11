---
name: book-to-skill
description: Turn a non-fiction book's repeatable method into one or two installable Claude skills — extract the system, write a triggering SKILL.md with NOT-for guards, optionally split into a diagnose skill and an apply skill, then test activation. Triggers on "turn this book into a skill", "make a skill from <book> by <author>", "build a skill from <book>'s method", "skillify <book>". NOT for fiction / memoir / pure storytelling, NOT for book summaries, NOT for general writing advice.
---

# Book to skill

Convert a book's method into a skill you can run anytime: **book → method →
SKILL.md → /command**. Only works for books with a repeatable framework.

## 1. Is the book skillable?

- **Works:** books with a repeatable framework, method, or checklist.
- **Skip:** fiction, memoirs, pure storytelling.
- **Test:** can you describe the book's method in numbered steps? If yes, it's
  skillable. If you can't, stop — don't manufacture a method the book doesn't have.

## 2. Extract the system — five questions

Answer these from the book (ask the user to paste passages where you lack them):

1. What problem does this book solve?
2. What are the steps of the method, in order?
3. What rules does the author repeat across chapters?
4. What mistakes does the author warn against?
5. What questions does the author ask the reader?

## 3. One skill or two?

Big books have two layers — split them:
- **`<book>-diagnose`** — runs the book's questions and frameworks *on the
  user's situation* (reviews, finds problems).
- **`<book>-apply`** — runs the book's steps and templates to *produce the
  output*.

Example (The Mom Test, Rob Fitzpatrick): `momtest-diagnose` reviews your
interview questions and flags the leading ones; `momtest-apply` rewrites them in
the Fitzpatrick format. Build two only when the diagnose and produce jobs are
genuinely distinct; otherwise one skill is cleaner.

## 4. Write the SKILL.md

Frontmatter `name` + `description`; the description must name:
- **Activation** — the exact task and 3–5 phrasings that should trigger it.
- **NOT-for** — 3–4 adjacent tasks it must *not* fire on (e.g. general writing,
  unrelated business advice, book summaries).

Body = the extracted method as a procedure: the ordered steps, the author's
repeated rules, the mistakes-to-avoid, and the author's questions. Attribute the
method to the book and author; this is a tool built *from* the book, not a copy
of it.

If anything from the five questions is missing, **interview the user before
generating** — don't fill the gaps with invented content.

## 5. Test before you install

1. **Activation:** try 5 different phrasings of the same request — does it fire
   every time?
2. **Over-firing:** try 3 unrelated requests — does it stay silent?
3. **Self-check:** ask "when would you use this skill?" and confirm the answer
   matches the intent.

Fix the `description` triggers until all three pass, then install.

## Output

The generated `SKILL.md` (or two, for diagnose/apply), the slash command(s) to
run it, and the activation test results. Note any of the five questions you had
to leave thin so the user can fill them.
