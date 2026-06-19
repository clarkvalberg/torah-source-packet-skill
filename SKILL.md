---
name: torah-source-packet
description: "Create printable bilingual Torah source packets from Sefaria refs, paragraph ranges, or supplied source PDFs."
---

# Torah Source Packet

Use when a user wants a polished printable source sheet for a shiur, lecture,
chaburah, or learning session from a Torah text range.

Also use this during Torah from the Table ingestion for every Tanya shiur:
identify the perakim discussed, render the source-packet PDF, and attach it to
the episode page alongside the audio and transcript.

## Workflow

1. Identify the exact source range: work, chapter, paragraph, and whether the
   user wants Hebrew, English, or bilingual.
2. Prefer structured refs from Sefaria when available. Use supplied PDFs as
   visual references or backup text, not as the only source of truth.
3. Create an editorial packet, not a data dump:
   - clear title and subtitle
   - source refs and short context line
   - Hebrew and English in aligned sections
   - generous margins, readable type, and printable contrast
   - page footer with source and date when helpful
4. Keep the packet faithful. Do not paraphrase source text unless the user asks
   for a summary or teaching handout.
5. Render HTML first, then PDF from the same source.
6. Verify the PDF visually before delivery: readable Hebrew, no clipped text,
   sane page breaks, and no private/local paths.

## Torah From The Table Tanya Rule

For any `Tanya Thursday Nights` episode:

1. Resolve the discussed perakim from the Fireflies title, transcript, source
   PDFs, or explicit user note.
2. Render a bilingual source packet for those perakim.
3. Save it with the episode assets, using a durable slug such as
   `pieces/<episode-slug>-source-packet.pdf`.
4. Add `Download Source Packet` beside `Download Audio` and
   `Download Transcript`.
5. Add a visible Source Packet card on the episode page.
6. Do not mark the episode ingestion complete until the source packet is linked
   or explicitly blocked.

## Default Style

Use the standard in `references/editorial-standard.md`. The baseline should feel
like a tasteful source packet for a real shiur: quiet, legible, and restrained.

## Helper

Use `scripts/render_torah_packet.py` for Sefaria-backed packets when possible.
It accepts one or more `--ref` values and writes a print-ready HTML file. If a
local PDF renderer is available, it can also write PDF.
