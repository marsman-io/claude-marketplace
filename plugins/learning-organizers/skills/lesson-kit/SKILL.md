---
name: lesson-kit
description: Assemble one lesson's set of learning tools from a learning outcome, as a single handout spec that renders to a multi-page printable PDF (answer key plus learner copy). Picks a before / during / after sequence (for example an anticipation guide or K-W-L chart to open, structured notes or a partial concept map during, a 3-2-1 summary, assessment checklist or action plan to close) and builds each piece with the graphic-organizer spec format. Grounded in the FHWA NHI LearnersFirst instructor handbook. Triggers on "make handouts for this lesson", "lesson kit for…", "before/during/after activities for…", "build the participant materials for…", "turn this outline into learner handouts", "worksheet set for my training". NOT for one organizer (use graphic-organizer), NOT for slides or a full course syllabus.
---

# Lesson kit

A kit is one `type: handout` spec whose `items` are complete organizer specs. Build,
check, render and edit it exactly as the `graphic-organizer` skill describes. That skill's
CLI, spec reference (`${CLAUDE_PLUGIN_ROOT}/references/spec.md`) and teaching guide
(`${CLAUDE_PLUGIN_ROOT}/references/teaching.md`) apply unchanged. Start from
`${CLAUDE_PLUGIN_ROOT}/examples/handout.yaml`.

## 1. Pin the outcome

Write the lesson's learning outcome as one observable sentence ("Participants can
classify a NEPA action as CE, EA or EIS"). If the user gave a topic but no outcome,
propose one and confirm it before building anything. Every tool in the kit must serve
that outcome. Drop any tool that doesn't.

## 2. Choose two to four tools

| Phase | Purpose | Good fits |
|---|---|---|
| Before | Activate prior knowledge, set a purpose | `anticipation-guide` (arguable beliefs), `kwl-chart` (open topic), `self-questioning` before stems |
| During | Process at key points | `structured-notes` (lines, partial lists, `[[fill-in]]`, a partial `mind-map` / `concept-map` / `flow-chart` section) |
| After | Consolidate, apply, assess | 3-2-1 summary (structured-notes), `assessment-checklist` (skills), `rubric` (performances), `action-plan` (transfer to the job), the K-W-L's L column |

Each organizer needs an application step after it, so make the last item an application
or transfer tool, not another fill-in. Vary the note formats: predictable notes bore
learners. Keep the kit to what fits the time. Two strong tools beat four thin ones.

## 3. Build

1. `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/organizer.py new handout <path>` (default
   `organizers/<lesson-slug>.yaml`), then replace the items.
2. Give each item a phase-led title ("Before — what do you think?") and one line of
   instructions to the learner.
3. Use the lesson's real content: anticipation statements the material settles, notes
   blanks on the key terms, checklist criteria taken from the outcome. If you don't have
   the source material, ask for it. Don't invent subject facts.
4. `check`, then `render` (each item is one page in the PDF). Show the key with `inline`
   when cc-intelligent-ui is installed, else give the PNG path.

## 4. Hand over

Give the spec path and both PDFs. Add a short facilitator note: when to hand out each page,
the timing, and the discussion or application step after each one.
