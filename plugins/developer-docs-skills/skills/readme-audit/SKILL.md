---
name: readme-audit
description: >-
  Audit a project README against the standard-readme spec and Make a README, weighted for a developer tool — does it carry the required sections, in the required order, with License last, and (the part that actually matters) does it get a stranger to a working first call with visible output? Read-only: grade the README, cite every finding to a line or pasted block, and let the maintainer fix it. Works on an in-repo README, a pasted README, or a raw URL — "not in repo" is normal. Triggers on "audit my README", "is my README any good", "does my README follow standard-readme", "grade this README", "README review", "check my README sections". NOT for grading the whole docs set against Diátaxis (docs-diataxis-audit), for detecting README claims that drift from the shipped CLI/SDK/API surfaces (doc-surface-drift), for writing the missing Install/Usage from scratch (quickstart-builder), for checking voice/terminology rules (style-conformance), or for verifying that fenced code blocks actually run (code-sample-audit).
---

# README Audit

A README is the storefront and the single fastest funnel to first success; a stranger lands here before anything else and decides in seconds whether your tool is worth their afternoon. For a developer tool its most important job is not prose — it is a copy-pasteable FIRST CALL with the expected output printed right next to it, plus links out to each surface's deeper docs rather than a wall of inlined detail. The standard-readme spec fixes which sections must exist and in what order; Make a README fixes the spirit: "Use examples liberally, and show the expected output if you can." This skill is a READ-ONLY critic. It diagnoses presence, order, and the usable-without-reading-the-code bar, cites each finding, and stops; the maintainer fixes.

## When to use
**Do** use when you have a README (in repo, pasted, or a raw URL) and want it graded for required sections, correct order, and whether a newcomer can make one successful call from it alone.
**Don't** use to grade the whole documentation set against Diátaxis — that's docs-diataxis-audit. **Don't** use to catch README claims that no longer match the shipped CLI/SDK/REST API/MCP server — that's doc-surface-drift. **Don't** use to author the missing Install or Usage section — that's quickstart-builder. **Don't** use to enforce tone, terminology, or heading conventions — that's style-conformance. **Don't** use to actually execute the fenced examples — that's code-sample-audit.

## Procedure
1. Get the README cheaply: read `README.md` at repo root, or take the pasted block, or fetch the raw URL. Note line count (the Table of Contents requirement is waived under 100 lines).
2. Walk the standard-readme required sections once, in order: Title → Short Description → Long Description → Table of Contents → Install → Usage → (optional API) → Maintainers → Contributing → License. For each, record present?, order-OK?, and evidence (file:line or quoted block).
3. Check the License-last rule explicitly — License MUST be the final section; anything after it fails.
4. Apply the dev-tool weighting: Short Description present and under 120 chars and matching the package/repo description; Install has a real code block; Usage has a COPY-PASTEABLE first call WITH expected output shown; per-surface doc links exist (CLI reference / SDK / REST API / MCP server) instead of inlined detail.
5. Run the bar — quote it: "Your documentation is complete when someone can use your [project] without ever having to look at its code." Name the exact spot where a stranger would have to open the source. Mark anything you cannot confirm from the text as unverifiable.

## Output
```
README AUDIT — ./README.md (218 lines; ToC required)

SECTION-PRESENCE MATRIX (standard-readme order)
Section            | Required? | Present? | Order OK? | Evidence
-------------------|-----------|----------|-----------|----------------------------------
Title              | yes       | ✓        | ✓         | L1 "# acme-cli"
Short Description   | yes       | ✓        | ✓         | L3 (94 chars — see checklist)
Long Description    | no        | ✓        | ✓         | L5–L11
Table of Contents   | yes(>100) | ✗        | n/a       | no ToC found; file is 218 lines
Install             | yes       | ✓        | ✓         | L40 "## Install" + fenced block L42
Usage               | yes       | partial  | ✓         | L70 "## Usage"; no expected output
API (optional)      | optional  | ✗        | n/a       | links to SDK docs instead (OK)
Maintainers         | yes       | ✓        | ✓         | L180
Contributing        | yes       | ✓        | ✓         | L190
License             | yes       | ✗ order  | ✗         | L205, but "## Acknowledgements" L212 follows

DEV-TOOL CHECKLIST
[✓] Short description present, <120 chars ......... 94 chars, L3
[✗] Short desc matches repo/package description ... README L3 vs package "..." differ — reconcile
[✓] Install has a real code block ................. ```sh npm i acme-cli``` L42
[partial] Usage has copy-pasteable first call ..... `acme run hello` L72 — runnable, but...
[✗] ...expected output shown ...................... no output printed after L72 (Make a README rule)
[partial] Per-surface doc links present ........... CLI ref L120, SDK L150; REST API + MCP server: none
[✗] License is the LAST section ................... Acknowledgements (L212) comes after License (L205)

VERDICT
FAILS the "usable without reading the code" bar. A stranger reaches Usage L70, runs
`acme run hello`, and has no shown output to confirm success — and must open the source
to learn what a passing run looks like. Fix: add expected output under L72, add the ToC,
move License to last, and link REST API + MCP server docs. (Unverifiable: whether L42's
install command resolves — out of scope; see code-sample-audit.)
```

Failure mode: ticking that a "Usage" section EXISTS while never checking that its example actually runs and shows output — a README can carry every required heading in perfect order and still leave a stranger unable to make a single successful call.
Sources: standard-readme spec — https://github.com/RichardLitt/standard-readme (spec.md); Make a README — https://makeareadme.com/.
