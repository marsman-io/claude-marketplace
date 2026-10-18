---
name: graphic-organizer
description: Build and edit graphic organizers and learning tools — T-charts, attribute (decision) matrices with weighted scores, flow charts with decisions, mind maps, concept maps with linking phrases, K-W-L charts, anticipation guides, action plans, structured notes with fill-in blanks, assessment checklists, rubrics and self-questioning sheets — as a YAML spec that renders to a printable PDF, a PNG, and a live picture in the terminal (with cc-intelligent-ui). One spec yields an answer key and a learner version with writing space where the answers were. Grounded in the FHWA NHI LearnersFirst instructor handbook. Triggers on "make a T-chart comparing…", "build a decision matrix for…", "flow chart this process", "mind map of…", "concept map for…", "K-W-L chart on…", "anticipation guide for my lesson", "action plan template", "guided notes / fill-in-the-blank notes", "assessment checklist", "rubric for…", "self-questioning handout", "graphic organizer", "learner version", "answer key", "add a row / branch / step to the organizer", "blank out…". NOT for data charts or plots (use a charting tool), NOT for slide decks, NOT for a whole lesson's set of handouts (use lesson-kit).
---

# Graphic organizer

An organizer here is one YAML file, the **spec**. It is the only thing you edit.
Everything else is rebuilt from it by `${CLAUDE_PLUGIN_ROOT}/scripts/organizer.py`
(Typst underneath): the PDF to print, the PNG to share, and the inline picture. Never edit
an output file, and never hand-write Typst for an organizer the spec can express.

`CLI` below means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/organizer.py`.

## 1. Choose the organizer

Pick by the job the learner's thinking has to do, not by looks. When the user names a
type, use it; when the job fits another type better, say so in one line and build theirs
anyway unless they agree to switch.

| The learner needs to… | Type |
|---|---|
| weigh two sides: pros/cons, before/after, A vs B | `t-chart` |
| compare 3+ options on shared criteria, or choose one | `attribute-matrix` (add `weight` and `scores` to decide) |
| follow or design a process with decisions | `flow-chart` |
| brainstorm or outline around one idea | `mind-map` |
| show how concepts relate, with the relation named | `concept-map` |
| surface prior knowledge and set learning goals | `kwl-chart` |
| commit to a position, then test it against the lesson | `anticipation-guide` |
| turn learning into dated tasks with owners | `action-plan` |
| take notes at key points (lines, blanks, partial lists) | `structured-notes` |
| be observed against yes/no criteria | `assessment-checklist` |
| be scored on quality levels | `rubric` |
| question themselves before, during, after | `self-questioning` |

Per-type purpose, how to run it with learners, and the known failure of each:
`${CLAUDE_PLUGIN_ROOT}/references/teaching.md`. Read the type's section before writing
content; it changes what good content is (anticipation statements must be arguable,
checklist criteria observable, mind map nodes key words not sentences).

## 2. Write the spec

1. Run `CLI doctor` once per session. It reports Typst, the package path and whether
   cc-intelligent-ui is installed. Without Typst, stop and tell the user `brew install typst`.
2. Start from the worked example: `CLI new <type> <path>`. The default path is
   `organizers/<slug>.yaml` in the current folder unless the user names one.
3. Replace the example content with the user's. Field reference:
   `${CLAUDE_PLUGIN_ROOT}/references/spec.md`. Keep `title`, write `instructions` as
   one or two sentences addressed to the learner, and keep `source` when content comes from
   a document (cite it). Write content the user can stand behind: when you lack the subject
   facts, ask or leave clearly marked placeholders instead of inventing them.
4. Mark what learners fill in. Put `blank: true` on an item, node, step or concept to
   make it a blank in the learner version. With no marks, every answer field is blank for
   the learner, which suits empty templates (K-W-L, T-chart, action plan). In
   structured-notes `fill-in` text, wrap each answer as `[[answer]]`.
5. Quote any string with a comma or a colon in it (`label: "if not possible, try"`). In
   YAML's `{…}` and `[…]` forms, an unquoted comma silently splits the text.
6. `CLI check <path>`. Fix every problem it names. It exits 1 until the spec is valid.

## 3. Render and show

- `CLI render <path>` writes `<stem>.key.pdf`, `<stem>.learner.pdf`, `<stem>.key.png` and
  `<stem>.learner.png` next to the spec. Options: `--format pdf,png,svg`,
  `--version key|learner`, `--dark` (PNG/SVG only), `--paper a4`, `--out-dir`.
- **In the terminal, with cc-intelligent-ui installed**: run `CLI inline <path>` (add
  `--version learner` for the learner view) and paste its output into your reply
  verbatim. It is a fenced `typst` block, and cc-intelligent-ui draws it in the
  terminal's own theme and colours. Never edit the block; regenerate it after every spec
  change. Its revision comment changes with the spec, which is what makes the renderer
  redraw.
- **Without cc-intelligent-ui**, or in a background session (which cannot draw
  pictures): give the PNG path and a one-line text summary of the structure. Send the PNG
  with SendUserFile when the user is on another device.
- Always tell the user the spec path and the PDF paths. The spec is what they bring back
  to change things.

## 4. Edit

Users iterate: "add a criterion", "move Grout under Materials", "make the third step a
decision", "blank out the evidence column", "swap the sides", "A4 please".

1. Read the spec and make the change with Edit. Change only what was asked.
2. `CLI check`, then re-render or re-run `CLI inline` and show the new version.
3. Summarise the change in one line ("added *Cost* (weight 2); Thru-turn now leads 25–22").
   When scores or totals moved, say how.

When the user edits the spec file themselves, re-read it before your next change.

## 5. Before you call it done

- The learner version shows writing space wherever the learner must think, and the key
  shows every answer. Look at both.
- A graphic organizer scaffolds; it does not teach by itself. The FHWA guidance is to
  follow it with an application step: a discussion, a written explanation, an action plan.
  Suggest one line of follow-up activity when it fits the user's purpose.
- Don't overload: matrices "become unwieldy if there are too many options"; T-charts hold
  two sides only; mind maps work for less complex ideas. Split, or switch type, rather than
  cram.

## Limits

- Layout is automatic. Flow charts and concept maps are drawn in ranks, with loops bent
  back. A crowded concept map can cross its dashed cross-links over boxes. If so, set
  `level` on concepts or use fewer cross-links.
- In a terminal picture, cc-intelligent-ui scales a drawing to fit the screen. Long
  tables grow the page instead.
- Text is plain: no Markdown or Typst markup inside spec strings. `[[…]]` works only in
  `fill-in` text.
