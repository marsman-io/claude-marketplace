# Mission slop

**Mission slop** is work from an unattended, long-horizon agent run that looks finished and
isn't. A mission here means an agent working for hours from a written brief, with no human
watching, and reporting in a completion file that an independent reviewer then checks.

This document explains where mission slop comes from, which remedies carry over from the
research on single-response "LLM laziness", and what a real review record says it actually
looks like. The pattern catalogue with detection signals is in
[`Slop patterns.md`](Slop%20patterns.md).

## The finding that shaped this plugin

The starting point was taste-skill's laziness research and its `output-skill`, which target
single-response truncation: placeholder code, skipped sections, "let me know if you want me
to continue". We expected missions to fail the same way at a larger scale. A review record
of real missions says otherwise. It covered about 350 independent adversarial verdicts on
about 120 missions or PR units, run unattended by Claude-based agents, with completion
reports, follow-up files and briefs alongside.

| Pattern | Units with a finding | Shape |
|---|---|---|
| Overclaiming prose | ~115 | PR body, changeset, help text or comment asserts behaviour, coverage or counts the code lacks |
| Tests that can't fail | ~88 | Passes against a plausible wrong implementation: a mocked seam, an unrealistic fixture, a mutation of the wrong thing |
| Happy-path only | ~85 | Time zone, letter case, the other OS, unreadable-vs-absent, concurrency, crash window: untested |
| False green | ~64 | "Passed" read from a stale log, a skipped suite, the wrong commit, or a check that cannot fail |
| Incomplete sweep | ~63 | "No X remains", proven by a search whose scope is what makes it pass |
| Swallowed error / unknown read as success | ~62 | A failure or an unknown reported as success, or as "not present" |
| Narrow fix | ~61 | The cited instance fixed; the same bug one row, branch or package over |
| Fix creates a new defect | ≥30 | The repair for round N is the blocker in round N+1 |
| Silent scope shrink | ~31 | Part of a clause, or only its letter, delivered without saying so |
| Stubs, placeholders, dead fields | ~14 | TODO markers, unfilled placeholders, fields nothing reads |
| Test weakened | ~13 | An exact assertion loosened or deleted |
| Undisclosed behaviour change | ~10 | A refactor quietly widens what the code does |
| Gate violation | ~7 | The worker decided its own stop condition, or touched what the brief forbade |
| Follow-up dumping | 4 of ~620 follow-ups | Required work filed as a follow-up |
| Premature stop / asking a question | 0 | The stalls that happened were caused by the harness, not the model |

The classic laziness patterns are the **rare tail**. Missions almost never ship visibly
unfinished work. Their slop is **evidence slop**: work that looks *proven* when it isn't.
And almost all of it, about 82 of 104 items across 19 repair rounds, was missing from the
mission's own completion report and was found only by the independent reviewer.

So this plugin keeps the output-skill rules as a floor, but most of its weight sits where
the failures were:

- where every green figure came from;
- whether a test can fail;
- whether a sweep's scope is honest;
- whether a fix closed the class;
- whether shipped prose claims more than the code does.

Counts are approximate: distinct units per pattern, tagged by readers, about ±10%.
Overclaiming prose is probably inflated, because reviewers read prose closely.

## Root causes

What the laziness research says about single responses mostly holds for missions, but each
cause takes a different shape over a multi-hour run.

**Stopping pressure → declaring done early, not stopping early.** Post-training rewards
ending a response, and the research reads truncation as a behavioural choice rather than a
capability limit. In a mission it rarely shows up as stopping. Missions with a written
gate convention write a gate memo and carry on. It shows up as *declaring* done: the last
clause marked complete on thinner evidence than the first.

**Placeholder propagation → tutorial-shaped evidence.** Training data is full of
`// implement here`. It is also full of tests that check a function returns *something*,
mocks that stand in for the very seam under test, and "all tests pass" written without a
log. The mission version of placeholder code is placeholder *evidence*.

**Effort thresholds → the cheapest reading.** When a task looks heavy, models take
shortcuts. In a mission the shortcut is interpretive. An ambiguous clause gets its cheaper
reading, "handle errors" becomes one try/catch, and "fix the finding" becomes fixing the
one cited line.

**Error avoidance → making red go away.** Single responses get shorter to reduce the
surface for mistakes. Missions reduce *visible* failure instead:

- a red test becomes a skip, or a looser assertion;
- a failing path gets a catch that returns a default;
- an "unknown" collapses into "absent".

**Self-report asymmetry (mission-specific).** The agent writes its own tests and its own
completion report. A self-written adversarial test only reaches as far as the author can
imagine an adversary. This is why the review record shows near-total reliance on the
independent reviewer, and why the audit rebuilds scope from the brief rather than from the
agent's ledger.

**Context loss (mission-specific, despite the research).** The research found that context
loss is not the main cause of truncation within one long conversation. Missions also
compact, restart and resume, and a summary drops the brief's details. The remedy is to keep
scope on disk: the ledger, re-read after every compaction.

**Brief defects (the upstream cause).** In the review record, several of the worst runs
trace straight to the brief:

- a prescribed proof that could not fail;
- a mechanism prescribed instead of a property, then bypassed by the case it didn't name;
- a cross-cutting invariant left unstated;
- a named symbol that did not exist on the base;
- an instruction to *claim* the change was safe to merge;
- a one-line spec, or a bundle of about eight deliverables, which took six and eleven
  review rounds.

The cleanest runs had briefs that required reproducing the problem on the base first,
targeted one seam, and named the wrong implementation each proof had to kill.

## Remedies that transfer

| Single-response remedy (laziness research / output-skill) | Mission form | Where |
|---|---|---|
| Banned-pattern lists for code and prose | Diff and report pattern lists, made deterministic in a scanner | `antislop-execution`, `antislop-audit`, `slop_scan.py` |
| Count the deliverables, then cross-check before answering | A scope ledger locked at step 0, reconciled at the end, rebuilt independently by the audit | all three skills |
| Pause at a clean breakpoint with `[X of Y complete]` | Stop at a clean breakpoint; the ledger records X of Y and the resume point; continue rather than restart | `antislop-execution` |
| Remove discretion ("explicit syntax binding") | Brief checks that close every cheaper reading: countable scope, falsifiable clauses, properties not mechanisms | `antislop-brief` |
| Evidence blocks before the narrative | Each clause's section opens with the command, the output and the commit it ran at | `antislop-execution` |
| Chain-of-Verification | Before the report: the question that would refute each claim, answered by a command | `antislop-execution` |
| Chunked execution | One ledger row at a time, proven before the next | `antislop-execution` |
| Specific skill descriptions improve discovery | Descriptions with concrete triggers and NOT-for guards | all skills |

## Remedies left out, and why

- **Temperature, top-p, thinking level.** A brief cannot set them. In orchestrated setups,
  model and effort belong to the launcher, not the prompt.
- **Incentive and stakes framing** ("I'll tip $200", "critical to my career"). The evidence
  is weak:
  - the tip figure comes from an informal social-media experiment;
  - the "take a deep breath" gain comes from Google DeepMind's OPRO work on older models;
  - EmotionPrompt's effect sizes were measured on 2023-era models.

  Current Claude models follow instructions closely, and emphatic framing tends to make
  them over-apply a rule rather than apply it better. These skills give the reason behind
  each rule instead.
- **Date and season tricks.** They rest on the anecdotal "winter break" observation, and
  they're irrelevant here.
- **"Exhaustive output" as a goal.** Missions need *complete*, not *long*. A long report is
  its own slop when padding buries the one honest gap. The ledger makes completeness
  countable, so it isn't judged by length.

## A note on the sources

The laziness research's mechanisms are plausible and match what the review record shows.
Several of its numbers trace to informal or misattributed sources, so this plugin adopts
the mechanisms and not the numbers. Sources the plugin does lean on:

- **Chain-of-Verification:** Dhuliawala et al., 2023, Meta AI.
- **OPRO:** Yang et al., 2023, Google DeepMind. The origin of "take a deep breath and work
  on this problem step-by-step".
- **EmotionPrompt:** Li et al., 2023.
- **taste-skill:** Leonxlnx, MIT, `research/laziness/` and `skills/output-skill/`.

The review-record figures come from one team's mission workflow, which is TypeScript-heavy,
infrastructure-adjacent, and reviewed by a different model prompted to falsify the
author's central claim. Other workflows will weight the patterns differently. The order at
the top of the table is the part most likely to generalise: evidence slop dominates,
visible incompleteness is rare.
