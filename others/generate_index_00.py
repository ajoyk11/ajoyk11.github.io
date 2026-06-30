# -*- coding: utf-8 -*-
"""
others/generate_index.py
────────────────────────────────────────────────────────────────────────────────
Generates  /index.json  at your site root — the search index that fuse.js
reads. Run this whenever you add new content (pages, publications, research).

USAGE
  Place this file in your  others/  folder.
  Run from your SITE ROOT:   python others/generate_index.py
  Output:  index.json  (created at site root, next to index.html)

WHAT IT INDEXES (union search — all words across all types):
  • All publications from Publication_Details.csv
  • Research pages:  research/*/index.html
  • Other pages you list in EXTRA_PAGES below

SEARCH BEHAVIOUR
  The fuse.js config in loader.js uses:
    minLength : 1   — starts matching from first character
    threshold : 0.3 — fuzzy tolerance (0 = exact, 1 = match anything)
  Searching "Fire Carbon Flux" returns results matching ANY of those words
  (union), ranked by relevance score.

TO ADD MORE PAGES TO THE INDEX:
  Add their paths to EXTRA_PAGES list below.
────────────────────────────────────────────────────────────────────────────────
"""

import csv, os, re, json

# ── CONFIG ────────────────────────────────────────────────────────────────────
SITE_ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE    = os.path.join(SITE_ROOT, "Publication_Details.csv")
OUTPUT_FILE = os.path.join(SITE_ROOT, "index.json")

# Add any extra standalone pages you want indexed
EXTRA_PAGES = [
    {"url": "/others/other_experiance/", "title": "Other Experiences",       "type": "page",    "body": "Equator Geo Stand For Forests NSS IFSA intern remote sensing GIS carbon"},
    {"url": "/project/",                 "title": "Projects",                 "type": "project", "body": "Fire flux carbon grassland Himalaya CLM5-FATES remote sensing"},
    {"url": "/publication/",             "title": "Publications & Conferences","type": "page",    "body": "publications conferences journal book chapter"},
]

# Research pages — auto-discovered from research/*/index.html
RESEARCH_DIR = os.path.join(SITE_ROOT, "research")
# ─────────────────────────────────────────────────────────────────────────────


def strip_html(text):
    """Remove HTML tags and collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()[:500]   # keep snippets short for fast loading


def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return re.sub(r"-+", "-", s)


entries = []

# ── 1. Publications from CSV ──────────────────────────────────────────────────
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            title   = (row.get("Title", "") or "").strip()
            year    = (row.get("Year",  "") or "").strip()
            ptype   = (row.get("Type",  "") or "").strip()
            authors = [v.strip() for k, v in row.items()
                       if k.startswith("Author") and v.strip()]
            doi     = (row.get("DOI",  "") or "").strip()
            url_path = "/publication/" + slugify(title)[:60] + "/"

            body = " ".join(filter(None, [title, year, ptype, " ".join(authors), doi]))

            entries.append({
                "objectID":    url_path,
                "url":         url_path,
                "relpermalink":url_path,
                "title":       title,
                "section":     "publication",
                "type":        ptype.lower() if ptype else "publication",
                "tags":        [ptype] if ptype else [],
                "body":        body,
                "snippet":     f"{', '.join(authors[:3])} ({year})" if authors else year,
            })
    print(f"  Publications indexed: {len(entries)}")
else:
    print(f"  WARNING: {CSV_FILE} not found — publications not indexed")

# ── 2. Research pages ─────────────────────────────────────────────────────────
research_count = 0
if os.path.isdir(RESEARCH_DIR):
    for project in os.listdir(RESEARCH_DIR):
        idx = os.path.join(RESEARCH_DIR, project, "index.html")
        if not os.path.isfile(idx):
            continue
        with open(idx, encoding="utf-8", errors="ignore") as f:
            html = f.read()

        # Try to extract <h1> as title
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
        title = strip_html(m.group(1)) if m else project.replace("-", " ").replace("_", " ").title()

        # Body = all visible text (stripped)
        body = strip_html(html)

        url_path = f"/research/{project}/"
        entries.append({
            "objectID":    url_path,
            "url":         url_path,
            "relpermalink":url_path,
            "title":       title,
            "section":     "research",
            "type":        "project",
            "tags":        ["research"],
            "body":        body,
            "snippet":     body[:120] + "…" if len(body) > 120 else body,
        })
        research_count += 1
print(f"  Research pages indexed: {research_count}")

# ── 3. Extra pages ────────────────────────────────────────────────────────────
for p in EXTRA_PAGES:
    entries.append({
        "objectID":    p["url"],
        "url":         p["url"],
        "relpermalink":p["url"],
        "title":       p["title"],
        "section":     p.get("type", "page"),
        "type":        p.get("type", "page"),
        "tags":        [],
        "body":        p.get("body", ""),
        "snippet":     p.get("body", "")[:120],
    })
print(f"  Extra pages indexed: {len(EXTRA_PAGES)}")

# ── 4. Write index.json ───────────────────────────────────────────────────────
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))

print(f"\n✅  index.json written → {OUTPUT_FILE}")
print(f"   Total entries: {len(entries)}")
print(f"   File size:     {os.path.getsize(OUTPUT_FILE) // 1024} KB")
print("\nSearch will now work across publications, research pages, and extra pages.")
