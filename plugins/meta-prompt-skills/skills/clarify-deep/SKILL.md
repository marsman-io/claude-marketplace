---
name: clarify-deep
description: Before acting on an ambiguous or high-stakes request, gather context yourself first, then ask a few deep, blind-spot-revealing clarifying questions. Triggers on "ask me clarifying questions first", "clarify before you build", "what do you need to know before starting", or as a discipline to apply to any large/vague task. NOT for trivial requests with an obvious default, NOT a license to interrogate — few deep questions, never many shallow ones.
---

# Clarify deep

Gather enough information *before* you ask, then ask questions that reveal blind
spots — not questions whose answers you could have found yourself.

## Procedure

1. **Gather first.** Read the repo, the existing artifacts, the pasted material,
   the conventions. Most "clarifying questions" are answerable from context. A
   question you could have resolved by reading is noise and erodes trust.

2. **Find the real decisions.** From what you gathered, surface the forks where
   the request genuinely underdetermines the outcome — where two reasonable
   builders would do different things, or where the user is making a choice they
   may not realize they're making (the blind spot). These are worth asking about.

3. **Ask few, deep.** Prefer 2–4 questions over a checklist. Each should:
   - target a decision that changes what you build, not a detail with a safe default
   - reveal a tradeoff or assumption the user may not have surfaced
   - be answerable in a sentence, not an essay

   Skip the obvious. "What framework?" when the repo already commits to one is a
   wasted question. "Should the mined corrections stay private, given this repo
   is public?" is a blind-spot question.

4. **Recommend, don't just enumerate.** Where you have a view, give it — lead
   with the option you'd pick and say why. Asking is not an excuse to offload the
   thinking.

5. **Pin the answers.** Record what you learn into the spec / a note / memory so
   you don't ask the same thing twice. Then proceed.

## When to skip

If the request is small and has an obvious default, don't ask — pick the default,
state it in one line, and proceed. Over-asking is its own failure mode.
