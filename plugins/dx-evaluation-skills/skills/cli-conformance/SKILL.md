---
name: cli-conformance
description: Heuristic review of a command-line program against the Command Line Interface Guidelines (clig.dev) — taxonomy, exit codes, stream discipline, help, output modes, flags, robustness, and config precedence. Use when you have a CLI (in-repo source, a `--help` dump, or a pasted command list) and need to judge whether it is well-behaved and scriptable. Triggers on "cli review", "clig.dev", "command line usability", "is this cli well-behaved", "audit the cli", "cli conformance", "does this command follow unix conventions". NOT for client-library or SDK idiom review (→ sdk-ergonomics), NOT for cataloguing a tool's error/failure states (→ failure-state-matrix).
---

# CLI Conformance

A CLI is an API whose users are humans at a terminal and scripts in a pipeline, and it is judged by the same conventions both have relied on for fifty years: data on stdout, noise on stderr, semantic exit codes, no surprises when piped. This skill walks one command-line program against the clig.dev guidelines and reports where it breaks those conventions — because every break is a paper cut that costs a user a debugging session or a script a silent corruption. It diagnoses; it does NOT edit product code. You read the source, the `--help` output, or a pasted command list, you find the gaps, and you hand back a taxonomy table and a compliance matrix — then a human intervenes.

## When to use

**Do** use when:
- You have one CLI to audit — its source tree, a captured `--help` dump, or a pasted list of commands/flags.
- You need a concrete, cite-backed verdict on scriptability and human usability.
- "Not in repo" is fine: a `--help` paste or a man page is a valid target.

**Don't** use when:
- The thing under review is a client library / SDK surface (→ sdk-ergonomics).
- You only want an inventory of error states and recovery affordances (→ failure-state-matrix).
- It's an HTTP API with a CLI wrapper — audit the API separately (→ api-error-model-audit).

## Checklist

Verify each. Cite the proof (`file:line`, a pasted `--help` block, or the exact command output). "Couldn't verify from the artifact" is a valid, honest finding.

**Taxonomy**
- [ ] Uses a real argument parser (not hand-rolled `argv` slicing that drops `--`/`=`/clustered short flags).
- [ ] Consistent `noun verb` (or `verb noun`) grammar across all subcommands — not a mix.
- [ ] No catch-all god subcommand that hides ten unrelated behaviors behind one name.

**Exit codes**
- [ ] `0` on success, non-zero on any failure (checked, not assumed).
- [ ] SEMANTIC codes, not just 0/1 — distinct codes for distinct failure classes so scripts can branch (e.g. usage error vs. not-found vs. network vs. auth).
- [ ] Exit codes are documented somewhere a script author can find them.

**Streams**
- [ ] stdout carries the primary data ONLY (the thing you'd pipe into `jq`/`grep`).
- [ ] stderr carries logs, diagnostics, progress, and prompts.
- [ ] The two are never interleaved on stdout; piping stdout yields clean machine-parseable data.

**Help & discoverability**
- [ ] `-h` and `--help` both work on the root AND every subcommand.
- [ ] Help LEADS with copy-pasteable examples, before the exhaustive flag list.
- [ ] Most-common flags listed first, not alphabetically buried.
- [ ] "Did you mean …?" suggestion on an unknown command/typo.
- [ ] `--version` present and prints a real version.

**Output**
- [ ] Brief on success, but still REPORTS state changes ("created X", "deleted 3").
- [ ] `--json` and/or `--format` for machine-readable output.
- [ ] TTY detection: color, spinners, and progress bars disabled when stdout is not a terminal (piped/redirected).
- [ ] Honors `NO_COLOR` and a `--no-color` flag.
- [ ] `--quiet` and `--verbose` adjust verbosity without changing the data on stdout.

**Args & flags**
- [ ] Long `--flags` with single-char aliases for the common ones.
- [ ] Honors standard names where applicable: `-v`/`--verbose`, `-o`/`--output`, `-f`/`--force` or `--file`, `--dry-run`.
- [ ] Destructive actions require confirmation OR an explicit flag (no silent `rm -rf`-equivalent).
- [ ] `--dry-run` shows what would happen without doing it.
- [ ] `--force`/`--yes` exists so scripts can skip prompts.
- [ ] Secrets accepted via env var or stdin, NEVER a plain flag value that leaks into shell history / `ps` output.
- [ ] Good defaults — the common case needs the fewest flags.

**Robustness**
- [ ] Graceful SIGINT (Ctrl-C): cleans up temp files / partial state, doesn't leave a corrupt lock.
- [ ] Idempotent where the operation allows it (re-running a create is a no-op or a clear "already exists").
- [ ] Network calls have timeouts with a clear message on timeout — not an indefinite hang.
- [ ] Never prompts interactively when stdin is not a TTY; fails with a clear message instead.

**Config**
- [ ] Documented precedence: flags > env vars > project config > user config > built-in defaults.
- [ ] Config/state/cache files live in XDG-respecting locations, not dotfiles scattered in `$HOME`.

## Procedure

Gather the interface cheaply first, then walk the checklist once.
1. Get the surface: `<cmd> --help`, then `<cmd> <sub> --help` for each subcommand (or read the parser-definition file in source, or take the pasted dump). Run `<cmd> | cat` and `<cmd> > /dev/null` mentally/actually to check TTY behavior and stream split.
2. Walk every checklist group in order. For each item record ✓ / ✗ / partial with a citation.
3. Build the two artifacts. Where a finding is unverifiable from the artifact you have, say so rather than guessing.

This audit is partly AUTOMATABLE: the compliance matrix can be generated by a CI conformance test that walks the command tree (parse `--help` on every node, assert `-h`/`--help`/`--version` exist, assert stderr/stdout split on a piped run, assert non-zero exit on a known-bad input). Recommend wiring that test where the gaps are mechanical.

## Output

```
## Command taxonomy
| Command | Purpose | Flags | Exit codes | Output mode | Idempotent? |
|---------|---------|-------|------------|-------------|-------------|
| <cmd sub> | … | --flag (-f), --dry-run | 0 ok / 3 not-found / 4 auth | text, --json | yes/no/n/a |

## clig.dev compliance matrix
| Guideline | Status | Evidence | Enforced-by |
|-----------|--------|----------|-------------|
| stdout = data, stderr = logs | ✓/✗/partial | file:line or `--help` block | CI conformance test / none |
| semantic exit codes | … | … | … |
| help leads with examples | … | … | … |
| NO_COLOR / TTY detection | … | … | … |
| secrets not via plain flags | … | … | … |
| config precedence documented | … | … | … |
```

Failure mode of this method: a green matrix from reading `--help` alone — the help text can promise `--json` and semantic exit codes the binary doesn't actually honor, so any row not backed by an executed command or a source line is a guess, not a finding.
