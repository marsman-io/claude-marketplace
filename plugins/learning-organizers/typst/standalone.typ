// Standalone page for one organizer spec: a printable PDF (paper size, one
// organizer or one handout item per page) or a PNG/SVG as tall as it needs.
// Driven by scripts/organizer.py:
//   typst compile --root / --input spec=/abs/spec.yaml [--input version=learner]
//     [--input format=png] [--input dark=true] [--input paper=a4] standalone.typ out.pdf
#import "organizers.typ": organizer, load-spec, wide, print-theme, dark-theme

#let inp = sys.inputs
#let spec = load-spec(inp.at("spec"))
#let fmt = inp.at("format", default: "pdf")
#let T = if inp.at("dark", default: "false") == "true" { dark-theme } else { print-theme }
#let landscape = wide(spec)
#let paper = inp.at("paper", default: "us-letter")

#set document(title: if type(spec) == dictionary { str(spec.at("title", default: "Organizer")) } else { "Organizer" })
#set page(paper: paper, flipped: landscape, margin: 0.6in, fill: T.bg) if fmt == "pdf"
#set page(width: if landscape { 11in } else { 8.5in }, height: auto, margin: 0.4in, fill: T.bg) if fmt != "pdf"
#set text(font: ("Helvetica Neue", "Helvetica", "Arial"), size: 10.5pt, fill: T.fg)
#set par(leading: 0.6em)

// The room an organizer has, without `layout` (a handout's page breaks must
// stay outside any container).
#let (pw, ph) = if fmt != "pdf" { (8.5in, 11in) } else if paper == "a4" { (210mm, 297mm) } else { (8.5in, 11in) }
#let (pw, ph) = if landscape { (if fmt != "pdf" { 11in } else { ph }, pw) } else { (pw, ph) }
#let margin = if fmt == "pdf" { 0.6in } else { 0.4in }
#organizer(spec,
  theme: T + (width: pw - 2 * margin, height: if fmt == "pdf" { ph - 2 * margin } else { (pw - 2 * margin) * 1.1 }),
  version: inp.at("version", default: "key"),
  print: fmt == "pdf")
