# developer-docs-skills

A flat collection of ten codebase-neutral skills for **writing and auditing the
documentation of a multi-surface developer tool** — a product that spans a CLI,
an SDK, a REST API, an MCP server, a desktop/Electron dashboard, an
installer/upgrade flow, and the docs themselves. For such a tool, documentation
is not a nicety: it is the activation surface, and in survey after survey it is
among the top factors developers weigh before adopting an API at all.

This is the third plugin in a trio. Its siblings
[`experience-mapping-skills`](../experience-mapping-skills) *map* the surfaces and
[`dx-evaluation-skills`](../dx-evaluation-skills) *evaluate* them; these skills
*document* them. The intended arc is **map → evaluate → document**.

The whole collection is built on one idea, from the **Diátaxis** framework:
there are exactly four kinds of documentation — **tutorial, how-to guide,
reference, explanation** — each serving a different need, and *mixing them on one
page is the primary documentation failure*. Six skills here help you write each
mode well; four audit what you already have.

No agents, no shared docs. Each skill stands alone — install the plugin and the
skills fire on the phrasings in their descriptions, or invoke one directly. Each
accepts an **in-repo target or a pasted/external artifact** (a `--help` dump, an
OpenAPI spec, a URL, pasted markdown), because these surfaces rarely all live in
one repo — "not in the repo" is a normal path, not an error.

## Skills

### Diátaxis core

| Skill | Does | Fires on |
|---|---|---|
| `docs-diataxis-audit` | **The flagship.** Classifies every existing page into one of the four Diátaxis modes, flags pages that mix modes (the #1 failure), and finds the missing quadrants per surface. | "diataxis audit", "classify our docs", "are the docs mixing tutorial and reference", "what docs are missing" |

### Generative — write one mode well

| Skill | Produces | Fires on |
|---|---|---|
| `quickstart-builder` | The canonical install → auth → first call → verify quickstart, headless and copy-pasteable, with an explicit time-to-first-success target. | "write a quickstart", "getting started page", "time to first call", "hello world doc" |
| `tutorial-scaffold` | A **learning-oriented** tutorial: a guaranteed-success guided lesson, no choices, no explanation, no error-handling detours. | "write a tutorial", "learning-oriented guide", "teach a beginner", "first-time lesson" |
| `how-to-recipe` | A **task-oriented** recipe: a real-world goal, assumes competence, a sequence of actions with no teaching. | "how-to guide", "write a recipe", "task-oriented doc", "how do I <verb> doc" |
| `explanation-doc` | An **understanding-oriented** page: the why, the mental model, the trade-offs and history — discursive, not instructional. | "explanation doc", "concept page", "explain why", "background / discussion doc", "mental model" |
| `reference-from-spec` | **Information-oriented** reference, machine-generated from an OpenAPI spec / `--help` dump / type signatures — complete, accurate, describe-and-only-describe. | "generate reference docs", "api reference from openapi", "cli reference from --help", "reference from spec" |

### Read-only critics

| Skill | Audits against | Fires on |
|---|---|---|
| `readme-audit` | standard-readme + Make a README, weighted for a dev tool (install, runnable first call, expected output, links to each surface). | "readme review", "audit the readme", "is our readme good", "readme standard" |
| `doc-surface-drift` | The docs vs the actual surfaces — documented flags vs `--help`, documented endpoints/fields vs the OpenAPI spec, documented symbols vs the SDK. Partly machine-checkable. | "docs drift", "are the docs out of date", "docs vs the actual cli/api", "stale documentation" |
| `style-conformance` | The Google developer documentation style guide — second person, active voice, present tense, sentence-case headings, no "simply/just/easy". | "docs style review", "google style guide", "tone and voice audit", "is the writing clear" |
| `code-sample-audit` | Every code sample: runnable, copy-pasteable, complete (no `...`), error-handled, idempotent, cross-language parity. | "code sample review", "are the examples runnable", "audit the snippets", "sample parity" |

## A note on the methods

Every skill is grounded in an authoritative source — the **Diátaxis** framework
(diataxis.fr, Daniele Procida), the **Google developer documentation style
guide** (developers.google.com/style), **Write the Docs** and the docs-as-code
philosophy (writethedocs.org), the **standard-readme** spec and **Make a
README** — then weighted for a developer tool, where the same concept must be
documented consistently across surfaces, reference can and should be generated
from the spec so it never drifts, and the fastest path to a developer's first
success is the highest-leverage page you own. Each skill cites its sources.

## Conventions all skills share

- **Diátaxis-pure.** Each generative skill produces exactly one mode and refuses
  to blend; each audit can name the mode a page is violating.
- **Codebase-neutral.** No product is hardcoded; the surfaces are the generic
  CLI / SDK / REST API / MCP / dashboard / installer / docs.
- **Accepts external / pasted artifacts.** A `--help` dump, an OpenAPI spec, a
  URL, or pasted markdown is a first-class target; "not in-repo" is normal.
- **Single target.** One page, one mode, one surface per invocation.
- **Drift is machine-checkable.** Where docs can be diffed against a spec or
  `--help`, the skill says so and recommends wiring a CI check.
- **Cite-or-it-didn't-happen.** Every finding ties to a `file:line`, a pasted
  block, or a URL.
- **Shared vocabulary.** Skills reference the same surfaces and the same dev-tool
  lifecycle — discover → install → authenticate → first-success → integrate →
  operate/debug → upgrade → rollback — so their output composes with the sibling
  plugins.

## Layout

```
.claude-plugin/plugin.json
README.md
skills/
  docs-diataxis-audit/SKILL.md
  quickstart-builder/SKILL.md
  tutorial-scaffold/SKILL.md
  how-to-recipe/SKILL.md
  reference-from-spec/SKILL.md
  explanation-doc/SKILL.md
  readme-audit/SKILL.md
  doc-surface-drift/SKILL.md
  style-conformance/SKILL.md
  code-sample-audit/SKILL.md
```

## Install

```
/plugin install developer-docs-skills@claude-marketplace
```

## License

MIT.
