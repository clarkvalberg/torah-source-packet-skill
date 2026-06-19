#!/usr/bin/env python3
"""Render a printable Torah source packet from one or more Sefaria refs."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


SEFARIA_API = "https://www.sefaria.org/api/texts/{ref}?commentary=0&context=0"


class _Stripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return " ".join(" ".join(self.parts).split())


def strip_html(value: Any) -> str:
    if value is None:
        return ""
    raw = str(value)
    parser = _Stripper()
    parser.feed(raw)
    return parser.text() or re.sub(r"<[^>]+>", "", raw)


def flatten(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(flatten(item))
        return out
    text = strip_html(value)
    return [text] if text else []


def fetch_ref(ref: str) -> dict[str, Any]:
    url = SEFARIA_API.format(ref=urllib.parse.quote(ref, safe=""))
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if "error" in payload:
        raise RuntimeError(f"Sefaria error for {ref}: {payload['error']}")
    return payload


def rows_for_ref(payload: dict[str, Any]) -> list[dict[str, str]]:
    hebrew = flatten(payload.get("he"))
    english = flatten(payload.get("text"))
    total = max(len(hebrew), len(english))
    rows: list[dict[str, str]] = []
    for index in range(total):
        rows.append(
            {
                "number": str(index + 1),
                "he": hebrew[index] if index < len(hebrew) else "",
                "en": english[index] if index < len(english) else "",
            }
        )
    return rows


def render_html(title: str, subtitle: str, refs: list[str], sections: list[dict[str, Any]]) -> str:
    sections_html = []
    for section in sections:
        row_html = []
        for row in section["rows"]:
            row_html.append(
                f"""
                <section class="source-row">
                  <div class="source-meta">{html.escape(row["number"])}</div>
                  <div class="source-he" dir="rtl" lang="he">{html.escape(row["he"])}</div>
                  <div class="source-en" lang="en">{html.escape(row["en"])}</div>
                </section>
                """
            )
        sections_html.append(
            f"""
            <article class="source-section">
              <h2>{html.escape(section["title"])}</h2>
              {''.join(row_html)}
            </article>
            """
        )

    refs_text = " · ".join(refs)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --ink: #181512;
      --muted: #6f675d;
      --rule: #ddd4c8;
      --paper: #fffdf8;
      --accent: #7c4d2d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #f3eee6;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{
      max-width: 960px;
      margin: 0 auto;
      min-height: 100vh;
      background: var(--paper);
      padding: 48px 54px 40px;
    }}
    header {{
      border-bottom: 1px solid var(--rule);
      padding-bottom: 22px;
      margin-bottom: 30px;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 12px;
      letter-spacing: .08em;
      text-transform: uppercase;
      font-weight: 700;
      margin-bottom: 10px;
    }}
    h1 {{
      font-family: Georgia, "Times New Roman", serif;
      font-size: 34px;
      line-height: 1.12;
      margin: 0 0 10px;
      letter-spacing: 0;
    }}
    .subtitle {{
      color: var(--muted);
      font-size: 16px;
      max-width: 720px;
      margin: 0;
    }}
    .refs {{
      margin-top: 18px;
      color: var(--muted);
      font-size: 12px;
    }}
    h2 {{
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: .06em;
      color: var(--accent);
      margin: 30px 0 14px;
    }}
    .source-row {{
      display: grid;
      grid-template-columns: 42px minmax(0, 1fr) minmax(0, 1fr);
      gap: 22px;
      padding: 16px 0;
      border-top: 1px solid var(--rule);
      break-inside: avoid;
    }}
    .source-meta {{
      color: var(--muted);
      font-size: 12px;
      padding-top: 3px;
    }}
    .source-he, .source-en {{
      font-family: Georgia, "Times New Roman", serif;
      font-size: 17px;
      line-height: 1.72;
    }}
    .source-he {{
      text-align: right;
      font-size: 19px;
    }}
    footer {{
      margin-top: 42px;
      padding-top: 14px;
      border-top: 1px solid var(--rule);
      color: var(--muted);
      font-size: 11px;
    }}
    @media print {{
      body {{ background: white; }}
      main {{ max-width: none; padding: 30px 34px; }}
      @page {{ margin: 0.55in; }}
    }}
    @media (max-width: 720px) {{
      main {{ padding: 30px 22px; }}
      .source-row {{ grid-template-columns: 32px 1fr; }}
      .source-en {{ grid-column: 2; }}
      h1 {{ font-size: 29px; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="eyebrow">Source Packet</div>
      <h1>{html.escape(title)}</h1>
      <p class="subtitle">{html.escape(subtitle)}</p>
      <div class="refs">{html.escape(refs_text)}</div>
    </header>
    {''.join(sections_html)}
    <footer>Rendered from Sefaria refs for private study and shiur preparation. Verify the final range before printing.</footer>
  </main>
</body>
</html>
"""


def try_pdf(html_path: Path, pdf_path: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception as exc:
        raise RuntimeError(
            "PDF rendering needs Playwright. Install with `python -m pip install playwright` "
            "and `python -m playwright install chromium`, or print the HTML to PDF from a browser."
        ) from exc

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.pdf(path=str(pdf_path), format="Letter", print_background=True)
        browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", action="append", required=True, help="Sefaria ref. May be repeated.")
    parser.add_argument("--title", required=True, help="Packet title.")
    parser.add_argument("--subtitle", default="", help="Short context line.")
    parser.add_argument("--out", required=True, help="Output HTML path.")
    parser.add_argument("--pdf", help="Optional output PDF path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sections = []
    for ref in args.ref:
        payload = fetch_ref(ref)
        sections.append(
            {
                "title": payload.get("ref") or ref,
                "rows": rows_for_ref(payload),
            }
        )

    html_text = render_html(args.title, args.subtitle, args.ref, sections)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_text, encoding="utf-8")

    if args.pdf:
        try_pdf(out_path, Path(args.pdf))

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
