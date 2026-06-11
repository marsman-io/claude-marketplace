---
name: video-distill
description: Turn a video (or its transcript) into structured, layered notes you'll actually retain — core message, concepts with analogies, critical analysis, an actionable framework, and memory anchors. Triggers on "summarize this video", "distill this talk", "analyze this YouTube video", "turn this video into notes", "what are the takeaways from <video>". Works from a transcript, captions, or a link you can fetch. NOT for transcribing raw audio you must process yourself, NOT for live streams, NOT for spoiler-y plot summaries of entertainment.
---

# Video distill

Turn a video into knowledge in a few minutes of reading, not the video's full
runtime. Work from the transcript / captions; if given only a link, fetch the
transcript first and cite timestamps.

## Procedure

1. **Get the content.** Obtain the transcript or captions with timestamps. If
   you cannot access them, say so and ask for the transcript rather than
   hallucinating the contents.

2. **Find the spine.** Identify the core message, the main concepts, the
   supporting arguments, and any data or concrete examples. Note the timestamp
   for each major point so claims stay checkable.

3. **Summarize structured.** A concise summary (aim 300–600 words unless told
   otherwise), organized under markdown headers by concept, not by chronology.

4. **Anchor with analogies.** For each major point, add one or two plain
   analogies that map the abstract idea to an everyday scenario. One good
   analogy beats three weak ones.

5. **Critical pass.** A short section on pros / cons, alternative perspectives
   (practical, ethical, technical), and where the claims are or aren't backed by
   evidence. Flag anything asserted without support — don't launder confidence.

6. **Actionable framework** (when the content supports one). A step-by-step
   sequence the reader can run today, derived from the video — not generic advice.

7. **Memory aids.** One or two mnemonics or anchors for retention, and a single
   final takeaway — the one thing to remember if everything else is forgotten.

## Output

Markdown, headers per section above. Objective and accurate; if it's
entertainment, keep it spoiler-free. Every non-obvious claim cites its
timestamp. No hype, no "this changed everything" framing.
