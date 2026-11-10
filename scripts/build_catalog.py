#!/usr/bin/env python3
"""Render the public catalogue from the publication records.

Each record is a Markdown file with YAML-style front matter.  The catalogue
renders one card per entry inside the site's shared page template.
"""
import glob
import html
import json
import os

HERE = os.path.dirname(__file__)
CONTENT_DIR = os.path.join(HERE, "..", "content", "publications")
HEADER_PATH = os.path.join(HERE, "catalog_header.html")
FOOTER_PATH = os.path.join(HERE, "catalog_footer.html")
OUT_PATH = os.path.join(HERE, "..", "public", "publications.html")


def parse_front_matter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    fm = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = json.loads(value)
        fm[key.strip()] = value
    return fm


def load_records():
    records = []
    # Publication records are kept flat in content/publications.
    for path in sorted(glob.glob(os.path.join(CONTENT_DIR, "*.md"))):
        with open(path, "r", encoding="utf-8") as handle:
            fm = parse_front_matter(handle.read())
        if fm.get("status", "").strip().lower() != "published":
            continue
        fm["_path"] = path
        records.append(fm)
    return records


def card(record):
    code = ""
    if record.get("codeurl"):
        code = ' <span class="badge code">Code</span>'
    return f"""
    <article class="pub-card" data-slug="{html.escape(record.get('slug',''))}">
      <h3 class="pub-title">{html.escape(record.get('title',''))}</h3>
      <p class="pub-authors">{html.escape(record.get('authors',''))}</p>
      <p class="pub-venue">{html.escape(record.get('venue',''))} &middot; {record.get('date','')}</p>
      <span class="badge venue">{html.escape(record.get('category',''))}</span>{code}
      <p class="pub-abstract">{html.escape(record.get('abstract',''))}</p>
    </article>"""


def render(records):
    cards = "".join(card(r) for r in sorted(records, key=lambda r: r.get("date", ""), reverse=True))
    with open(HEADER_PATH, "r", encoding="utf-8") as handle:
        header = handle.read()
    with open(FOOTER_PATH, "r", encoding="utf-8") as handle:
        footer = handle.read()
    return header + cards + footer


def main():
    records = load_records()
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(render(records))
    print(f"wrote {{len(records)}} entries to {{OUT_PATH}}")


if __name__ == "__main__":
    main()
