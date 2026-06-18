# design-craft-skills

Two **generative** design-craft skills for building and polishing real
interfaces. Unlike the diagnostic plugins in this marketplace, these don't
just critique — they design and refine the interface with you.

## Skills

| Skill | Owns | Reference files |
|---|---|---|
| `ui-designer` | visual craft — spacing, color, typography, design tokens, component systems, dark mode, responsive layout, pixel-perfect polish | `design-tokens.md`, `component-library.md`, `polish-and-craft.md` |
| `ux-designer` | experience strategy — user flows, information architecture, interaction design, usability, and the psychology behind the decisions | `psychology-deep-dive.md`, `patterns-and-flows.md` |

Each auto-routes on its own triggers (e.g. *"make it look good"*, *"improve
the spacing"*, *"how should this flow"*, *"reduce the drop-off"*). The two
hand off to each other: `ux-designer` designs the flow, then `ui-designer`
gives it visual polish. Interface text (microcopy) is treated as a separate
copywriting pass — these skills don't write the words.

## Progressive disclosure

Each `SKILL.md` stays lean and pulls in its deeper material on demand from a
`references/` directory (linked with relative paths), so the always-loaded
surface is small while the craft detail is one hop away when needed.

## Layout

```
.claude-plugin/plugin.json
skills/
  ui-designer/
    SKILL.md
    references/
      design-tokens.md
      component-library.md
      polish-and-craft.md
  ux-designer/
    SKILL.md
    references/
      psychology-deep-dive.md
      patterns-and-flows.md
README.md
```

## Pairs with

`design-loop-methodology` critiques design surfaces **read-only** through
conceptual lenses. This plugin is the generative counterpart — build and
polish here, critique there.

## Install

```
/plugin install design-craft-skills@claude-marketplace
```

## License

MIT.
