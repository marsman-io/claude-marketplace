---
name: api-error-model-audit
description: Conformance review of an HTTP/REST API against industry guidelines (Stripe, Google AIP, Microsoft, RFC 9457) — centered on the error model, plus pagination, versioning, idempotency, rate limits, auth, streaming, and contracts. Use when you have an API (OpenAPI/spec file, live base URL, or pasted endpoint/error samples) and need to judge whether its error envelope is consistent and its evolution safe. Triggers on "api review", "error model audit", "rest api design", "is the error envelope consistent", "pagination versioning idempotency audit", "problem+json", "are our errors machine-readable". NOT for client-library ergonomics that wrap this API (→ sdk-ergonomics), NOT for MCP tool surfaces (→ mcp-server-ux), NOT for command-line tools (→ cli-conformance).
---

# API Error Model Audit

The success path of a REST API is the part everyone tests; the error path is the part that decides whether clients can build anything reliable on top of it. An inconsistent error envelope forces every client to string-match human-readable `message` text, which breaks the day someone fixes a typo. This skill reviews one HTTP API against the established guidelines — RFC 9457 Problem Details, Google AIP, Microsoft, Stripe — with the error model as the load-bearing center, then checks the cross-cutting contracts (pagination, versioning, idempotency, rate limits) that are breaking changes to retrofit. It diagnoses; it does NOT edit the API or its product code. You read the OpenAPI spec, hit the endpoints, or take pasted samples, find the divergence, and hand back the tables — then a human intervenes.

## When to use

**Do** use when:
- You have one API to audit — an OpenAPI 3.1 file, a live base URL, or pasted request/response/error samples.
- You need a cite-backed verdict on error-envelope consistency and on the safety of pagination/versioning/idempotency.
- "Not in repo" is fine: a spec file or a handful of pasted error bodies is a valid target.

**Don't** use when:
- You're reviewing the SDK/client library that calls this API (→ sdk-ergonomics).
- The surface is an MCP server whose tools wrap the API (→ mcp-server-ux).
- It's a CLI (→ cli-conformance).

## Checklist

Verify each. Cite the proof (spec `file:line`, a pasted response body + status, or the exact URL). "Couldn't verify from the artifact" is a valid finding.

**Resources**
- [ ] Resource-oriented design, plural nouns (`/invoices/{id}`), no verbs in URLs (`/createInvoice` is wrong).
- [ ] Correct verbs and status codes: `POST`→201+Location, `GET`→200, `PUT/PATCH`→200, `DELETE`→204, not-found→404, conflict→409.

**Error envelope (the core)**
- [ ] ONE consistent envelope across EVERY endpoint — same shape for 400, 404, 409, 422, 500.
- [ ] RFC 9457 Problem Details: `Content-Type: application/problem+json` with `type` (URI that resolves to docs), stable `title`, `status`, instance-specific `detail`, and `instance`.
- [ ] A machine-readable code beyond the status — Google AIP-193 style `reason` + `domain` (or equivalent stable enum) the client switches on.
- [ ] Validation errors keyed by field (which field failed and why), not one flat string.
- [ ] A correlation / `requestId` in EVERY error body (and ideally a response header) for support triage.
- [ ] Clients are NEVER expected to string-match the human-readable `message`/`detail`.

**Pagination**
- [ ] Cursor/token-based (opaque, URL-safe), NOT offset/`page` — offset drifts under concurrent inserts and degrades at scale.
- [ ] `page_size` optional with a documented default; over-max is coerced down, not rejected.
- [ ] An empty `next_page_token` is the ONLY end-of-results signal (no separate `has_more` that can disagree).
- [ ] Pagination is present from day one on any list endpoint — adding it later is a breaking change.

**Idempotency**
- [ ] `PUT`/`DELETE` are idempotent by nature (verified, not assumed).
- [ ] Creating `POST`s accept an `Idempotency-Key` header.
- [ ] Key → response is stored ≥ 24h; a duplicate key + same body replays the stored response.
- [ ] A duplicate key + DIFFERENT body returns 409/422, not a silent second create.

**Versioning & deprecation**
- [ ] Explicit, documented versioning scheme (URL, header, or date).
- [ ] A breaking change creates a new major; non-breaking ADDITIONS never bump the version.
- [ ] At most ~2 concurrent versions supported.
- [ ] Deprecation announced via `Deprecation` + `Sunset` headers (RFC 8594), `Link rel="successor-version"`, a published timeline, and a migration guide.

**Rate limits**
- [ ] `RateLimit-Limit` / `RateLimit-Remaining` / `RateLimit-Reset` returned.
- [ ] `Retry-After` is REQUIRED on every 429.
- [ ] Limits are per-client (API key / token), not per-IP, and are documented.

**Auth / streaming / contracts**
- [ ] `Authorization: Bearer` with scopes; 403 for insufficient scope, 401 for missing/expired credential (distinguished).
- [ ] Any streaming endpoint (SSE/NDJSON) has explicit framing, a heartbeat/keep-alive, and resumability (`Last-Event-ID` or cursor).
- [ ] Concurrency control via `ETag` + `If-Match` where lost-updates matter.
- [ ] OpenAPI 3.1 is the single source of truth and matches actual responses.
- [ ] NEVER `Access-Control-Allow-Origin: *` on authenticated routes.
- [ ] Webhooks are signed (and the signature scheme is documented).

## Procedure

Gather the surface cheaply first, then walk the checklist once.
1. Get the contract: open the OpenAPI 3.1 file if present, else collect ~5 real responses — one success and as many distinct error statuses as you can trigger (400/401/403/404/409/422/429/500). Capture full bodies AND headers.
2. Pin the error envelope first: lay every error body side by side and check it's literally the same shape. Divergence here invalidates everything downstream.
3. Walk the remaining groups, recording ✓ / ✗ / partial with citations.

This audit is partly AUTOMATABLE: a CI contract test can hit each documented status code and assert the response is `application/problem+json` with the required fields and a `requestId`, and assert `Retry-After` is present on 429 — turning envelope consistency into a build gate.

## Output

```
## Error-model audit
| Status | `type` suffix | `title` | When returned | Machine code? | requestId? |
|--------|---------------|---------|---------------|---------------|------------|
| 404 | /errors/not-found | Resource not found | id no match | reason=NOT_FOUND domain=… | yes/no |
| 422 | /errors/validation | Validation failed | bad field | field-keyed | yes/no |
| 429 | /errors/rate-limited | Too many requests | quota hit | reason=RATE_LIMITED | yes/no |

## Pagination / versioning / idempotency conformance
| Concern | Status | Evidence | Enforced-by |
|---------|--------|----------|-------------|
| cursor (not offset) pagination | ✓/✗/partial | spec:line or URL | CI contract test / none |
| Idempotency-Key on creating POST | … | … | … |
| versioning + Deprecation/Sunset | … | … | … |
| Retry-After on 429 | … | … | … |

## Deprecation timeline register
| Version / endpoint | Deprecated on | Sunset on | Successor | Migration guide |
|--------------------|---------------|-----------|-----------|-----------------|
| v1 /old | 2026-01-01 | 2026-07-01 | v2 /new | URL |
```

Failure mode of this method: auditing the spec instead of the wire — OpenAPI can declare a tidy `problem+json` envelope on every error while the running service still emits a framework's default `{"error":"..."}` on the paths nobody documented, so any envelope row not backed by a real captured response is a claim, not a finding.
