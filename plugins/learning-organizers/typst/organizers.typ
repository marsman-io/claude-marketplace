// learning-organizers — graphic organizers and learning tools drawn with Typst
// from a YAML or JSON spec (one file per organizer; the spec is the source of
// truth, every picture or PDF is rebuilt from it).
//
//   #import "organizers.typ": organizer
//   #organizer("/abs/path/to/spec.yaml", theme: theme, version: "key")
//
// `theme` is the dictionary that cc-intelligent-ui puts in scope for a live
// ```typst block (fg, muted, border, accent, bg, palette, width, height, …);
// anything missing falls back to `print-theme`. `version` is "key" (the full
// organizer, with marked blanks shown as answers in the accent colour) or
// "learner" (answers replaced by writing space).
//
// Every call also places `metadata((errors, type)) <organizer-check>`, so
// `typst query … "<organizer-check>"` validates a spec without drawing it.

#import "@preview/cetz:0.5.2"
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

// ---------- themes ----------

#let _light = (
  dark: false,
  fg: rgb("#1f2328"), muted: rgb("#59636e"), link: rgb("#0969da"),
  border: rgb("#c8d1da"), accent: rgb("#0969da"), bg: rgb("#ffffff"),
  code-bg: rgb("#f6f8fa"),
  red: rgb("#cf222e"), green: rgb("#1a7f37"), blue: rgb("#0969da"),
  yellow: rgb("#9a6700"), orange: rgb("#bc4c00"), purple: rgb("#8250df"),
  width: 7.3in, height: 9.4in, text-size: 10.5pt,
)
#let print-theme = _light + (
  palette: (_light.blue, _light.orange, _light.green, _light.red, _light.purple, _light.yellow),
)
#let _dark = (
  dark: true,
  fg: rgb("#e6edf3"), muted: rgb("#9198a1"), link: rgb("#4493f8"),
  border: rgb("#3d444d"), accent: rgb("#4493f8"), bg: rgb("#0d1117"),
  code-bg: rgb("#151b23"),
  red: rgb("#ff7b72"), green: rgb("#3fb950"), blue: rgb("#58a6ff"),
  yellow: rgb("#d29922"), orange: rgb("#f0883e"), purple: rgb("#bc8cff"),
  width: 7.3in, height: 9.4in, text-size: 10.5pt,
)
#let dark-theme = _dark + (
  palette: (_dark.blue, _dark.orange, _dark.green, _dark.red, _dark.purple, _dark.yellow),
)

// ---------- the catalogue ----------

// type → (keys that must be present, default page orientation, one line)
#let catalogue = (
  "t-chart": (req: ("left", "right"), wide: false,
    about: "Two facets of one topic side by side: pros/cons, before/after, A vs B."),
  "attribute-matrix": (req: ("options", "criteria"), wide: true,
    about: "Several options compared on shared criteria, with optional weights and scores."),
  "flow-chart": (req: ("steps",), wide: false,
    about: "Sequential steps of a process with decision points and branches."),
  "mind-map": (req: ("center", "branches"), wide: true,
    about: "A central idea with key-word branches radiating out."),
  "concept-map": (req: ("concepts", "links"), wide: true,
    about: "Concepts in a hierarchy joined by labelled linking phrases."),
  "kwl-chart": (req: (), wide: false,
    about: "Know / Want to know / Learned (optionally How) columns."),
  "anticipation-guide": (req: ("statements",), wide: false,
    about: "Statements marked agree/disagree before and after the lesson, with evidence."),
  "action-plan": (req: (), wide: true,
    about: "A goal broken into tasks with owner, deadline, resources and a measure."),
  "structured-notes": (req: ("sections",), wide: false,
    about: "Guided notes: questions with lines, fill-in blanks, partial lists, group notes."),
  "assessment-checklist": (req: ("criteria",), wide: false,
    about: "Observable criteria with Yes/No marks and space for comments."),
  "rubric": (req: ("levels", "criteria"), wide: true,
    about: "Criteria × performance levels with explicit descriptors and points."),
  "self-questioning": (req: (), wide: false,
    about: "Before / during / after question stems with answer space."),
  "handout": (req: ("items",), wide: false,
    about: "Several organizers in sequence, one lesson's set (one page each in a PDF)."),
)

// ---------- small helpers ----------

#let s(x) = {
  if x == none { "" }
  else if type(x) == str { x }
  else if type(x) == int or type(x) == float { str(x) }
  else if type(x) == bool { if x { "true" } else { "false" } }
  else { repr(x) }
}

// An entry is a string or a mapping with `text` (and maybe `blank: true`).
#let as-item(x) = {
  if x == none { none }
  else if type(x) == dictionary { (blank: false) + x + (text: s(x.at("text", default: ""))) }
  else { (text: s(x), blank: false) }
}

#let as-array(x) = if x == none { () } else if type(x) == array { x } else { (x,) }

#let has-marked(x) = {
  if type(x) == dictionary {
    x.at("blank", default: false) == true or x.values().any(has-marked)
  } else if type(x) == array { x.any(has-marked) } else { false }
}

#let hidden(ctx, it) = {
  ctx.learner and it != none and (
    ctx.blanks == "all" or (ctx.blanks == "marked" and it.at("blank", default: false) == true))
}

// The answer text: a marked blank shows in the accent colour in the key.
// Each drawn answer leaves `metadata((text, blank)) <organizer-answer>`, so a
// test can prove what a learner version shows.
#let answer(ctx, it) = {
  if it == none { [] }
  else {
    let marked = it.at("blank", default: false) == true
    [#metadata((text: it.text, blank: marked)) <organizer-answer>]
    if marked and not ctx.learner { text(fill: ctx.T.accent, weight: "medium", it.text) } else { it.text }
  }
}

#let line-h = 1.75em
#let rule(T, width: 100%) = box(width: width, height: line-h, stroke: (bottom: 0.5pt + T.muted))
#let rules(T, n) = stack(spacing: 0pt, ..range(calc.max(n, 1)).map(_ => rule(T)))

#let tick-box(T, checked: false) = box(
  width: 0.85em, height: 0.85em, baseline: 0.12em, radius: 1.5pt,
  stroke: 0.7pt + T.fg,
  if checked { align(center + horizon, text(size: 0.75em, weight: "bold", fill: T.green, "✓")) },
)

#let tint(c, pct: 82%) = c.transparentize(pct)

// One list row: a bullet and the text, or writing space for a learner.
#let entry(ctx, it, bullet: "•") = {
  if it == none or hidden(ctx, it) {
    if ctx.learner { rule(ctx.T) } else { [] }
  } else {
    block(above: 0pt, below: 0pt, inset: (y: 3pt), width: 100%,
      grid(columns: (auto, 1fr), column-gutter: 5pt, text(fill: ctx.T.muted, bullet), answer(ctx, it)))
  }
}

#let entries(ctx, items, rows: 0, bullet: "•") = {
  let items = as-array(items).map(as-item)
  let n = if ctx.learner { calc.max(rows, items.len()) } else { items.len() }
  stack(spacing: 2pt, ..range(n).map(i => entry(ctx, items.at(i, default: none), bullet: bullet)))
}

// Text with [[answer]] spans: the key shows the answer, a learner gets a blank
// as wide as the answer (at least 4em).
#let fill-in(ctx, str-text) = {
  let parts = s(str-text).split(regex("\[\[|\]\]"))
  for (i, p) in parts.enumerate() {
    if calc.odd(i) {
      if ctx.learner {
        box(width: calc.max(p.len(), 6) * 0.55em, height: 1.1em, baseline: 0.25em,
          stroke: (bottom: 0.6pt + ctx.T.fg))
      } else {
        [#metadata((text: p, blank: true)) <organizer-answer>]
        underline(offset: 2pt, stroke: 0.6pt + ctx.T.accent, text(fill: ctx.T.accent, weight: "medium", p))
      }
    } else { p }
  }
}

// Scale a wide (or tall) drawing down to the room it has; never up.
#let fit(T, body, height: false) = context {
  let size = measure(body)
  let r = 1.0
  if size.width > T.width { r = T.width / size.width }
  if height and size.height * r > T.height { r = T.height / size.height }
  if r < 1.0 { scale(r * 100%, reflow: true, body) } else { body }
}

#let otable(T, columns: (), header: (), ..cells) = table(
  columns: columns,
  stroke: 0.6pt + T.border,
  inset: (x: 7pt, y: 6pt),
  fill: (x, y) => if y == 0 { tint(T.accent, pct: 86%) },
  align: left + top,
  table.header(..header.map(h => text(weight: "bold", h))),
  ..cells,
)

#let titled(spec, ctx, body) = {
  let T = ctx.T
  let t = spec.at("title", default: none)
  let sub = spec.at("instructions", default: none)
  let src = spec.at("source", default: none)
  block(width: 100%, breakable: true, {
    if t != none { block(below: 0.45em, text(size: 1.3em, weight: "bold", s(t))) }
    if sub != none { block(below: 0.9em, text(fill: T.muted, s(sub))) }
    body
    if src != none { block(above: 0.7em, text(size: 0.82em, fill: T.muted, [Source: #s(src)])) }
  })
}

// ---------- layered layout (flow charts, concept maps) ----------
// Nodes 0..n-1; edges (from, to). An edge to an earlier or the same node is a
// back edge (a loop) and does not set a rank. Ranks are longest paths over the
// forward edges; x spreads each node's tree children around it.
#let layered(n, edges, given: none) = {
  let rank = range(n).map(_ => 0)
  for i in range(n) {
    if given != none and given.at(i) != none { rank.at(i) = given.at(i) }
  }
  for i in range(n) {
    for e in edges.filter(e => e.from == i and e.to > i) {
      if given == none or given.at(e.to) == none {
        rank.at(e.to) = calc.max(rank.at(e.to), rank.at(i) + 1)
      }
    }
  }
  // a node sits under its nearest forward predecessor (the highest rank)
  let parent = range(n).map(_ => -1)
  for e in edges {
    if e.to > e.from and rank.at(e.from) < rank.at(e.to) {
      let p = parent.at(e.to)
      if p < 0 or rank.at(e.from) > rank.at(p) { parent.at(e.to) = e.from }
    }
  }
  let x = range(n).map(_ => 0.0)
  for r in range(calc.max(..rank, 0) + 1) {
    let members = range(n).filter(i => rank.at(i) == r)
    if members.len() == 0 { continue }
    let desired = members.map(i => {
      let p = parent.at(i)
      if p < 0 { 0.0 } else {
        let kids = edges.filter(e => e.from == p and parent.at(e.to) == p).map(e => e.to).dedup()
        let j = kids.position(k => k == i)
        x.at(p) + (j - (kids.len() - 1) / 2)
      }
    })
    let order = range(members.len()).sorted(key: k => desired.at(k))
    let placed = ()
    for k in order {
      let want = desired.at(k)
      if placed.len() > 0 { want = calc.max(want, placed.last() + 1) }
      placed.push(want)
    }
    let shift = (desired.sum() - placed.sum()) / members.len()
    for (m, k) in order.enumerate() { x.at(members.at(k)) = placed.at(m) + shift }
  }
  // fletcher stretches fractional cells, so snap to a doubled integer grid
  // (neighbours two columns apart, an empty column between them)
  for r in range(calc.max(..rank, 0) + 1) {
    let members = range(n).filter(i => rank.at(i) == r).sorted(key: i => x.at(i))
    let last = none
    for i in members {
      let v = int(calc.round(x.at(i) * 2))
      if last != none and v < last + 2 { v = last + 2 }
      x.at(i) = v
      last = v
    }
  }
  (rank: rank, x: x)
}

// ---------- geometry: what a graph actually drew ----------
// Concept maps, flow charts and mind maps leave `metadata(…)
// <organizer-geometry>` records of what they drew: the two corners of every
// node and label box, measured where they land on the page
// (`here().position()`, in pt, y down, so fletcher's grid, CeTZ's anchors and
// `fit`'s scaling are all in them); every edge as points sampled along the
// curve it was drawn as, in canvas units (`pts`); and three `frame` marks per
// graph, the canvas points (0, 0), (unit, 0) and (0, unit) as measured on the
// page, which map those points into the same frame. `key` names the element
// within its graph (`graph` counts graphs in the document). An edge's `ends`
// are its two node keys, a label's is its edge's key; a node's `shape` says
// whether its outline is the box or the diamond inscribed in it. organizer.py
// assembles and checks them (`check`; tests/selftest.py).
#let _graph = counter("organizer-graph")

#let _geo(key, kind, id, part, ends: none, shape: "box", pts: none, unit: none) = context {
  let p = here().position()
  [#metadata((graph: _graph.get().first(), key: key, kind: kind, id: id, part: part, ends: ends,
    shape: shape, pts: pts, unit: unit, page: p.page, x: p.x.pt(), y: p.y.pt())) <organizer-geometry>]
}

// A zero-size mark for CeTZ `content` at a canvas point.
#let _geo-pt(..args) = box(width: 0pt, height: 0pt, _geo(..args))

// The frame marks of a CeTZ canvas whose coordinates are numbers of `unit`.
#let _geo-frame(content, unit) = {
  let zero = if type(unit) == length { 0pt } else { 0 }
  for (part, pt) in (("o", (zero, zero)), ("x", (unit, zero)), ("y", (zero, unit))) {
    content(pt, _geo-pt("frame", "frame", "frame", part, unit: if type(unit) == length { unit.pt() } else { unit }))
  }
}

// The box `body` occupies, by its top-left and bottom-right corners.
#let _tracked(key, kind, id, body, ends: none) = box({
  place(top + left, _geo(key, kind, id, "tl", ends: ends))
  place(bottom + right, _geo(key, kind, id, "br", ends: ends))
  body
})

// Samples of a drawn fletcher edge: a straight line's two ends, a polyline's
// corners rounded as fletcher rounds them (draw-edge-polyline), an arc's
// points every few degrees.
#let _edge-samples(edge, kind, verts) = {
  if kind == "poly" and edge.corner-radius != none {
    let θs = range(verts.len() - 1).map(i => fletcher.utils.angle-between(verts.at(i), verts.at(i + 1)))
    let pts = (verts.first(),)
    for i in range(1, verts.len() - 1) {
      let Δθ = fletcher.utils.wrap-angle-180(θs.at(i) - θs.at(i - 1))
      let dir = if Δθ > 0deg { 1 } else { -1 }
      let r = edge.corner-radius * (1 + calc.cos(Δθ))
      if edge.extrude != () { r += if dir > 0 { calc.max(..edge.extrude) } else { -calc.min(..edge.extrude) } }
      r *= dir
      if calc.abs(Δθ) > 179deg or calc.abs(Δθ) <= 1deg { pts.push(verts.at(i)); continue }
      let c = fletcher.cetz.vector.add(verts.at(i), fletcher.utils.vector-polar(r / calc.cos(Δθ / 2), θs.at(i - 1) + Δθ / 2 + 90deg))
      let n = 12
      for j in range(n + 1) {
        pts.push(fletcher.cetz.vector.add(c, fletcher.utils.vector-polar(r, θs.at(i - 1) - 90deg + Δθ * j / n)))
      }
    }
    pts + (verts.last(),)
  } else if kind == "arc" {
    let (from, to) = verts
    let (center, radius, start, stop) = fletcher.utils.get-arc-connecting-points(from, to, edge.bend)
    let n = 48
    range(n + 1).map(j => {
      let a = start + (stop - start) * j / n
      (center.at(0) + radius * calc.cos(a), center.at(1) + radius * calc.sin(a))
    })
  } else { verts }
}

// ---------- settling a graph's layout ----------
// Run inside fletcher's `render`, on its resolved coordinates (pt, CeTZ's y
// up), before anything is drawn: give every bent edge (a cross-link, a back
// edge, a straight edge that would run through a node) the first bend that
// clears the nodes between its ends, then put every label at the first place
// along its edge (position × side) that is clear of the nodes, the labels
// already placed and the other edges. When something stays blocked, or a
// straight edge could only clear the nodes by bending, the ranks move apart in
// steps and both choices run again; the first clean step wins, else the one
// with the fewest collisions, then the fewest bent straight edges. This models
// fletcher's own drawing (anchors, defocus, arcs, label anchors); the measured
// geometry (`<organizer-geometry>`) is what checks the result.

#let _clearance = 3.0 // pt kept free around boxes and edges while settling (the check's tolerance is 1pt)
#let _rank-step = 12.0 // pt added between neighbouring ranks per widening step
#let _rank-steps = 8

#let _xy(v) = (v.at(0).pt(), v.at(1).pt())
#let _ang(a, b) = calc.atan2(b.at(0) - a.at(0), b.at(1) - a.at(1))
#let _at(p, θ, r) = (p.at(0) + r * calc.cos(θ), p.at(1) + r * calc.sin(θ))

// A node's outline as a convex polygon (fletcher's shapes with their defaults).
#let _outline(node) = {
  let (cx, cy) = _xy(node.pos.xyz)
  let (w, h) = node.size.map(v => v.pt() / 2)
  if node.shape == fletcher.shapes.diamond {
    ((cx - 1.5 * w, cy), (cx, cy - 1.5 * h), (cx + 1.5 * w, cy), (cx, cy + 1.5 * h))
  } else if node.shape == fletcher.shapes.parallelogram {
    let d = h * calc.tan(20deg)
    let x = w + d * 0.8
    ((cx - x, cy - h), (cx + x - d, cy - h), (cx + x, cy + h), (cx - x + d, cy + h))
  } else { ((cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h)) }
}

#let _bbox(p) = {
  let xs = p.map(q => q.at(0))
  let ys = p.map(q => q.at(1))
  (calc.min(..xs), calc.min(..ys), calc.max(..xs), calc.max(..ys))
}

// Separating axes, as in organizer.py: convex shapes `a` and `b` (a segment
// is one) come closer than `m` along every edge normal of either.
#let _hit(a, b, m) = {
  let (ax0, ay0, ax1, ay1) = _bbox(a)
  let (bx0, by0, bx1, by1) = _bbox(b)
  if ax0 - bx1 >= m or bx0 - ax1 >= m or ay0 - by1 >= m or by0 - ay1 >= m { return false }
  for poly in (a, b) {
    let n = poly.len()
    for i in range(n) {
      let (px, py) = poly.at(i)
      let (qx, qy) = poly.at(calc.rem(i + 1, n))
      let (nx, ny) = (qy - py, px - qx)
      let len = calc.sqrt(nx * nx + ny * ny)
      if len == 0 { continue }
      let pa = a.map(((x, y)) => (x * nx + y * ny) / len)
      let pb = b.map(((x, y)) => (x * nx + y * ny) / len)
      if calc.min(calc.max(..pa) - calc.min(..pb), calc.max(..pb) - calc.min(..pa)) <= -m { return false }
    }
  }
  true
}

#let _path-hit(path, poly, m) = range(path.len() - 1).any(i => _hit((path.at(i), path.at(i + 1)), poly, m))

// Where a ray from `p` (inside the convex `poly`) at angle θ leaves it.
#let _exit(p, θ, poly) = {
  let (dx, dy) = (calc.cos(θ), calc.sin(θ))
  let best = none
  let n = poly.len()
  for i in range(n) {
    let (ax, ay) = poly.at(i)
    let (bx, by) = poly.at(calc.rem(i + 1, n))
    let (ex, ey) = (bx - ax, by - ay)
    let den = dx * ey - dy * ex
    if calc.abs(den) < 1e-9 { continue }
    let (wx, wy) = (ax - p.at(0), ay - p.at(1))
    let t = (wx * ey - wy * ex) / den
    let u = (wx * dy - wy * dx) / den
    if t > 1e-6 and u >= -1e-9 and u <= 1 + 1e-9 and (best == none or t < best) { best = t }
  }
  if best == none { p } else { _at(p, θ, best) }
}

// fletcher's arc through two points (utils.get-arc-connecting-points), in floats.
#let _arc(a, b, β) = {
  let (dx, dy) = (b.at(0) - a.at(0), b.at(1) - a.at(1))
  let k = 0.5 / calc.tan(β)
  let c = ((a.at(0) + b.at(0)) / 2 + dy * k, (a.at(1) + b.at(1)) / 2 - dx * k)
  let r = calc.sqrt(calc.pow(b.at(0) - c.at(0), 2) + calc.pow(b.at(1) - c.at(1), 2))
  let (start, stop) = (_ang(c, a), _ang(c, b))
  if start < stop and β > 0deg { start += 360deg }
  if start > stop and β < 0deg { start -= 360deg }
  (c: c, r: r, start: start, stop: stop)
}

// The path fletcher draws for an edge (kind, bend, its two nodes), as a polyline.
#let _model-path(e, n0, n1) = {
  let vs = e.final-vertices.map(_xy)
  let (p0, p1) = (_outline(n0), _outline(n1))
  if e.kind == "arc" {
    let θ = _ang(vs.first(), vs.last())
    let a = _exit(vs.first(), θ + e.bend, p0)
    let b = _exit(vs.last(), θ - e.bend + 180deg, p1)
    let A = _arc(a, b, e.bend)
    range(17).map(j => _at(A.c, A.start + (A.stop - A.start) * j / 16, A.r))
  } else if e.kind == "poly" {
    let a = _exit(vs.at(0), _ang(vs.at(0), vs.at(1)), p0)
    let b = _exit(vs.last(), _ang(vs.last(), vs.at(-2)), p1)
    (a,) + vs.slice(1, -1) + (b,)
  } else {
    let θ = _ang(vs.first(), vs.last())
    let f = fletcher.cetz.vector.add(e.final-vertices.first(), fletcher.defocus-adjustment(n0, θ)).map(v => v.pt())
    let g = fletcher.cetz.vector.add(e.final-vertices.last(), fletcher.defocus-adjustment(n1, θ + 180deg)).map(v => v.pt())
    (_exit(f, _ang(f, g), p0), _exit(g, _ang(g, f), p1))
  }
}

#let _compass = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))

// The box fletcher draws a label in (place-edge-label-on-curve), as a polygon.
#let _label-box(e, path, pos, side, size, sep) = {
  let (seg, t) = pos
  let (c, θ) = if e.kind == "arc" {
    let A = _arc(path.first(), path.last(), e.bend)
    let a = A.start + (A.stop - A.start) * t
    (_at(A.c, a, A.r), a + if A.stop > A.start { 90deg } else { -90deg })
  } else {
    let (a, b) = (path.at(seg), path.at(seg + 1))
    ((a.at(0) + (b.at(0) - a.at(0)) * t, a.at(1) + (b.at(1) - a.at(1)) * t), _ang(a, b))
  }
  θ = (θ / 360deg - calc.round(θ / 360deg)) * 360deg
  let side = if side != auto { side } else if e.kind == "arc" { if e.bend > 0deg { left } else { right } }
    else if calc.abs(θ) < 90deg { left } else { right }
  let (w, h) = size
  let mid = if side == center { c } else {
    let θn = θ + if side == right { 90deg } else { -90deg }
    let q = _at(c, θn, -sep)
    let (ox, oy) = _compass.at(int(calc.round(calc.rem(8 * θn / 360deg, 8))))
    (q.at(0) - ox * w / 2, q.at(1) - oy * h / 2)
  }
  let (x, y) = mid
  ((x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2))
}

// Settle `nodes` and `edges` (fletcher's resolved dictionaries); `rank` maps a
// node name to its rank, `axis` is the rank direction (0 x, 1 y).
#let _settle(nodes, edges, rank, axis) = {
  let at = (:)
  for (i, n) in nodes.enumerate() { at.insert(str(n.name), i) }
  let ends = edges.map(e => (e.vertices.first(), e.vertices.last()).map(v =>
    if type(v) == label { at.at(str(v), default: none) }))
  let sizes = edges.map(e => if e.label != none {
    let m = measure(box({ set text(e.label-size); (e.label-wrapper)(e) }))
    (m.width.pt(), m.height.pt())
  })
  // rank centres along the rank axis, in drawing order
  let centre = (:)
  for n in nodes {
    let r = rank.at(str(n.name), default: none)
    if r != none { centre.insert(str(r), _xy(n.pos.xyz).at(axis)) }
  }
  let order = centre.keys().map(int).sorted().map(r => centre.at(str(r)))
  let dir = if order.len() > 1 and order.at(1) < order.at(0) { -1 } else { 1 }
  let moved(v, extra) = {
    if order.len() < 2 { return v }
    let k = range(order.len()).sorted(key: k => calc.abs(order.at(k) - v.at(axis).pt())).first()
    let v = v
    v.at(axis) += dir * extra * k * 1pt
    v
  }
  let best = none
  for step in range(_rank-steps + 1) {
    let extra = step * _rank-step
    let ns = nodes.map(n => { n.pos.xyz = moved(n.pos.xyz, extra); n })
    let polys = ns.map(_outline)
    let es = edges.map(e => { e.final-vertices = e.final-vertices.map(v => moved(v, extra)); e })
    let cost = 0
    let bent = 0
    let paths = ()
    for (k, e) in es.enumerate() {
      let (i, j) = ends.at(k)
      if i == none or j == none or i == j { paths.push(e.final-vertices.map(_xy)); continue }
      let others = range(ns.len()).filter(x => x != i and x != j)
      let blocked(p) = others.filter(x => _path-hit(p, polys.at(x), _clearance)).len()
      let p = _model-path(e, ns.at(i), ns.at(j))
      let c = blocked(p)
      if e.kind == "arc" or (e.kind == "line" and c > 0) {
        let b0 = if e.kind == "arc" { e.bend } else { 0deg }
        let tries = (b0, -b0) + (35, -35, 20, -20, 50, -50, 65, -65, 80, -80, 0).map(d => d * 1deg)
        let found = none
        for β in tries.dedup() {
          let e2 = e + (kind: if β == 0deg { "line" } else { "arc" }, bend: β)
          let p2 = _model-path(e2, ns.at(i), ns.at(j))
          let c2 = blocked(p2)
          if found == none or c2 < found.at(2) { found = (e2, p2, c2) }
          if c2 == 0 { break }
        }
        if e.kind == "line" and found.at(0).kind == "arc" { bent += 1 }
        (e, p, c) = found
        es.at(k) = e
      }
      paths.push(p)
      cost += c
    }
    let placed = ()
    for (k, e) in es.enumerate() {
      let (i, j) = ends.at(k)
      if e.label == none or i == none or j == none { continue }
      let path = paths.at(k)
      let segs = path.len() - 1
      let sep = e.label-sep.pt()
      let own = (e.label-pos.segment, fletcher.utils.relative-to-float(e.label-pos.position))
      let cands = ((own, e.label-side),)
      let ts = (0.5, 0.35, 0.65, 0.25, 0.75, 0.2, 0.8, 0.15, 0.85)
      let segments = if e.kind == "poly" { (own.at(0),) + range(segs).filter(s => s != own.at(0)) } else { (0,) }
      for s in segments {
        for t in ts {
          for side in (e.label-side, center, left, right).dedup() {
            cands.push(((s, t), side))
          }
        }
      }
      let score(box) = (polys.filter(q => _hit(box, q, _clearance)).len()
        + placed.filter(q => _hit(box, q, _clearance)).len()
        + range(paths.len()).filter(x => x != k and _path-hit(paths.at(x), box, _clearance)).len())
      let found = none
      for (pos, side) in cands {
        let box = _label-box(e, path, pos, side, sizes.at(k), if side == center { 0 } else { sep })
        let c = score(box)
        if found == none or c < found.at(2) { found = (pos, side, c, box) }
        if c == 0 { break }
      }
      let (pos, side, c, box) = found
      placed.push(box)
      cost += c
      es.at(k) = e + (label-pos: (segment: pos.at(0), position: pos.at(1) * 100%), label-side: side,
        label-anchor: if side == center { "center" } else { e.label-anchor },
        label-sep: if side == center { 0pt } else { e.label-sep })
    }
    if best == none or (cost, bent) < best.at(2) { best = (ns, es, (cost, bent)) }
    if cost == 0 and bent == 0 { break }
  }
  (best.at(0), best.at(1))
}

// fletcher's `render`: settle the layout (above), then draw it with fletcher's
// own draw-anchored-* steps plus geometry marks: each node outline's bounding
// box from CeTZ anchors, and each edge sampled between the anchors it was
// drawn to. `nkeys` maps a node name to (key, id, rank); `ekeys` lists (key,
// id, from, to) in edge order; `axis` is the rank direction (0 x, 1 y).
#let _geo-render(nkeys, ekeys, axis: 1) = (grid, nodes, edges, options) => {
  let (nodes, edges) = _settle(nodes, edges, nkeys.pairs().map(((k, v)) => (k, v.at(2))).to-dict(), axis)
  fletcher.cetz.canvas({
  import fletcher.cetz.draw: *
  let ok = edges.len() == ekeys.len()
  for (k, edge) in edges.enumerate() {
    let ns = fletcher.find-nodes-for-edge(grid, nodes, edge)
    let mark(verts) = if ok {
      let (key, id, a, b) = ekeys.at(k)
      let pts = _edge-samples(edge, edge.kind, verts).map(q => q.map(v => v.pt()))
      content(verts.first(), _geo-pt(key, "edge", id, "path", ends: (a, b), pts: pts))
    }
    let outlines(i, ray) = { group(ns.at(i).map(fletcher.draw-node-outline).join()); ray }
    let obj = if edge.kind == "line" {
      let (from, to) = edge.final-vertices
      let θ = fletcher.utils.angle-between(from, to) + 90deg
      if ns.at(0).len() == 1 { from = fletcher.cetz.vector.add(from, fletcher.defocus-adjustment(ns.at(0).at(0), θ - 90deg)) }
      if ns.at(1).len() == 1 { to = fletcher.cetz.vector.add(to, fletcher.defocus-adjustment(ns.at(1).at(0), θ + 90deg)) }
      let dummy = line(from, to)
      fletcher.find-anchor-pair((outlines(0, dummy), outlines(1, dummy)), (from, to), anchors => {
        (edge.post)(fletcher.draw-edge-line(edge + (final-vertices: anchors)))
        mark(anchors)
      })
    } else if edge.kind == "arc" {
      let (from, to) = edge.final-vertices
      let θ = fletcher.utils.angle-between(from, to)
      let rays = ((from, θ + edge.bend), (to, θ - edge.bend + 180deg)).map(((p, φ)) =>
        line(p, fletcher.cetz.vector.add(p, fletcher.utils.vector-polar(10cm, φ))))
      fletcher.find-anchor-pair((outlines(0, rays.at(0)), outlines(1, rays.at(1))), (from, to), anchors => {
        (edge.post)(fletcher.draw-edge-arc(edge + (final-vertices: anchors)))
        mark(anchors)
      })
    } else {
      let vs = edge.final-vertices
      let ends = (line(..vs.slice(0, 2)), line(..vs.slice(-2)))
      fletcher.find-anchor-pair((outlines(0, ends.at(0)), outlines(1, ends.at(1))), (vs.first(), vs.last()), anchors => {
        let e = edge
        e.final-vertices.at(0) = anchors.at(0)
        e.final-vertices.at(-1) = anchors.at(1)
        (edge.post)(fletcher.draw-edge-polyline(e))
        mark(e.final-vertices)
      })
    }
    if edge.layer != 0 { on-layer(edge.layer, obj) } else { obj }
  }
  _geo-frame(content, 100pt)
  for (i, node) in nodes.enumerate() {
    fletcher.draw-node(node)
    let nk = nkeys.at(str(node.name), default: none)
    if nk != none {
      let g = "_geo-node-" + str(i)
      hide(group(name: g, { translate(node.pos.xyz); (node.shape)(node, node.outset) }))
      let shape = if node.shape == fletcher.shapes.diamond { "diamond" } else { "box" }
      content(g + ".north-west", _geo-pt(nk.at(0), "node", nk.at(1), "tl", shape: shape))
      content(g + ".south-east", _geo-pt(nk.at(0), "node", nk.at(1), "br", shape: shape))
    }
  }
  })
}

// ---------- validation ----------

#let _ids(list, what) = {
  let errs = ()
  let seen = ()
  for (i, it) in as-array(list).enumerate() {
    if type(it) != dictionary or "id" not in it {
      errs.push(what + " " + str(i + 1) + " has no `id`")
    } else if s(it.id) in seen {
      errs.push(what + " id `" + s(it.id) + "` is used twice")
    } else { seen.push(s(it.id)) }
  }
  (errs: errs, ids: seen)
}

// A key with no value is nearly always unquoted text split by YAML: in
// `{label: if not possible, try}` the comma makes `try` a second, empty key.
#let _empty-keys(x) = {
  if type(x) == dictionary {
    x.pairs().map(((k, v)) => if v == none { (k,) } else { _empty-keys(v) }).flatten()
  } else if type(x) == array { x.map(_empty-keys).flatten() } else { () }
}

#let validate(spec) = {
  if type(spec) != dictionary { return ("the spec must be a mapping (key: value) at the top level",) }
  let empty = _empty-keys(spec).dedup()
  if empty.len() > 0 {
    return empty.map(k => "`" + k + "` has no value: quote text that contains a comma or a colon (\"if not possible, try\")")
  }
  let t = spec.at("type", default: none)
  let names = catalogue.keys().join(", ")
  if t == none { return ("missing `type` (one of: " + names + ")",) }
  if s(t) not in catalogue { return ("unknown type `" + s(t) + "` (one of: " + names + ")",) }
  let t = s(t)
  let errs = ()
  for k in catalogue.at(t).req {
    if k not in spec { errs.push(t + ": missing `" + k + "`") }
  }
  if errs.len() > 0 { return errs }
  let b = spec.at("blanks", default: none)
  if b != none and s(b) not in ("all", "marked", "none") {
    errs.push("`blanks` must be all, marked or none")
  }
  if t == "flow-chart" {
    let r = _ids(spec.steps, "step")
    errs += r.errs
    for st in as-array(spec.steps).filter(x => type(x) == dictionary) {
      for nx in as-array(st.at("next", default: none)) {
        if s(nx) not in r.ids { errs.push("step `" + s(st.at("id", default: "?")) + "`: next `" + s(nx) + "` is not a step id") }
      }
      for br in as-array(st.at("branches", default: none)) {
        if type(br) != dictionary or "to" not in br {
          errs.push("step `" + s(st.at("id", default: "?")) + "`: every branch needs `to`")
        } else if s(br.to) not in r.ids {
          errs.push("step `" + s(st.at("id", default: "?")) + "`: branch to `" + s(br.to) + "` is not a step id")
        }
      }
      let kind = st.at("kind", default: "step")
      if s(kind) not in ("start", "end", "step", "decision", "io") {
        errs.push("step `" + s(st.at("id", default: "?")) + "`: kind must be start, end, step, decision or io")
      }
    }
  } else if t == "concept-map" {
    let r = _ids(spec.concepts, "concept")
    errs += r.errs
    for (i, l) in as-array(spec.links).enumerate() {
      if type(l) != dictionary or "from" not in l or "to" not in l {
        errs.push("link " + str(i + 1) + " needs `from` and `to`")
      } else {
        for end in (l.from, l.to) {
          if s(end) not in r.ids { errs.push("link " + str(i + 1) + ": `" + s(end) + "` is not a concept id") }
        }
      }
    }
  } else if t == "attribute-matrix" {
    let n = as-array(spec.options).len()
    if n == 0 { errs.push("attribute-matrix: `options` is empty") }
    for c in as-array(spec.criteria) {
      if type(c) != dictionary or "name" not in c { errs.push("every criterion needs `name`"); continue }
      for k in ("values", "scores") {
        let xs = c.at(k, default: none)
        if xs != none and as-array(xs).len() != n {
          errs.push("criterion `" + s(c.name) + "`: " + str(as-array(xs).len()) + " " + k + " for " + str(n) + " options")
        }
      }
      for x in as-array(c.at("scores", default: none)) {
        if x != none and type(x) != int and type(x) != float {
          errs.push("criterion `" + s(c.name) + "`: scores must be numbers (got `" + s(x) + "`)")
        }
      }
      let w = c.at("weight", default: 1)
      if type(w) != int and type(w) != float { errs.push("criterion `" + s(c.name) + "`: weight must be a number") }
    }
  } else if t == "rubric" {
    let n = as-array(spec.levels).len()
    for l in as-array(spec.levels) {
      if type(l) != dictionary or "label" not in l { errs.push("every level needs `label` (and usually `score`)") }
    }
    for c in as-array(spec.criteria) {
      if type(c) != dictionary or "skill" not in c { errs.push("every rubric criterion needs `skill`"); continue }
      let d = as-array(c.at("descriptors", default: ()))
      if d.len() != n {
        errs.push("criterion `" + s(c.skill) + "`: " + str(d.len()) + " descriptors for " + str(n) + " levels")
      }
    }
  } else if t == "structured-notes" {
    for (i, sec) in as-array(spec.sections).enumerate() {
      let k = if type(sec) == dictionary { s(sec.at("kind", default: "lines")) } else { "?" }
      if k not in ("lines", "fill-in", "list", "group", "organizer") {
        errs.push("section " + str(i + 1) + ": kind must be lines, fill-in, list, group or organizer")
      } else if k == "organizer" {
        errs += validate(sec.at("organizer", default: none)).map(e => "section " + str(i + 1) + ": " + e)
      }
    }
  } else if t == "handout" {
    for (i, it) in as-array(spec.items).enumerate() {
      errs += validate(it).map(e => "item " + str(i + 1) + ": " + e)
    }
  } else if t == "mind-map" {
    if as-array(spec.branches).len() == 0 { errs.push("mind-map: `branches` is empty") }
  }
  errs
}

#let error-box(T, errs) = block(
  width: 100%, inset: 10pt, radius: 4pt, stroke: 1pt + T.red, fill: tint(T.red, pct: 90%),
  {
    text(weight: "bold", fill: T.red, "This organizer spec has problems:")
    list(..errs.map(e => text(e)))
  },
)

// ---------- renderers ----------

#let render-t-chart(spec, ctx) = {
  let T = ctx.T
  let sides = (spec.left, spec.right).map(x => if type(x) == dictionary { x } else { (heading: s(x)) })
  let rows = spec.at("rows", default: 6)
  grid(
    columns: (1fr, 1fr),
    stroke: (x, y) => (
      bottom: if y == 0 { 1.6pt + T.fg },
      left: if x == 1 { 1.6pt + T.fg },
    ),
    inset: (x: 10pt, y: 7pt),
    ..sides.map(sd => align(center, text(weight: "bold", size: 1.1em, s(sd.at("heading", default: ""))))),
    ..sides.map(sd => entries(ctx, sd.at("items", default: ()), rows: rows)),
  )
}

#let render-attribute-matrix(spec, ctx) = {
  let T = ctx.T
  let opts = as-array(spec.options).map(s)
  let crit = as-array(spec.criteria)
  let scored = crit.any(c => c.at("scores", default: none) != none)
  let weighted = crit.any(c => c.at("weight", default: none) != none)
  let totals = range(opts.len()).map(j => crit.fold(0, (acc, c) => {
    let x = as-array(c.at("scores", default: ())).at(j, default: none)
    acc + if x == none { 0 } else { c.at("weight", default: 1) * x }
  }))
  let show-best = scored and not ctx.learner and spec.at("highlight-best", default: true)
  let best = if show-best { totals.position(t => t == calc.max(..totals)) } else { none }
  let cells = ()
  for c in crit {
    let w = c.at("weight", default: none)
    cells.push({
      text(weight: "bold", s(c.name))
      if w != none { text(fill: T.muted, size: 0.85em, [ (weight #s(w))]) }
      let d = c.at("note", default: none)
      if d != none { linebreak(); text(fill: T.muted, size: 0.85em, s(d)) }
    })
    let vals = as-array(c.at("values", default: range(opts.len()).map(_ => none)))
    let scs = as-array(c.at("scores", default: none))
    for j in range(opts.len()) {
      let it = as-item(vals.at(j, default: none))
      let sc = scs.at(j, default: none)
      cells.push(table.cell(fill: if j == best { tint(T.green, pct: 90%) }, {
        if it == none or hidden(ctx, it) { if ctx.learner { rules(T, spec.at("lines", default: 2)) } }
        else { answer(ctx, it) }
        if scored {
          v(2pt)
          align(right, if ctx.learner and ctx.blanks != "none" {
            box(width: 2.2em, height: 1.3em, stroke: 0.6pt + T.muted, radius: 2pt)
          } else if sc != none {
            box(inset: (x: 5pt, y: 2pt), radius: 6pt, fill: tint(T.accent, pct: 80%),
              text(size: 0.85em, weight: "bold", s(sc) + if w != none and w != 1 { " × " + s(w) }))
          })
        }
      }))
    }
  }
  if scored {
    cells.push(text(weight: "bold", if weighted { "Weighted total" } else { "Total" }))
    for j in range(opts.len()) {
      cells.push(table.cell(fill: if j == best { tint(T.green, pct: 75%) }, align(right,
        if ctx.learner and ctx.blanks != "none" { box(width: 3em, height: 1.3em, stroke: 0.6pt + T.muted, radius: 2pt) }
        else { text(weight: "bold", size: 1.1em, s(calc.round(totals.at(j), digits: 2))) })))
    }
  }
  let header = (s(spec.at("criteria-heading", default: "Criteria")),) + opts.enumerate().map(((j, o)) =>
    if j == best { [#o #text(fill: T.green, "★")] } else { o })
  otable(T, columns: (auto,) + opts.map(_ => 1fr), header: header, ..cells)
  let scale = spec.at("scale", default: none)
  if scale != none { block(above: 0.5em, text(size: 0.85em, fill: T.muted, [Scale: #s(scale)])) }
}

#let render-flow-chart(spec, ctx) = {
  let T = ctx.T
  let steps = as-array(spec.steps)
  let n = steps.len()
  let idx = (:)
  for (i, st) in steps.enumerate() { idx.insert(s(st.id), i) }
  let edges = ()
  for (i, st) in steps.enumerate() {
    let nx = as-array(st.at("next", default: none))
    let br = as-array(st.at("branches", default: none))
    for t in nx { edges.push((from: i, to: idx.at(s(t)), label: none)) }
    for b in br { edges.push((from: i, to: idx.at(s(b.to)), label: b.at("label", default: none))) }
    if nx.len() == 0 and br.len() == 0 and s(st.at("kind", default: "step")) != "end" and i + 1 < n {
      edges.push((from: i, to: i + 1, label: none))
    }
  }
  let L = layered(n, edges)
  let right = s(spec.at("direction", default: "down")) == "right"
  let w = spec.at("node-width", default: 36) * 1mm
  let nodes = steps.enumerate().map(((i, st)) => {
    let it = as-item(st)
    let kind = s(st.at("kind", default: "step"))
    let col = (start: T.green, end: T.red, decision: T.yellow, io: T.purple, step: T.blue).at(kind)
    let shape = (start: fletcher.shapes.pill, end: fletcher.shapes.pill, decision: fletcher.shapes.diamond,
      io: fletcher.shapes.parallelogram, step: fletcher.shapes.rect).at(kind)
    let hid = hidden(ctx, it)
    let bw = if kind == "decision" { w * 0.78 } else { w }
    let body = if hid { box(width: bw * 0.85, height: 1.6em) } else {
      box(width: bw, align(center, {
        answer(ctx, it)
        let who = st.at("who", default: none)
        if who != none { linebreak(); text(size: 0.8em, fill: T.muted, s(who)) }
      }))
    }
    let pos = if right { (L.rank.at(i), L.x.at(i)) } else { (L.x.at(i), L.rank.at(i)) }
    node(pos, body, name: label("n" + str(i)), shape: shape,
      fill: if hid { none } else { tint(col, pct: 84%) },
      stroke: if hid { (paint: T.muted, thickness: 0.8pt, dash: "dashed") } else { 0.9pt + col })
  })
  let at(c, r) = if right { (r, c) } else { (c, r) }
  let eid(e) = "arrow " + s(steps.at(e.from).id) + "→" + s(steps.at(e.to).id) + if e.label != none { " " + repr(s(e.label)) } else { "" }
  let es = edges.enumerate().map(((k, e)) => {
    let back = e.to <= e.from
    let (r0, r1) = (L.rank.at(e.from), L.rank.at(e.to))
    // an edge that skips ranks goes around the nodes between, on its side
    let between = range(n).filter(i => L.rank.at(i) > r0 and L.rank.at(i) < r1)
    let (x0, x1) = (L.x.at(e.from), L.x.at(e.to))
    let blocked = between.filter(i => L.x.at(i) >= calc.min(x0, x1) - 1 and L.x.at(i) <= calc.max(x0, x1) + 1)
    let via = if not back and blocked.len() > 0 {
      let xs = blocked.map(i => L.x.at(i))
      let left = x0 + x1 <= calc.min(..xs) + calc.max(..xs)
      let side = if left { calc.min(..xs) - 2 } else { calc.max(..xs) + 2 }
      (if side != x0 { (at(side, r0),) } else { () }) + (if side != x1 { (at(side, r1),) } else { () })
    } else { () }
    let args = (label("n" + str(e.from)),) + via + (label("n" + str(e.to)), "-|>")
    if e.label != none { args.push(text(size: 0.82em, s(e.label))) }
    edge(..args, bend: if back { -50deg } else { 0deg }, label-fill: T.bg,
      label-wrapper: w => _tracked("l" + str(k), "label", "label " + repr(s(e.label)) + " on " + s(steps.at(e.from).id) + "→" + s(steps.at(e.to).id),
        box(w.label, inset: .2em, radius: .2em, fill: w.label-fill), ends: "e" + str(k)))
  })
  _graph.step()
  fit(T, height: true, align(center, diagram(
    spacing: if right { (10mm, 4mm) } else { (3mm, 9mm) },
    node-inset: 6pt, node-corner-radius: 3pt,
    edge-stroke: 0.8pt + T.fg, node-stroke: 0.8pt + T.fg,
    render: _geo-render(
      steps.enumerate().map(((i, st)) => ("n" + str(i), ("n" + str(i), "step " + s(st.id), L.rank.at(i)))).to-dict(),
      edges.enumerate().map(((k, e)) => ("e" + str(k), eid(e), "n" + str(e.from), "n" + str(e.to))),
      axis: if right { 0 } else { 1 }),
    ..nodes, ..es,
  )))
}

#let render-concept-map(spec, ctx) = {
  let T = ctx.T
  let cs = as-array(spec.concepts)
  let n = cs.len()
  let idx = (:)
  for (i, c) in cs.enumerate() { idx.insert(s(c.id), i) }
  let links = as-array(spec.links).map(l => (from: idx.at(s(l.from)), to: idx.at(s(l.to)),
    label: l.at("label", default: none), cross: l.at("cross", default: false)))
  let given = cs.map(c => c.at("level", default: none))
  let L = layered(n, links.filter(l => not l.cross), given: if given.any(g => g != none) { given } else { none })
  let w = spec.at("node-width", default: 34) * 1mm
  let nodes = cs.enumerate().map(((i, c)) => {
    let it = as-item(c)
    let hid = hidden(ctx, it)
    let col = T.palette.at(calc.rem(L.rank.at(i), T.palette.len()))
    node((L.x.at(i), L.rank.at(i)),
      if hid { box(width: w * 0.8, height: 1.6em) } else { box(width: w, align(center,
        if L.rank.at(i) == 0 { text(weight: "bold", answer(ctx, it)) } else { answer(ctx, it) })) },
      name: label("c" + str(i)), shape: fletcher.shapes.rect, corner-radius: 5pt,
      fill: if hid { none } else { tint(col, pct: if L.rank.at(i) == 0 { 70% } else { 86% }) },
      stroke: if hid { (paint: T.muted, thickness: 0.8pt, dash: "dashed") } else { 0.9pt + col })
  })
  let lid(l) = "link " + s(cs.at(l.from).id) + "→" + s(cs.at(l.to).id) + {
    let lab = as-item(l.label)
    if lab != none { " " + repr(lab.text) } else { "" }
  }
  let es = links.enumerate().map(((k, l)) => {
    // stagger labels of neighbouring links from one concept so a fan stays legible
    let sib = links.slice(0, k).filter(o => o.from == l.from and not o.cross).len()
    let args = (label("c" + str(l.from)), label("c" + str(l.to)), "-|>")
    let lab = as-item(l.label)
    if lab != none {
      args.push(if hidden(ctx, lab) { box(width: 4em, height: 1em, stroke: (bottom: 0.6pt + T.muted)) }
        else { text(size: 0.82em, style: "italic", answer(ctx, lab)) })
    }
    edge(..args, label-fill: T.bg, label-pos: if l.cross { 0.3 } else if calc.odd(sib) { 0.74 } else { 0.5 }, bend: if l.cross { 35deg } else if l.to <= l.from { -40deg } else { 0deg },
      stroke: if l.cross { (paint: T.muted, thickness: 0.8pt, dash: "dashed") } else { 0.8pt + T.fg },
      label-wrapper: w => _tracked("l" + str(k), "label", "label " + repr(s(lab.text)) + " on " + s(cs.at(l.from).id) + "→" + s(cs.at(l.to).id),
        box(w.label, inset: .2em, radius: .2em, fill: w.label-fill), ends: "e" + str(k)))
  })
  let fq = spec.at("focus-question", default: none)
  if fq != none {
    block(below: 0.8em, inset: 7pt, radius: 3pt, fill: tint(T.accent, pct: 90%),
      [#text(weight: "bold", "Focus question: ")#s(fq)])
  }
  _graph.step()
  fit(T, height: true, align(center, diagram(
    spacing: (4mm, 17mm), node-inset: 6pt, edge-stroke: 0.8pt + T.fg,
    render: _geo-render(
      cs.enumerate().map(((i, c)) => ("c" + str(i), ("c" + str(i), "concept " + s(c.id), L.rank.at(i)))).to-dict(),
      links.enumerate().map(((k, l)) => ("e" + str(k), lid(l), "c" + str(l.from), "c" + str(l.to)))),
    ..nodes, ..es)))
}

// Mind map: two-sided tree around the centre, branch colour from the palette.
// Every node gets a slot at least `row-height` tall and tall enough for its
// box as drawn (a wrapped line makes it taller); a branch spans its own slot
// or its children's, whichever is more, and sits centred on that span.
#let _mm-kids(b) = if type(b) == dictionary { as-array(b.at("children", default: ())) } else { () }
#let _mm-leaves(b) = {
  let k = _mm-kids(b)
  if k.len() == 0 { 1 } else { k.map(_mm-leaves).sum() }
}
#let _mm-span(b, depth, slot) = calc.max(slot(b, depth),
  _mm-kids(b).map(c => _mm-span(c, depth + 1, slot)).sum(default: 0))
#let _mm-place(b, depth, side, y0, color, parent, path, slot) = {
  let span = _mm-span(b, depth, slot)
  let kids = _mm-kids(b)
  let out = ()
  let y = y0 + (span - kids.map(c => _mm-span(c, depth + 1, slot)).sum(default: 0)) / 2
  for (i, c) in kids.enumerate() {
    out += _mm-place(c, depth + 1, side, y, color, path, path + "." + str(i), slot)
    y += _mm-span(c, depth + 1, slot)
  }
  out.push((id: path, depth: depth, side: side, y: y0 + span / 2,
    item: as-item(b), color: color, parent: parent))
  out
}

#let render-mind-map(spec, ctx) = {
  let T = ctx.T
  let br = as-array(spec.branches)
  let total = br.map(_mm-leaves).sum()
  // right side takes branches until it holds half the leaves
  let side-of = ()
  let acc = 0
  for b in br {
    side-of.push(if acc < total / 2 or br.len() == 1 { 1 } else { -1 })
    acc += _mm-leaves(b)
  }
  let cw = 3.8
  let bw = spec.at("node-width", default: 3.4)
  let dx = bw + 0.9
  let h = spec.at("row-height", default: 1.15)
  let gap = 0.3
  let xs(d) = cw / 2 + 0.7 + (d - 1) * dx
  let node-box(item, depth, side, color) = {
    let hid = hidden(ctx, item)
    box(width: bw * 1cm, inset: 5pt, radius: 4pt,
      fill: if hid or depth > 1 { none } else { tint(color, pct: 80%) },
      stroke: if hid { (paint: T.muted, thickness: 0.7pt, dash: "dashed") }
        else if depth == 1 { 0.9pt + color } else { (bottom: 0.9pt + color) },
      align(if side == 1 { left } else { right },
        if hid { box(height: 1.1em) }
        else if depth == 1 { text(weight: "bold", answer(ctx, item)) }
        else { text(size: 0.9em, answer(ctx, item)) }))
  }
  let hub = as-item(spec.center)
  let mid(nd) = "branch " + nd.id + " " + repr(nd.item.text)
  _graph.step()
  context {
    let slot(b, depth) = calc.max(h, measure(node-box(as-item(b), depth, 1, T.fg)).height / 1cm + gap)
    let nodes = ()
    let spans = (:)
    for sd in (1, -1) {
      let y = 0
      for (i, b) in br.enumerate() {
        if side-of.at(i) != sd { continue }
        nodes += _mm-place(b, 1, sd, y, T.palette.at(calc.rem(i, T.palette.len())), "root", "b" + str(i), slot)
        y += _mm-span(b, 1, slot)
      }
      spans.insert(str(sd), y)
    }
    let pos = (:)
    for nd in nodes {
      let L = spans.at(str(nd.side))
      pos.insert(nd.id, (x: nd.side * xs(nd.depth), y: -(nd.y - L / 2), side: nd.side))
    }
    fit(T, height: true, align(center, cetz.canvas(length: 1cm, {
      import cetz.draw: *
      for nd in nodes {
        let p = pos.at(nd.id)
        let from = if nd.parent == "root" { (p.side * cw / 2, 0) } else {
          let q = pos.at(nd.parent)
          (q.x + q.side * bw, q.y)
        }
        let mx = (from.at(0) + p.x) / 2
        let (a, c1, c2, b) = (from, (mx, from.at(1)), (mx, p.y), (p.x, p.y))
        bezier(a, b, c1, c2,
          stroke: (paint: nd.color, thickness: if nd.depth == 1 { 1.6pt } else { 0.9pt }))
        // the cubic's own points, so the samples lie on the drawn curve
        let pts = range(25).map(j => {
          let u = j / 24
          let wts = (calc.pow(1 - u, 3), 3 * calc.pow(1 - u, 2) * u, 3 * (1 - u) * calc.pow(u, 2), calc.pow(u, 3))
          range(2).map(d => (a, c1, c2, b).zip(wts).map(((q, w)) => q.at(d) * w).sum())
        })
        content(a, _geo-pt("e" + nd.id, "edge", "curve " + nd.parent + "→" + nd.id, "path",
          ends: (if nd.parent == "root" { "hub" } else { "m" + nd.parent }, "m" + nd.id), pts: pts))
      }
      _geo-frame(content, 1)
      for nd in nodes {
        let p = pos.at(nd.id)
        content((p.x, p.y), anchor: if p.side == 1 { "west" } else { "east" },
          _tracked("m" + nd.id, "node", mid(nd), node-box(nd.item, nd.depth, p.side, nd.color)))
      }
      content((0, 0), _tracked("hub", "node", "center " + repr(hub.text), box(width: cw * 1cm, inset: 8pt, radius: 8pt, fill: tint(T.accent, pct: 70%),
        stroke: 1.4pt + T.accent, align(center, text(weight: "bold", size: 1.1em, answer(ctx, hub))))))
    })))
  }
}

#let _kwl-cols = (
  know: ("K", "What I Know"),
  want: ("W", "What I Want to Know"),
  learned: ("L", "What I Learned"),
  how: ("H", "How I Will Find Out"),
)

#let render-kwl-chart(spec, ctx) = {
  let T = ctx.T
  let cols = as-array(spec.at("columns", default: ("know", "want", "learned"))).map(s)
  let rows = spec.at("rows", default: 8)
  let topic = spec.at("topic", default: none)
  if topic != none { block(below: 0.6em, [#text(weight: "bold", "Topic: ")#s(topic)]) }
  table(
    columns: cols.map(_ => 1fr),
    stroke: 0.8pt + T.border,
    inset: 8pt,
    fill: (x, y) => if y == 0 { tint(T.palette.at(calc.rem(x, T.palette.len())), pct: 80%) },
    table.header(..cols.map(c => {
      let (letter, lab) = _kwl-cols.at(c, default: (c.first(), c))
      align(center, [#text(size: 1.8em, weight: "bold", letter) \ #text(weight: "bold", lab)])
    })),
    ..cols.map(c => entries(ctx, spec.at(c, default: ()), rows: rows)),
  )
}

#let render-anticipation-guide(spec, ctx) = {
  let T = ctx.T
  let resp = as-array(spec.at("responses", default: ("Agree", "Disagree"))).map(s)
  let choices(mark) = stack(spacing: 4pt, ..resp.map(r => [#tick-box(T, checked: mark == r) #r]))
  let cells = ()
  for (i, st) in as-array(spec.statements).enumerate() {
    let it = as-item(st)
    let ans = if ctx.learner { none } else { s(it.at("answer", default: none)) }
    let ev = as-item(it.at("evidence", default: none))
    cells.push(choices(none))
    cells.push([#text(weight: "bold", str(i + 1) + ". ")#it.text])
    cells.push(choices(ans))
    cells.push(if ev == none or ctx.learner { if ctx.learner { rules(T, spec.at("lines", default: 2)) } }
      else { text(size: 0.9em, answer(ctx, ev)) })
  }
  otable(T, columns: (auto, 2fr, auto, 1.6fr),
    header: ("Before", "Statement", "After", s(spec.at("notes-heading", default: "Evidence and notes"))),
    ..cells)
}

#let render-action-plan(spec, ctx) = {
  let T = ctx.T
  let goal = as-item(spec.at("goal", default: none))
  if goal != none or ctx.learner {
    block(width: 100%, below: 0.8em, inset: (left: 10pt, y: 6pt, right: 6pt),
      stroke: (left: 3pt + T.accent), fill: tint(T.accent, pct: 92%), {
        text(weight: "bold", "Goal: ")
        if goal == none or hidden(ctx, goal) { rule(T) } else { answer(ctx, goal) }
      })
  }
  let tasks = as-array(spec.at("tasks", default: ()))
  let all = (("task", "Task / step"), ("owner", "Who"), ("due", "When"), ("resources", "Resources"),
    ("measure", "Measure of progress"), ("status", "Status"))
  let fields = if "columns" in spec { all.filter(f => f.at(0) in as-array(spec.columns)) }
    else if ctx.learner or tasks.len() == 0 { all }
    else { all.filter(f => f.at(0) == "task" or tasks.any(t => type(t) == dictionary and f.at(0) in t)) }
  let n = if ctx.learner { calc.max(tasks.len(), spec.at("rows", default: 6)) } else { tasks.len() }
  let cells = ()
  for i in range(n) {
    let t = tasks.at(i, default: none)
    let t = if t == none { (:) } else if type(t) == dictionary { t } else { (task: t) }
    cells.push(text(fill: T.muted, str(i + 1)))
    for (k, _) in fields {
      let it = as-item(t.at(k, default: none))
      let it = if it != none and t.at("blank", default: false) == true { it + (blank: true) } else { it }
      cells.push(if it == none or hidden(ctx, it) { if ctx.learner { box(height: 2.2em) } } else { answer(ctx, it) })
    }
  }
  let widths = (task: 2.2fr, owner: 0.9fr, due: 0.8fr, resources: 1.4fr, measure: 1.4fr, status: 0.8fr)
  otable(T, columns: (auto,) + fields.map(f => widths.at(f.at(0))), header: ("#",) + fields.map(f => f.at(1)), ..cells)
  let ms = as-array(spec.at("milestones", default: ()))
  if ms.len() > 0 {
    block(above: 0.9em, text(weight: "bold", "Milestones"))
    for m in ms {
      let m = if type(m) == dictionary { m } else { (text: s(m)) }
      block(above: 0.3em, [#text(fill: T.accent, weight: "bold", s(m.at("date", default: ""))) #h(0.5em) #s(m.at("text", default: ""))])
    }
  }
}

// `body-of` draws a nested organizer section (passed in: Typst has no
// forward declarations).
#let render-structured-notes(spec, ctx, body-of) = {
  let T = ctx.T
  for (i, sec) in as-array(spec.sections).enumerate() {
    let k = s(sec.at("kind", default: "lines"))
    let prompt = sec.at("prompt", default: none)
    block(width: 100%, breakable: false, inset: 10pt, radius: 4pt, stroke: 0.8pt + T.border, below: 0.9em, {
      if prompt != none { block(below: 0.6em, text(weight: "bold", s(prompt))) }
      if k == "lines" {
        // every answer on a numbered line is something the learner writes
        let ans = as-array(sec.at("answers", default: ())).map(a => as-item(a) + (blank: true))
        let n = calc.max(ans.len(), sec.at("lines", default: if ans.len() == 0 { 3 } else { 0 }))
        let numbered = sec.at("numbered", default: true)
        for j in range(n) {
          let it = ans.at(j, default: none)
          grid(columns: (1.6em, 1fr), align: bottom,
            if numbered { text(fill: T.muted, str(j + 1) + ".") },
            if it == none or hidden(ctx, it) { rule(T) }
            else { box(width: 100%, height: line-h, stroke: (bottom: 0.5pt + T.border), align(bottom + left, answer(ctx, it))) })
        }
      } else if k == "fill-in" {
        par(leading: 1.1em, fill-in(ctx, sec.at("text", default: "")))
      } else if k == "list" {
        entries(ctx, sec.at("items", default: ()), bullet: sec.at("bullet", default: "•"))
      } else if k == "group" {
        let parts = as-array(sec.at("parts", default: ()))
        for (j, p) in parts.enumerate() {
          let p = if type(p) == dictionary { p } else { (label: s(p)) }
          block(above: 0.6em, text(weight: "medium", str(j + 1) + ". " + s(p.at("label", default: ""))))
          let a = as-item(p.at("answer", default: none))
          if a == none or ctx.learner { rules(T, p.at("lines", default: 3)) } else { block(inset: (left: 1.2em), answer(ctx, a + (blank: true))) }
        }
      } else if k == "organizer" {
        body-of(sec.organizer, ctx)
      }
    })
  }
}

#let render-assessment-checklist(spec, ctx) = {
  let T = ctx.T
  let fields = as-array(spec.at("fields", default: ("Participant name", "Date")))
  if fields.len() > 0 {
    block(below: 0.9em, grid(columns: fields.map(_ => 1fr), column-gutter: 1.2em,
      ..fields.map(f => grid(columns: (auto, 1fr), column-gutter: 4pt, align: bottom, s(f) + ":", rule(T)))))
  }
  let resp = as-array(spec.at("responses", default: ("Yes", "No"))).map(s)
  let cells = ()
  let mark-of(it) = if ctx.learner { none } else { s(it.at("mark", default: none)) }
  for c in as-array(spec.criteria) {
    let it = as-item(c)
    let sub = as-array(it.at("sub", default: ()))
    cells.push(it.text)
    for r in resp { cells.push(align(center, if sub.len() == 0 { tick-box(T, checked: mark-of(it) == r) })) }
    for sb in sub {
      let si = as-item(sb)
      cells.push(pad(left: 1.4em, [– #si.text]))
      for r in resp { cells.push(align(center, tick-box(T, checked: mark-of(si) == r))) }
    }
  }
  otable(T, columns: (1fr,) + resp.map(_ => auto),
    header: (s(spec.at("criteria-heading", default: "Criteria")),) + resp, ..cells)
  if spec.at("comments", default: true) {
    let cm = as-item(spec.at("comment", default: none))
    block(above: 0.9em, width: 100%, inset: 8pt, stroke: 0.6pt + T.border, radius: 3pt, {
      text(weight: "bold", "Comments:")
      if cm != none and not ctx.learner { block(above: 0.4em, answer(ctx, cm)) } else { rules(T, spec.at("comment-lines", default: 3)) }
    })
  }
}

#let render-rubric(spec, ctx) = {
  let T = ctx.T
  let levels = as-array(spec.levels)
  let lab(l) = { if "score" in l { s(l.score) + " — " } else { "" } } + s(l.label)
  if spec.at("show-scale", default: true) and levels.any(l => "definition" in l) {
    otable(T, columns: (auto, 1fr), header: ("Score", "Performance level"),
      ..levels.map(l => (text(weight: "bold", s(l.at("score", default: ""))),
        [#text(weight: "bold", s(l.label)) — #s(l.at("definition", default: ""))])).flatten())
    v(0.6em)
  }
  let scoring = spec.at("score-column", default: false)
  let cells = ()
  for c in as-array(spec.criteria) {
    cells.push({
      text(weight: "bold", s(c.skill))
      let w = c.at("weight", default: none)
      if w != none { text(fill: T.muted, size: 0.85em, [ (×#s(w))]) }
    })
    for (j, d) in as-array(c.descriptors).enumerate() {
      cells.push(text(size: 0.92em, s(d)))
    }
    if scoring { cells.push([]) }
  }
  if scoring {
    cells.push(table.cell(colspan: levels.len() + 1, align(right, text(weight: "bold", "Total"))))
    cells.push([])
  }
  otable(T, columns: (auto,) + levels.map(_ => 1fr) + if scoring { (auto,) } else { () },
    header: (s(spec.at("criteria-heading", default: "Skill")),) + levels.map(lab) + if scoring { ("Score",) } else { () },
    ..cells)
  let pass = spec.at("passing", default: none)
  if pass != none { block(above: 0.6em, [#text(weight: "bold", "Passing requirement: ")#s(pass)]) }
}

#let _phases = (
  before: ("Before", ("Why am I reading or listening to this?", "How can I use this information?", "What will I learn in this lesson?")),
  during: ("During", ("What is the main idea of ____?", "How does this relate to what I already know?", "What is different from, or conflicts with, my experience?")),
  after: ("After", ("How has my knowledge changed?", "What other questions do I have about the topic?", "How will I apply this on the job?")),
)

#let render-self-questioning(spec, ctx) = {
  let T = ctx.T
  let phases = as-array(spec.at("phases", default: ("before", "during", "after")))
  let lines = spec.at("lines", default: 2)
  for (i, ph) in phases.enumerate() {
    let ph = if type(ph) == dictionary { ph } else {
      let (name, qs) = _phases.at(s(ph), default: (s(ph), ()))
      (name: name, questions: qs)
    }
    let col = T.palette.at(calc.rem(i, T.palette.len()))
    block(width: 100%, below: 0.9em, inset: 10pt, radius: 4pt, stroke: (left: 3pt + col, rest: 0.6pt + T.border), {
      block(below: 0.5em, text(weight: "bold", fill: col, size: 1.1em, s(ph.at("name", default: ""))))
      for q in as-array(ph.at("questions", default: ())) {
        let q = if type(q) == dictionary { q } else { (text: s(q)) }
        block(above: 0.6em, below: 0.2em, text(weight: "medium", s(q.at("text", default: ""))))
        let a = as-item(q.at("answer", default: none))
        if a == none or ctx.learner { if ctx.learner or a == none { rules(T, lines) } }
        else { block(inset: (left: 1em), answer(ctx, a + (blank: true))) }
      }
    })
  }
}

// ---------- dispatch ----------

#let body-of(spec, ctx) = {
  let t = s(spec.type)
  let ctx = ctx + (blanks: s(spec.at("blanks", default: if has-marked(spec) { "marked" } else { "all" })))
  let r = if t == "t-chart" { render-t-chart(spec, ctx) }
    else if t == "attribute-matrix" { render-attribute-matrix(spec, ctx) }
    else if t == "flow-chart" { render-flow-chart(spec, ctx) }
    else if t == "mind-map" { render-mind-map(spec, ctx) }
    else if t == "concept-map" { render-concept-map(spec, ctx) }
    else if t == "kwl-chart" { render-kwl-chart(spec, ctx) }
    else if t == "anticipation-guide" { render-anticipation-guide(spec, ctx) }
    else if t == "action-plan" { render-action-plan(spec, ctx) }
    else if t == "structured-notes" {
      // a nested organizer section draws through a simplified dispatcher
      render-structured-notes(spec, ctx, (sp, cx) => {
        let tt = s(sp.type)
        let cx = cx + (blanks: s(sp.at("blanks", default: if has-marked(sp) { "marked" } else { "all" })))
        if tt == "mind-map" { render-mind-map(sp, cx) }
        else if tt == "concept-map" { render-concept-map(sp, cx) }
        else if tt == "flow-chart" { render-flow-chart(sp, cx) }
        else if tt == "t-chart" { render-t-chart(sp, cx) }
        else if tt == "kwl-chart" { render-kwl-chart(sp, cx) }
        else if tt == "attribute-matrix" { render-attribute-matrix(sp, cx) }
        else { text(fill: cx.T.red, "a " + tt + " cannot be nested in structured notes") }
      })
    }
    else if t == "assessment-checklist" { render-assessment-checklist(spec, ctx) }
    else if t == "rubric" { render-rubric(spec, ctx) }
    else if t == "self-questioning" { render-self-questioning(spec, ctx) }
  titled(spec, ctx, r)
}

#let load-spec(path) = {
  let p = s(path)
  if p.ends-with(".json") { json(p) } else { yaml(p) }
}

#let wide(spec) = {
  let o = spec.at("orientation", default: none)
  if o != none { s(o) == "landscape" }
  else if type(spec) == dictionary and s(spec.at("type", default: "")) in catalogue {
    catalogue.at(s(spec.type)).wide
  } else { false }
}

// The entry point. `spec` is a mapping or a path to a .yaml/.yml/.json file.
#let organizer(spec, theme: (:), version: "key", print: false) = {
  let spec = if type(spec) == str { load-spec(spec) } else { spec }
  let T = print-theme + theme
  let errs = validate(spec)
  [#metadata((errors: errs, type: if type(spec) == dictionary { spec.at("type", default: none) })) <organizer-check>]
  let ctx = (T: T, learner: s(version) == "learner", print: print, blanks: "all")
  if errs.len() > 0 { error-box(T, errs) }
  else if s(spec.type) == "handout" {
    titled(spec + (source: none), ctx, [])
    for (i, it) in as-array(spec.items).enumerate() {
      if i > 0 { if print { pagebreak(weak: true) } else { v(1.6em) } }
      body-of(it, ctx)
    }
    if "source" in spec { block(above: 0.7em, text(size: 0.82em, fill: T.muted, [Source: #s(spec.source)])) }
  } else { body-of(spec, ctx) }
}
