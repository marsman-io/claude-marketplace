# Founder surfaces

A solo founder doesn't have a "codebase" the way a team does. They have a
handful of **surfaces** — the few places where a stranger turns into a
visitor, a visitor into a trial, a trial into a paying customer, and a
customer into someone who stays. The lenses in this plugin all aim at
these surfaces, so this doc names them once, as shared vocabulary, and
every lens refers back to the same four terms.

The hard truth this doc exists to encode: **a surface is wherever the
behavior happens, not wherever the code happens to live.** A founder's
landing page might be a Framer site, their pricing might be three Stripe
products plus a marketing-site table, their backlog might be a Notion
page. When you point Claude Code at the repo, half the surfaces aren't in
it. So each surface below states what *artifact* represents it, where it
*typically* lives in a repo, and the very real chance it lives somewhere
else entirely. Whenever a lens can't find a surface in-repo, that's not a
failure — it's the cue to ask for the pasted markup, the URL, or the
exported page.

## Landing page

**What it is.** The surface where traffic arrives — the first screen a
stranger sees. It carries the promise: who this is for, what changes for
them, and the one action they should take.

**What artifact represents it.** The rendered page and its source markup
— the headline, the hero, the primary call-to-action, the proof, and the
copy in between. For a lens, the artifact is either the source file or a
pasted block of the rendered HTML / a live URL.

**Where it typically lives in a repo.** A root-level entry like
`index.html`, an `app/` or `pages/` route (a home or marketing route),
or component files such as `*.astro`, `*.tsx`, `*.vue`, `*.svelte` under
a `marketing/`, `landing/`, `home/`, or `(marketing)/` directory.

**Where it may live instead.** Very commonly external — a Framer or
Webflow project, a no-code page builder, or a separate marketing site
repo. When it isn't in the repo, a lens must accept pasted markup or a
URL as the target.

## Pricing

**What it is.** The surface where a visitor decides what to pay and why.
It's a *decision* surface, not a list: tiers, what each unlocks, the
anchor, and the path from "interested" to "checked out."

**What artifact represents it.** The pricing page or component, plus the
plan / tier definitions behind it — the names, the prices, the feature
gating, and the call-to-action per tier.

**Where it typically lives in a repo.** A pricing route or component
(`pricing`, `plans`, `Pricing.tsx`, a `/pricing` page), and sometimes a
config or constants file enumerating the tiers.

**Where it may live instead.** Often external — Stripe (Products /
Prices, a Payment Link, or a hosted pricing table) and/or a marketing
site that renders the table separately from the app. The real prices may
only exist in the Stripe dashboard. When the page isn't in the repo, a
lens must accept a pasted pricing table, a screenshot's text, or a URL.

## Onboarding

**What it is.** The path from "just signed up" to first value — the
moment the product does the thing the visitor came for. It's the surface
where activation is won or lost.

**What artifact represents it.** The signup → first-value flow: the auth
screens, the first-run experience, any setup steps, empty states, and the
moment the product delivers its first useful result.

**Where it typically lives in a repo.** `auth/`, `signup`, `login`,
`onboarding`, `welcome`, or `getting-started` routes and components;
first-run / empty-state UI; and the wiring that decides what a brand-new
account sees.

**Where it may live instead.** Partly external — a hosted auth provider
(Clerk / Auth0 / Supabase Auth), an email sequence in a separate tool, or
a Calendly / scheduling step. When the in-repo flow is only a fragment of
the real onboarding, a lens must accept a pasted description of the steps
or a walkthrough of the live flow.

## Analytics / event wiring

**What it is.** The surface that tells the founder whether any of the
above is working. Without it, every other lens is reasoning about a
funnel no one can see.

**What artifact represents it.** The event-tracking calls and their
placement — what's tracked, where, and whether the key moments (page
view, signup, activation, checkout) actually emit events.

**Where it typically lives in a repo.** `track(` calls and analytics SDK
usage — `posthog`, `mixpanel`, `gtag`, `segment`, `analytics.`,
`plausible`, or a thin in-house wrapper — scattered across the surfaces
above, plus an init / provider in the app shell.

**Where it may live instead.** Partly external — a tag manager, a no-code
analytics install snippet, or events configured in the analytics tool's
own dashboard rather than in code. When the wiring isn't visible in the
repo, a lens must accept a pasted snippet, a list of configured events,
or a description of what's tracked.
