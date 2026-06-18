---
name: style-conformance
description: >-
  Audit documentation PROSE against the Google developer documentation style guide — second person, active voice, present tense, sentence-case headings, conditions-before-instructions, serial commas, code font vs bold, and the banned false-reassurance words (simply, just, easy). Read-only critic: flags every violation with a citation and a concrete rewrite, then summarizes counts per rule so systemic habits surface. Works on in-repo markdown, pasted prose, or a docs URL; "not in repo" is normal. Triggers on "style guide", "passive voice", "use 'you' not 'we'", "remove 'simply'/'just'", "sentence case headings", "conform to Google style", "tighten the wording". NOT for judging whether a page is the right Diátaxis mode (use docs-diataxis-audit) and NOT for checking whether claims match the actual surface (use doc-surface-drift).
---

# Style Conformance

Clear technical prose is mostly a handful of mechanical rules applied relentlessly: write in second person, use active voice, stay in present tense, and never reassure the reader falsely with "simply", "just", or "easy". This skill is a READ-ONLY critic — it judges WORDING, nothing else. Style is downstream of structure: if a page is in the wrong Diátaxis mode, that is docs-diataxis-audit's job, not this one; if the prose confidently documents a flag the tool no longer has, that is doc-surface-drift's job. Stay in your lane. You flag and rewrite; the human edits. Cite or it didn't happen: every violation names the rule, quotes the offending text, and points to a line or paste location.

## When to use
**Do** use when you have a block of prose — in-repo markdown, a pasted draft, or a docs URL — and want it scrubbed against the Google developer documentation style guide, with each issue cited and rewritten.

**Don't** use to decide what KIND of page this should be (docs-diataxis-audit), or to verify that the documented behavior matches the CLI / SDK / REST API / dashboard (doc-surface-drift). Polishing the wording of a structurally wrong or factually false page is wasted work.

## Procedure
1. Get the prose. Read the in-repo `.md`, accept the pasted text, or fetch the docs URL. Note the source so every citation resolves to `file:line` or "pasted".
2. Walk each rule across the full text, one rule at a time:
   - Second person — "you", not "we". (Style guide: "Use second person: 'you' rather than 'we.'")
   - Active voice — make clear who performs the action. (Style guide: "Use active voice: make clear who's performing the action.")
   - Present tense — strike gratuitous "will". (Style guide: "Use present tense.")
   - Conditions before instructions — "If X, do Y", not "Do Y if X".
   - Sentence case for titles and section headings.
   - Banned reassurance — "easy / easily / simply / just". (Style guide word list, easy/easily: "What might be easy for you might not be easy for others. Try eliminating this word from the sentence because usually the same meaning can be conveyed without it.")
   - Serial (Oxford) commas in lists of three or more.
   - Code font for code-related text in prose; UI element labels in bold.
   - Minor checks: 80-character line wrap on source; numbered lists for ordered sequences, bulleted otherwise.
3. For every violation, capture the exact offending phrase WITH a citation and a concrete rewrite. No vague "this reads passively" — quote it and fix it.
4. Summarize counts per rule so systemic habits (passive voice on every line, "we" throughout) surface as patterns rather than scattered nits.
5. Mark anything ambiguous (could be intentional, domain term, quoted source) as a flag rather than over-counting it as a violation.

## Output
```
# Style conformance — <docs/cli/install.md | pasted | https://example.com/docs/install>
Guide: Google developer documentation style guide (developers.google.com/style)

## Violations
| Rule | Offending text (cite) | Why | Suggested rewrite |
|------|----------------------|-----|-------------------|
| Second person | "we recommend running the installer first" (install.md:12) | Guide: use "you", not "we" | "Run the installer first." |
| Active voice | "the config file is read at startup" (install.md:24) | Passive — actor hidden | "The CLI reads the config file at startup." |
| Present tense | "the command will create a token" (install.md:31) | Gratuitous future | "The command creates a token." |
| Condition order | "Run `init` to set up the project if it's empty." (install.md:40) | Condition trails instruction | "If the project is empty, run `init` to set it up." |
| Banned word | "just run the command and you're done" (install.md:7) | "just" minimizes effort | "Run the command." |
| Banned word | "setup is easy" (pasted ¶2) | "easy" — see word list | Delete; state what setup requires instead. |
| Sentence case | "## Configuring Your API Key" (install.md:50) | Title case heading | "## Configuring your API key" |
| Serial comma | "tokens, scopes and refresh tokens" (install.md:58) | Missing Oxford comma | "tokens, scopes, and refresh tokens" |
| Code font | "set the API_KEY variable in plain text" (install.md:62) | Code term not in code font | "Set the `API_KEY` variable." |
| UI element | "click submit" (dashboard.md:9) | UI label not bold | "click **Submit**" |
| Ambiguous (flagged) | "we" in "we deprecated v1" (notes.md:3) | May be intentional org voice | Confirm before rewriting. |

## Per-rule summary
| Rule | Violations | Systemic? | Verdict |
|------|-----------|-----------|---------|
| Second person | 14 | yes | "we" is the default voice here — sweep the whole file. |
| Active voice | 9 | yes | Passive constructions dominate procedural steps. |
| Present tense | 5 | no | Scattered "will"; clean per instance. |
| Condition order | 3 | no | Reorder the three flagged sentences. |
| Banned words | 6 | yes | "just"/"easy" recur in the intro — strip the reassurance. |
| Sentence case | 4 | yes | All H2s use title case; convert all headings. |
| Serial comma | 2 | no | Two lists missing the Oxford comma. |
| Code font / UI bold | 7 | yes | Code and UI terms run as plain prose throughout. |

Verdict: prose is fixable in place; dominant habits are first-person voice and passive constructions.
Not checked: Diátaxis mode (docs-diataxis-audit) and claim-vs-surface accuracy (doc-surface-drift).
```

Failure mode: bikeshedding the wording of a page that is in the wrong Diátaxis mode or that documents a flag the tool no longer has — polishing prose that is structurally broken or factually false, which this skill cannot detect (that's docs-diataxis-audit and doc-surface-drift).
Sources: Google developer documentation style guide — https://developers.google.com/style (highlights at https://developers.google.com/style/highlights); word list — https://developers.google.com/style/word-list.
