# Source Selection

## Inputs To Accept

- A Sefaria ref:
  - `Tanya, Part I; Likkutei Amarim.34`
  - `Tanya, Part I; Likkutei Amarim.34-35`
  - `Exodus.25.8`
- A paragraph or range in plain language:
  - `Tanya chapter 35 paragraphs 1-4`
  - `Likutei Amarim 34 and 35`
- A PDF source sheet or screenshot:
  - inspect the visible title, URL, chapter, paragraph numbers, and page count
  - recover the structured ref before rendering when possible

## Range Rules

- Keep the packet to the requested range.
- If the user gives only a broad chapter but the lecture covers a smaller span,
  ask for the paragraph range only when producing the full chapter would be
  materially too long.
- If the range is uncertain, render a clearly labeled draft and state the
  assumption.

## Source Fidelity

- Prefer original source text and recognized translations.
- Do not silently rewrite translations.
- If the output includes commentary, mark it as commentary.
- Keep source text separate from summary, prompts, and teaching notes.

## Tanya Shiur Ingestion

When publishing a Torah from the Table Tanya shiur, source selection is part of
the ingest, not an optional add-on.

- Infer the perakim from Fireflies titles such as `Tanya 34-35`, attached
  Sefaria PDFs, transcript opening lines, or Clark's explicit range.
- Render one packet for the full discussed span.
- Attach that PDF to the episode page.
- If the range cannot be recovered confidently, publish the episode only with a
  visible open task to add the source packet once the range is known.
