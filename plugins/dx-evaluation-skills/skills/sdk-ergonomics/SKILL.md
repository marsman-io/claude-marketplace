---
name: sdk-ergonomics
description: Review of a client library for idiomatic feel, naming, defaults, types, and runtime ergonomics against the Azure SDK Design Guidelines and the target language's own idiom. Use when you have an SDK/client library (in-repo source, generated reference docs, or pasted usage snippets) and need to judge whether it feels native, names things consistently, and handles pagination/retries/errors well. Triggers on "sdk review", "client library ergonomics", "is the sdk idiomatic", "sdk naming pagination errors", "sdk parity across languages", "review the client library", "does this sdk feel native". NOT for the HTTP API the SDK wraps (→ api-error-model-audit), NOT for an MCP server surface (→ mcp-server-ux), NOT for a command-line tool (→ cli-conformance).
---

# SDK Ergonomics

A client library is the only part of a service most developers ever read, and it succeeds when the first call is a one-liner and the hundredth call still feels native to the language. This skill reviews one SDK against the Azure SDK Design Guidelines and the host language's idiom: does it name things the way the language does, distinguish unset from empty, paginate lazily, retry with backoff, and translate HTTP failures into typed exceptions that carry the request id? It diagnoses; it does NOT edit the library or its product code. You read the source, the reference docs, or pasted snippets, find the non-idiomatic leaks, and hand back the tables — then a human intervenes. Review ONE language surface per invocation; cross-language parity is judged against that one.

## When to use

**Do** use when:
- You have one client library to audit — its source, generated reference docs, or pasted construction/usage snippets.
- You need a cite-backed verdict on idiom, naming, types, and runtime behavior.
- "Not in repo" is fine: a published reference page or a few usage snippets is a valid target.

**Don't** use when:
- The concern is the underlying HTTP API's design/errors/pagination (→ api-error-model-audit).
- The surface is an MCP server (→ mcp-server-ux) or a CLI (→ cli-conformance).

## Checklist

Verify each. Cite the proof (`file:line`, a reference-doc snippet, or the pasted code). "Couldn't verify from the artifact" is a valid finding.

**Idiomatic & consistent**
- [ ] Feels native to the language (uses its iterators, context managers/disposables, error model, naming case — not a transliteration of another language's SDK).
- [ ] Consistency priority order honored: within-language > with-service > across-languages.
- [ ] Service-agnostic concerns — logging, HTTP pipeline, auth, retries, error shape — behave IDENTICALLY across the org's SDKs.
- [ ] Feature parity across languages is prioritized (no language is a second-class citizen missing whole capabilities).

**Naming**
- [ ] Client types end in `Client`; option/config bags end in `Options`.
- [ ] Standardized verb prefixes used consistently across ALL languages: `create` / `get` / `list` / `update` / `delete` / `exists`.
- [ ] Methods read `verb + resource` (`getInvoice`, not `invoiceFetch`).
- [ ] Abbreviations ≤ 3 chars are fully capitalized — `GetAPIToken`, not `GetApiToken`.
- [ ] No marketing / brand / codename strings in public identifiers.
- [ ] No Get-vs-List confusion (`get` returns one and 404s if absent; `list` returns a possibly-empty collection).

**Approachable**
- [ ] One-liner construction with sensible defaults: `Client(api_key=...)` and you're working.
- [ ] Advanced configuration is AVAILABLE but does not complicate the basic happy path.
- [ ] Samples are runnable real-world tasks, not a method-by-method dump of the spec.

**Types**
- [ ] Request/response types are generated (not hand-maintained and drifting).
- [ ] Nested JSON is mapped to native classes/structs, not raw dicts/maps the caller index-keys.
- [ ] OPTIONAL fields are distinguishable from zero values — unset ≠ `0`/`""`/`false`/empty (nullable / `Optional` / pointer / presence flag).
- [ ] Closed sets are enums, not bare strings.

**Runtime ergonomics**
- [ ] Automatic pagination via a lazy iterator, PLUS an eager "give me the whole list" option.
- [ ] Built-in retries with backoff; idempotency-key handling on retried creates; configurable timeouts; rate-limit awareness (respects `Retry-After`).
- [ ] Idiomatic TYPED exceptions translating HTTP status + body — e.g. `RateLimitError`, `AuthError`, `NotFoundError` — each carrying the request id; raw status codes never leak to the caller.
- [ ] Context-manager / disposable cleanup for connections and clients.
- [ ] Auth is configured once on the client; the caller never hand-builds per-call auth headers.

**Sustainability**
- [ ] Versioned in lockstep with the service.
- [ ] Deprecations surfaced as first-class language warnings (deprecation attribute/annotation), not just doc text.
- [ ] Generated in CI so the SDK stays at parity with the spec instead of drifting.

## Procedure

Gather the interface cheaply first, then walk the checklist once.
1. Get the surface: read the public entrypoint / client class and the generated model types, OR take the reference docs / pasted snippets. Find the construction call, one `list` method, and the error types.
2. Anchor on three concrete snippets — construct the client, list a paginated resource, handle a failure — and judge them against the language's idiom before scoring naming/types.
3. Walk the remaining groups, recording ✓ / ✗ / partial with citations, and collect every non-idiomatic leak you spot.

This audit is partly AUTOMATABLE: a CI lint can assert the naming rules (client types end `Client`, verb prefixes from the allowed set, abbreviation casing) by reflecting over the public surface, and assert error types subclass the SDK's base exception — turning naming/error conformance into a build gate.

## Output

```
## Per-language ergonomics review
| Construction snippet | Naming conformance | Pagination style | Retry/idempotency | Error-type mapping | Parity gaps |
|----------------------|--------------------|------------------|-------------------|--------------------|-------------|
| `Client(api_key=…)` | ✓ / ✗ GetApiToken | lazy iter + list() | backoff, idem-key | typed, carries req id | missing async |

## Cross-language consistency matrix
| Concern | Lang A | Lang B | Lang C | Consistent? |
|---------|--------|--------|--------|-------------|
| verb prefixes | ✓ | ✓ | partial | no |
| retry/backoff defaults | … | … | … | … |
| typed errors + request id | … | … | … | … |

## Non-idiomatic leaks
- file:line — raw `dict` returned where a typed model is expected
- file:line — `bool` field can't distinguish unset from `false`
```

Failure mode of this method: scoring the SDK against another language's idiom — a library can be a perfect mechanical port and still feel alien, so any "idiomatic" verdict not grounded in THIS language's own conventions (its iterator protocol, error model, naming case) is taste dressed up as a finding.
