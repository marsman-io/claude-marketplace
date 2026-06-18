---
name: code-sample-audit
description: >-
  Audit every code sample in the docs against a hard quality bar — runnable (imports + setup present), copy-pasteable (complete, no bare `...`), shows expected output, error-handled (not just the happy path), idempotent where the operation allows, and at parity across every supported SDK language. Grounded in Google's code-samples style rules (mark omissions with a language COMMENT, never an ellipsis; don't present an incomplete block as click-to-copy; wrap at 80; precede each sample with an intro sentence), Make a README ("show the expected output if you can"), and docs-as-code (test samples in CI so they can't rot). Read-only: it grades each sample and cites where it lives; you fix. Accepts in-repo fenced blocks, a pasted snippet, or a docs URL — "not in repo" is normal. Triggers on "do these code samples work", "audit my code examples", "are the docs examples runnable", "check the snippets", "do the SDK examples match across languages", "are my examples copy-pasteable", "code sample review". NOT for judging whether the SDK itself is idiomatic or has cross-language parity as a library (that's sdk-ergonomics in dx-evaluation-skills); NOT for whether documented symbols still exist on the surface (doc-surface-drift); NOT for Diátaxis fit (docs-diataxis-audit); NOT for prose tone/terminology (style-conformance).
---

# Code Sample Audit

A code sample is the most-copied, least-tested content in any doc. Developers paste it verbatim into a real project, so a sample that doesn't run — or that silently omits the error path — teaches a bug at scale. The highest-confidence move is to EXECUTE the samples (or wire CI to do it), not to eyeball them: a snippet can read perfectly and still fail to compile, miss a required import, or have drifted from the current API. This skill is a READ-ONLY critic. It inventories every sample, grades each against a six-point bar, cites where each lives, and stops; you fix. Boundary: whether the SDK itself is idiomatic or maintains parity as a library is `sdk-ergonomics` in dx-evaluation-skills — THIS audits the SAMPLES printed in the docs.

## When to use
**Do** use when you have code samples (in-repo fenced blocks, a pasted snippet, or a docs URL) and want each graded for runnable / copy-pasteable / shows-output / error-handled / idempotent / cross-language parity. Pasted external artifacts are first-class; "not in repo" is normal.
**Don't** use to assess whether the underlying SDK is idiomatic or at parity as a client library — that's sdk-ergonomics in dx-evaluation-skills. **Don't** use to check whether documented symbols still exist on the shipped surface — that's doc-surface-drift. **Don't** use to classify docs against Diátaxis — that's docs-diataxis-audit. **Don't** use to enforce voice or terminology — that's style-conformance.

## Procedure
1. **Inventory every sample.** Walk the docs and pull each fenced/code block — cite where each lives (file:line, pasted block, or URL anchor) and its surface + language (CLI / SDK-py / SDK-ts / REST / MCP). One row per sample.
2. **Score each against the six-point bar.** (1) RUNNABLE — imports and setup present, would actually execute; (2) COPY-PASTEABLE — complete, omissions marked with a language COMMENT not a bare `...`/ellipsis, and not presented as click-to-copy if incomplete; (3) SHOWS EXPECTED OUTPUT — the result is printed next to the call; (4) ERROR-HANDLED — covers the failure path, not only the happy path; (5) IDEMPOTENT — where the operation allows, re-running doesn't corrupt; (6) PARITY — the same task exists and matches across every supported SDK language.
3. **Flag the two highest-severity defects first:** non-runnable samples, and samples shown as copy-pasteable but truncated with `...`. These actively hand the reader broken code.
4. **Check cross-language parity** by lining up the same task across each SDK language — same steps, same error handling, same shown output. A task present in one language and missing in another is a parity gap.
5. **Recommend wiring sample execution into CI** wherever samples are load-bearing — extract and run them on every build (docs-as-code) so they can't silently rot.

## Output
```
CODE SAMPLE AUDIT — docs/quickstart.md + docs/sdk/*.md (read 2026-06-18)

SAMPLE INVENTORY MATRIX
| Sample (cite)                          | Surface/lang | Runnable? | Copy-paste (no `...`)? | Shows output? | Error-handled? | Idempotent? | Parity? |
|----------------------------------------|--------------|-----------|------------------------|---------------|----------------|-------------|---------|
| "first call" (quickstart.md L40)       | SDK-py       | ✗ no import| ✓                      | ✗             | ✗ happy only   | n/a (read)  | —       |
| "create item" (sdk/py.md L22)          | SDK-py       | ✓         | ✗ `...` mid-block      | ✓             | ✓ try/except   | ✗ no upsert | base    |
| "create item" (sdk/ts.md L18)          | SDK-ts       | ✓         | ✓                      | ✗             | ✗              | ✗           | DRIFT   |
| "create item" (sdk/go.md)              | SDK-go       | —         | —                      | —             | —              | —           | MISSING |
| `curl POST /v1/items` (api.md L70)     | REST         | ✓         | ✓                      | ✗ no response | ✗ no non-2xx   | ✗           | n/a     |
| "call tool" (mcp.md L12)               | MCP          | ✓         | ✓                      | ✓             | ✓              | ✓           | n/a     |

FINDINGS (by severity)
1. NON-RUNNABLE — quickstart.md L40: the first sample a newcomer copies omits `import client`
   and any setup; pasted as-is it raises NameError on line 1. Highest severity: it's the first call.
2. TRUNCATED-BUT-CLICK-TO-COPY — sdk/py.md L22: block is click-to-copy yet contains a bare `...`
   at L27. Per Google, mark omissions with a language COMMENT (e.g. `# ... configure options`) and
   do NOT format an incomplete block as copy-pasteable. Reader pastes uncompilable code.
3. PARITY GAP — "create item" exists for py + ts but is MISSING for the documented Go SDK; and the
   ts version (sdk/ts.md L18) drops the try/catch the py version has — same task, different safety.
4. NO EXPECTED OUTPUT — quickstart.md L40, sdk/ts.md L18, api.md L70 print no result; reader can't
   confirm success (Make a README: "show the expected output if you can").
5. HAPPY-PATH ONLY — quickstart.md L40, sdk/ts.md L18, api.md L70 show no error handling; the REST
   sample shows no non-2xx response.
6. STYLE — confirm 80-char wrap and an introductory sentence before each block (Google).

VERDICT
FAILS the executable bar. The first-call sample doesn't run, one click-to-copy block is truncated,
and the SDK examples are out of parity (Go missing, ts unsafe). Block publish until samples execute.

CI-EXECUTION RECOMMENDATION
- Extract every fenced block and run it on each build (docs-as-code); fail the build on non-zero exit.
- Assert the printed expected-output matches the real run output, so drift is caught mechanically.
- Run the SAME task across py/ts/go in CI to enforce parity — a missing language fails the matrix.
- Treat samples as tested code, not prose, so they can't rot between releases.
```

Failure mode: declaring samples good by reading them — a snippet can look correct and still fail to compile, omit a required import, or have silently drifted from the current API; only executing it (or a CI test that does) is proof.
Sources: Google developer documentation style guide — Code samples (https://developers.google.com/style/code-samples; mark omissions with a language comment not an ellipsis, don't format an incomplete block as click-to-copy, wrap at 80, intro sentence per sample); Make a README (https://makeareadme.com/, "Use examples liberally, and show the expected output if you can"); Write the Docs — Docs as Code (https://www.writethedocs.org/guide/docs-as-code/, test code samples in CI).
