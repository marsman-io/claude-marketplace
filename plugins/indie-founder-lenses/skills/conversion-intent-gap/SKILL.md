---
name: conversion-intent-gap
description: Check ONE landing page's gap between the arriving visitor's intent altitude and the page's actual organization altitude. For new-page / iterating phase, where you're examining whether one page aligns with who lands on it. For mature multi-page sites (drift), use conversion-intent-drift-audit instead.
---

# Check the conversion intent gap

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a Conversion Lens.md`. Assumes the altitude is named (see `landing-altitude-name` skill).

## Procedure

1. **Name who lands here and why.** Traffic source (ad, organic search, comparison page, word of mouth, brand), awareness level (problem-aware, solution-aware, product-aware), and the question already in their head when they arrive. If several plausible visitors, name them all and say which one the page serves by default.
2. **Name the intent altitude.** Given that visitor, what altitude does their intent sit at — do they need their *outcome* named, are they ready to *act*, do they need *identity* first? Outcome, not feature. List sub-intents in rough likelihood order if more than one.
3. **Get the current altitude** (from `landing-altitude-name`).
4. **Calculate the gap.** In one sentence: "organized at *X* altitude when the arriving visitor's intent sits at *Y*."
5. **Name the leak.** What does the visitor have to do, or supply themselves, to bridge the gap the page left open? That bridging work is the friction; that friction is the drop-off. Be concrete — "the visitor must translate 'real-time sync engine' into 'my team stops losing edits' on their own."

If the gap is zero, say so plainly. A page already organized at the visitor's altitude is a valid finding and does not need a rewrite.

## Output

```
Who lands:        <visitor — source, awareness level, the question in their head>
Intent altitude:  <feature | action | outcome | identity — what the visitor needs the page organized around>
Current altitude: <from landing-altitude-name>

Gap:        "organized at <X> altitude when the arriving visitor's intent sits at <Y>."
Leak:       <what the visitor must translate / supply / push through — concrete, the drop-off cause>
```

Do not propose how to close the gap or write replacement copy. That is a separate act; this skill only *names* the gap and the leak it opens.
