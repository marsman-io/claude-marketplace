Constraint-based design is a way to build interfaces by describing **relationships** instead of fixed positions.

In UI terms, instead of saying:

```css
.card {
  left: 24px;
  top: 80px;
  width: 320px;
}
```

you define rules like:

```txt
card.left = container.left + 24
card.right = container.right - 24
card.top = header.bottom + 16
card.height >= 120
button.baseline = label.baseline
```

The layout engine solves those relationships and produces the final frame.

## Core idea

A design is modeled as a set of constraints:

```txt
A is 16px below B
A is centered in parent
A must be at least 200px wide
A should align with B unless space is tight
A’s width equals 40% of the container
```

The system then figures out the geometry that satisfies those rules.

## Where it shows up

Common examples:

```swift
// iOS Auto Layout
button.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16)
button.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16)
button.topAnchor.constraint(equalTo: label.bottomAnchor, constant: 12)
```

```css
/* CSS has constraint-like systems */
.card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 16px;
}
```

```css
/* Intrinsic constraints */
.title {
  min-width: 0;
  max-width: 60ch;
}
```

```css
/* Relationship constraints */
.sidebar {
  width: clamp(240px, 25vw, 360px);
}
```

## Why it matters

Constraint-based design is useful because fixed layouts break easily. Constraints let a UI adapt to:

```txt
different screen sizes
dynamic content
localization
accessibility text scaling
responsive layouts
unknown image sizes
conditional UI states
```

Instead of designing one static arrangement, you define the rules that make the layout valid.

## Important concepts

### Hard vs soft constraints

A hard constraint must be satisfied:

```txt
modal.left >= viewport.left + 16
modal.right <= viewport.right - 16
```

A soft constraint is preferred but negotiable:

```txt
title should stay on one line
button should remain 120px wide
image should keep 16:9 ratio
```

When space is limited, the solver decides which soft constraints to relax.

### Intrinsic size

Some elements have natural sizes:

```txt
text wants to be as wide as its content
images may want to preserve aspect ratio
buttons want padding around their label
```

Good constraint systems combine external rules with intrinsic content size.

### Priorities

Some constraints matter more than others:

```txt
avatar must remain 40x40
label should avoid wrapping
container must not overflow
secondary text may truncate first
```

This is especially central in iOS Auto Layout, but the idea applies broadly.

## Frontend analogy

On the web, we usually do not call it “constraint solving,” but modern CSS is full of constraint-based thinking:

```css
.component {
  width: min(100%, 72rem);
  margin-inline: auto;
  padding-inline: clamp(1rem, 4vw, 3rem);
}
```

That says:

```txt
Never exceed 72rem
Never overflow parent
Center when there is extra space
Scale padding with viewport, but keep it bounded
```

Another example:

```css
.layout {
  display: grid;
  grid-template-columns: minmax(16rem, 22rem) minmax(0, 1fr);
  gap: clamp(1rem, 2vw, 2rem);
}
```

This is essentially a set of layout constraints:

```txt
sidebar can shrink to 16rem
sidebar can grow to 22rem
main content takes remaining space
gap is responsive within bounds
```

## Constraint-based design vs breakpoint-based design

Breakpoint-based design says:

```txt
At 768px, change the layout.
At 1024px, change it again.
```

Constraint-based design says:

```txt
Let the component respond continuously based on available space.
```

For example:

```css
.grid {
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
}
```

This avoids hardcoding how many columns exist at each breakpoint. The layout emerges from constraints.

## Good mental model

Think less like:

```txt
Where do I put this?
```

Think more like:

```txt
What relationships must always be true?
What can flex?
What can shrink?
What can wrap?
What should preserve its size?
What breaks first when space runs out?
```

## In practice

A constraint-based design system usually defines:

```txt
spacing rules
alignment rules
minimum and maximum sizes
content behavior
overflow behavior
priority rules
component relationships
adaptive layout rules
```

The goal is not just “responsive design.” It is designing components that remain valid under changing conditions.