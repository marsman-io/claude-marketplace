# Spec reference

One organizer is one YAML (or JSON) file. `examples/<type>.yaml` has a complete,
working spec for every type. Start from it with `organizer.py new <type> <path>`.

## Common fields

| Field | Meaning |
|---|---|
| `type` | Required. One of the types below. |
| `title` | Heading drawn above the organizer. |
| `instructions` | One or two sentences to the learner, drawn under the title. |
| `source` | Citation drawn as "Source: …" under the organizer. |
| `blanks` | `all`, `marked` or `none`: what the learner version blanks. Default: `marked` when any item has `blank: true`, else `all`. |
| `orientation` | `portrait` or `landscape` for the PDF (and the PNG width). The default depends on the type (wide types are landscape). |

**Items.** Wherever a list of entries is accepted, an entry is a string or a mapping
`{text: …, blank: true}`. `blank: true` makes the entry a blank in the learner version and
draws it in the accent colour in the key. Strings are plain text: no Markdown, no markup.

**Quote text with a comma or a colon** inside `{…}` or `[…]`: `{label: "if not possible, try"}`.
Unquoted, YAML splits it into a second empty key (or a second list item). `check` refuses
an empty key, but a stray extra list item only shows up as a count mismatch, or not at all.

**Versions.** `key` draws everything. `learner` replaces the answer fields with writing
space: ruled lines, empty boxes or dashed nodes, per type. Answer fields are listed under
each type.

## t-chart (portrait)

```yaml
left:  {heading: Pros, items: [...]}
right: {heading: Cons, items: [...]}
rows: 6          # learner: at least this many writing lines per side
```
Answer fields: the items.

## attribute-matrix (landscape)

```yaml
options: [Option A, Option B, Option C]
criteria:
  - name: Cost
    weight: 2                 # optional; multiplies the scores
    note: lower is better     # optional, drawn under the name
    values: [text per option] # optional; one per option
    scores: [3, 2, 1]         # optional numbers; one per option
scale: 1 = weakest, 3 = strongest   # optional legend
criteria-heading: Criteria          # optional first-column heading
highlight-best: true                # star and shade the top total (default true)
lines: 2                            # learner writing lines per cell
```
When any criterion has `scores`, a total row is added (weighted when any `weight` is set),
and the best option is starred in the key. Answer fields: values, scores and totals.

## flow-chart (portrait)

```yaml
direction: down        # or right
node-width: 36         # mm
steps:
  - id: start          # required, unique
    kind: start        # start | step | decision | io | end  (default step)
    text: Receive request
    who: Clerk         # optional, small line under the text
    next: check        # id, or a list of ids
  - id: check
    kind: decision
    text: Complete?
    branches:
      - {label: yes, to: approve}
      - {label: no, to: start}     # an edge to an earlier step is a loop, drawn bent
```
A step with no `next` and no `branches` continues to the following step, unless it is
an `end`. The steps are laid out in ranks. An edge that skips ranks is routed around the
boxes between. Answer fields: step text.

## mind-map (landscape)

```yaml
center: Main idea
branches:
  - text: Branch
    children: [Leaf, {text: Leaf with children, children: [...]}, {text: Hidden, blank: true}]
node-width: 3.4     # cm
row-height: 1.15    # cm per leaf
```
The branches split across both sides of the centre. Answer fields: every node except the
centre.

## concept-map (landscape)

```yaml
focus-question: How do … relate?
concepts:
  - {id: a, text: General concept}
  - {id: b, text: Specific concept, level: 1}   # level optional; else derived from links
links:
  - {from: a, to: b, label: includes}            # label = the linking phrase
  - {from: c, to: a, label: affects, cross: true} # cross-link: dashed and curved
node-width: 34      # mm
```
A label can be `{text: includes, blank: true}`, so the learner writes the linking phrase.
Answer fields: concept text, and link labels.

## kwl-chart (portrait)

```yaml
topic: Underwater inspection
columns: [know, want, learned]   # add `how` for K-W-L-H
know: [...]
want: [...]
learned: [...]
how: [...]
rows: 8
```
Answer fields: every column's entries.

## anticipation-guide (portrait)

```yaml
responses: [Agree, Disagree]     # or [T, F]
notes-heading: Evidence and notes
lines: 2
statements:
  - text: An arguable statement tied to a learning outcome.
    answer: Disagree             # key: ticked in the After column
    evidence: Where the lesson settles it.
```
The Before column is always empty: it holds the learner's own prior view. Answer fields:
answer and evidence.

## action-plan (landscape)

```yaml
goal: One well-defined goal
tasks:
  - {task: …, owner: …, due: …, resources: …, measure: …, status: …}
columns: [task, owner, due, measure]   # optional; default: the fields the tasks use
milestones: [{date: Day 30, text: …}]
rows: 6                                 # learner: at least this many rows
```
Answer fields: the goal and every task field.

## structured-notes (portrait)

```yaml
sections:
  - kind: lines        # a question with numbered answer lines
    prompt: Name the four objectives
    answers: [a, b, c, d]   # or `lines: 4` for empty lines
    numbered: true
  - kind: list         # a partial list: blank the items to recall
    prompt: Report elements
    items: [Cover, {text: Summary, blank: true}]
  - kind: fill-in      # running text with [[answers]]
    prompt: Compaction
    text: "Systems are [[static]] or [[dynamic]]."
  - kind: group        # directions plus labelled writing space
    prompt: With your partner…
    parts: [{label: Purpose, lines: 3, answer: optional model answer}]
  - kind: organizer    # a blank or partial diagram inside the notes
    prompt: Complete the diagram
    organizer: {type: mind-map, center: …, branches: [...]}
```
A nested organizer can be a mind-map, concept-map, flow-chart, t-chart, kwl-chart or
attribute-matrix. Answer fields: `lines` answers, blanked `list` items, `[[…]]` spans,
group answers.

## assessment-checklist (portrait)

```yaml
fields: [Participant name, Date]   # header lines
responses: [Yes, No]
criteria-heading: Criteria
criteria:
  - text: Observable behaviour
    sub: [Part one, Part two]      # optional sub-criteria, each with boxes
    mark: Yes                      # optional: ticked in the key (a filled example)
  - Another observable behaviour
comments: true
comment-lines: 3
```

## rubric (landscape)

```yaml
levels:
  - {score: 3, label: Excellent, definition: Exceeds expectations}
  - {score: 2, label: Acceptable, definition: Meets expectations}
criteria:
  - skill: Use of room
    weight: 2                      # optional, shown as ×2
    descriptors: [one per level, in level order]
show-scale: true     # the level-definition table above (when levels have definitions)
score-column: true   # adds a Score column and a Total row to fill in
passing: The passing requirement.
```
The learner and key versions are the same, because rubrics are shared with learners.

## self-questioning (portrait)

```yaml
phases: [before, during, after]    # built-in FHWA question stems
lines: 2
# or write your own:
phases:
  - name: Before
    questions: [Why am I reading this?, {text: What will I learn?, answer: model answer}]
```

## handout (portrait)

```yaml
title: Lesson kit
items:            # full organizer specs, in order
  - {type: anticipation-guide, ...}
  - {type: structured-notes, ...}
```
In a PDF, each item starts a new page. In a PNG or the terminal, the items are stacked.
