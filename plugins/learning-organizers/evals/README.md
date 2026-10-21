# learning-organizers evals

An eval suite for `claude plugin eval`, a post-run checker for the specs the
runs write, and a replay that shows every regex grader is live. Everything
here runs locally; the paid part is the eval itself (real model sessions on
your own credential). No CI runs it.

## What each case proves

| case (dir) | tags | the request | it passes when |
|---|---|---|---|
| `t-chart` (01) | routing | "Make a T-chart comparing renting a home with buying one…" | a `type: t-chart` spec with both sides at the named path, its learner PDF rendered, and a reply that hands it over (llm) |
| `lesson-kit` (02) | routing, kit | "Make the handouts for my lesson on the water cycle…" | one `type: handout` spec with two or more organizer items, its learner PDF, a reply naming the set (llm) |
| `concept-map` (03) | routing | connected boxes "with the relationship written on each connecting line" — a concept map that is never named | a `type: concept-map` spec with labelled links, exactly two link labels `blank: true`, its learner PDF |
| `one-organizer-for-a-lesson` (04) | routing | a lesson is mentioned but ONE K-W-L chart is asked for (lesson-kit: "NOT for one organizer") | a `type: kwl-chart` spec that is not a handout, its learner PDF |
| `plot-data` (05) | negative | "Plot this data…" with six rows of rainfall (graphic-organizer: "NOT for data charts or plots") | neither plugin skill is called (`tool_used: Skill`, `max: 0`, `arm: both`, scored), no organizer spec appears anywhere in the trace, and the trace shows a real chart (plotting code, an SVG, or a written/read image file) |
| `learner-version` (06) | edit | starts from `inputs/organizers/bridges.yaml` (a copy of `examples/t-chart.yaml`) and asks for the learner version with two named points blanked | exactly those two items carry `blank: true` (two regexes plus `count:2`), a `render … bridges.yaml` command ran, and the learner PDF exists |
| `flow-chart` (07) | routing | "Flow chart this process…" (book returns, with two decisions) | a `type: flow-chart` spec with a `kind: decision` step and `branches`, its learner PDF |
| `lesson-set` (08) | routing, kit | names three organizer types but wants them as "one set of handouts for the session" (graphic-organizer: "NOT for a whole lesson's set of handouts") | one `type: handout` spec holding an anticipation guide, structured notes and an assessment checklist, its learner PDF |

Every case's score graders read the outcome (the spec file, the rendered PDF,
the trace), so the no-plugin arm is scored against the same bar. Each
`tool_used: Skill` grader naming `graphic-organizer` or `lesson-kit` is the
CLI's with-only *indicator* under `--ablation with-without`: reported, never
scored (`plot-data`'s is the exception: `arm: both`, so "no skill fired" is
scored in both arms). Prompts name the output path so a grader can read it.

## Before you run it

- Typst on PATH (`organizer.py doctor`), and either cc-intelligent-ui
  installed or one earlier render with network, so cetz 0.5.2 and fletcher
  0.5.8 sit in `~/.claude/plugins/cache/*/cc-intelligent-ui/*/render/packages`
  or `~/Library/Caches/typst/packages`.
- **Why every case has a scaffold.** The eval sandbox gives each run an empty
  home and blocks the network (a dev run failed with `failed to download package
  (https://packages.typst.org/preview/cetz-0.5.2.tar.gz: Proxy failed to
  connect)`), and only `EVAL_*` variables reach a run, so
  `LEARNING_ORGANIZERS_PACKAGES` cannot be passed in. `seed-typst-cache.sh`
  (identical in every case; `test_suite.py` checks) runs before the agent, as
  you, and copies those packages into the run's own Typst cache; for
  `learner-version` it also copies `inputs/` into the run's cwd. That is why
  every run needs `--scaffold`. Read the script before you pass the flag.
- **Tools.** Cases list `Skill Read Write Edit Glob Grep Bash`; the operator
  grant is `--allow-tools Bash Write Edit`. `Bash(python3:*)` is not enough:
  the agent runs the skill's CLI as `CLI="python3 …/organizer.py"; $CLI check …`,
  which that pattern does not match (dev run 02: Bash denied, nothing rendered).
  The CLI runs Bash inside its OS sandbox.

## Run it

One case (or one `--tag`) per invocation — `--case` is not repeatable. From the
repository root:

```bash
claude plugin eval plugins/learning-organizers \
  --trust-plugin --no-publish -j 1 --max-cost-usd 2 \
  --model claude-sonnet-5-5 --judge-model claude-sonnet-5-5 \
  --allow-tools Bash Write Edit --scaffold --keep-temp \
  --runs 3 --ablation with-without --case t-chart \
  --output-dir /tmp/lo-evals/t-chart --report /tmp/lo-evals/t-chart/report.html \
  --json /tmp/lo-evals/t-chart/result.json
```

- `--no-publish`: otherwise the HTML report is published to claude.ai.
- `--max-cost-usd`: a hard ceiling, checked before each run starts (so one
  run in flight can overrun it; keep `-j 1`). Exit 2 means the ceiling cut the
  invocation short: the cases it did not reach are partial, not failed.
- `--judge-model claude-sonnet-5-5`: the default haiku judge is unreliable.
- `--trust-plugin`: skips the first-run trust prompt for this folder.
- `--keep-temp`: keeps each run's sandbox, which the checker and the replay
  read. Without `--output-dir` results go to `evals/results/`, which `evals/.gitignore` keeps out of git.

The kept sandboxes land in `/tmp/e-XXXXXX` on macOS whatever `TMPDIR` says. The
CLI seals the parts the plugin wrote; it prints, for each, the
`chmod 700 /private/tmp/e-XXXXXX /private/tmp/e-XXXXXX/sealed` that opens it.
Do not run git inside a kept sandbox.

## Check what the runs wrote

```bash
export PYTHONDONTWRITEBYTECODE=1
python3 plugins/learning-organizers/evals/check_runs.py /private/tmp/e-XXXXXX/sealed/home/cwd ...
# the edit case: also prove the two named points are hidden from the learner
python3 plugins/learning-organizers/evals/check_runs.py <its kept cwds> \
  --expect-hidden "Long lane closures and detours" \
  --expect-hidden "Needs heavy lifting equipment and planning"
```

Every YAML/JSON file whose top-level `type` is one `organizer.py types` lists
must pass `organizer.py check`, and its learner version (queried through
`<organizer-answer>`, as `tests/selftest.py` does) must draw no answer marked
`blank: true` — and none at all when the key marks none, unless the spec says
`blanks: none` (then the learner copy shows every unmarked answer, by request).
One line per spec and a total; exit 0 = at least one spec checked and none
failed, 1 = a failure, 2 = `nothing-checked`.

## Show the regex graders are live

```bash
python3 plugins/learning-organizers/evals/replay_graders.py /tmp/lo-evals/t-chart/result.json --mutate
python3 plugins/learning-organizers/evals/results_table.py /tmp/lo-evals/*/result.json
```

`replay_graders.py` rebuilds each regex grader's text (`trace` = the run's
trace.jsonl lines; `{source: file, path}` = that file in the run's cwd) and
must agree with the CLI on every verdict (`compared N, agreeing N`); a
disagreement means the replay is wrong. `--mutate` then breaks each passing
verdict's text — deletes the matches, deletes one of a `count:N`, or inserts
`replay_breaks.json`'s offending text for a `not_contains` — and shows the
grader turn red, then green again on the original. `results_table.py` prints
the with-plugin vs no-plugin table, with the checker's verdict per arm.

Free tests, no model calls: `python3 plugins/learning-organizers/evals/test_check_runs.py`
and `python3 plugins/learning-organizers/evals/test_suite.py`.

## What it cost, and what it showed

Measured on Claude Code 2.1.305, 2026-10-21, at commit 8ed2929: every case,
`--ablation with-without --runs 3`, Sonnet 5.5 agent and judge, one
invocation per case (`results_table.py` output):

| case | with-plugin score | no-plugin score | delta | Skill indicator (with arm) | checker, with arm | checker, no-plugin arm | cost (USD) |
|---|---|---|---|---|---|---|---|
| t-chart | 1.00 | 0.50 | +0.50 | 3/3 runs | 3/3 ok | 3/3 ok | 0.6146 |
| lesson-kit | 1.00 | 0.00 | +1.00 | 3/3 runs | 3/3 ok | nothing-checked | 0.9592 |
| concept-map | 1.00 | 0.33 | +0.67 | 3/3 runs | 3/3 ok | 0/3 ok | 0.8675 |
| one-organizer-for-a-lesson | 1.00 | 0.44 | +0.56 | 3/3 runs | 3/3 ok | 1/1 ok | 0.4579 |
| plot-data | 1.00 | 1.00 | +0.00 | 0/3 runs | nothing-checked | nothing-checked | 0.4938 |
| learner-version | 1.00 | 0.00 | +1.00 | 3/3 runs | 3/3 ok | 6/6 ok | 0.4677 |
| flow-chart | 1.00 | 0.22 | +0.78 | 3/3 runs | 3/3 ok | 1/2 ok | 0.5111 |
| lesson-set | 1.00 | 0.07 | +0.93 | 3/3 runs | 3/3 ok | nothing-checked | 0.7874 |

8 case(s); cases' run costs (agent + judge) $5.1591; invocations' reported costUsd $5.1591

The whole suite (8 cases × 3 runs × 2 arms = 48 runs) cost **$5.16**; a
development pass of one case at `--runs 1 --ablation none` costs $0.09–0.17.
Without the plugin, Sonnet writes YAML of its own invention (`header:`,
`points:`), which `organizer.py check` partly accepts, and never renders a PDF.
`plot-data` scores 1.00 in both arms on purpose: the plugin must not take a
plotting request (no plugin skill fired in 3/3 with-plugin runs).

## Known limits

- **The description is not what routes.** With lesson-kit's description
  replaced by an unrelated one that says "NOT for … handouts", Sonnet still
  called `learning-organizers:lesson-kit` for "make the handouts for my lesson"
  (mutation run, `--runs 1`): in a one-plugin sandbox the skill's name routes.
  The Skill indicator shows the skill fired, not why.
- **The built-in `dataviz` skill is in both arms.** It is what answers
  `plot-data`, even when "plot this data" is written into graphic-organizer's
  triggers.
- The judge is a model: `llm` graders (two cases) are kept short and positive,
  with one "FAIL only when" list; the routing verdicts rest on regex and
  `file_exists` graders.
- The eval sandbox does not confine what a run's agent may *read*; no run of
  this suite's final measurement named a path outside its sandbox and the
  plugin, but nothing here enforces that.
- Type regexes alone do not separate the arms (the no-plugin agent also writes
  `type: t-chart` when the prompt says "T-chart"); the rendered PDF and the
  learner-PDF graders do. On `01-t-chart` the structural regexes and the checker
  do not either: a no-plugin T-chart with made-up keys (`header:`, `points:`)
  passes `spec-is-a-t-chart` and `spec-has-both-sides`, and the checker reports
  it `ok` while it draws no answers.
