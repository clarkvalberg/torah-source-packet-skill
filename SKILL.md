---
name: torah-source-packet
description: "Create printable bilingual Torah source packets from Sefaria refs, paragraph ranges, or supplied source PDFs."
---

# Torah Source Packet

Use when a user wants a polished printable source sheet for a shiur, lecture,
chaburah, or learning session from a Torah text range.

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

## Default Style

Use the standard in `references/editorial-standard.md`. The baseline should feel
like a tasteful source packet for a real shiur: quiet, legible, and restrained.

## Helper

Use `scripts/render_torah_packet.py` for Sefaria-backed packets when possible.
It accepts one or more `--ref` values and writes a print-ready HTML file. If a
local PDF renderer is available, it can also write PDF.
