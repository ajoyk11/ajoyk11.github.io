# -*- coding: utf-8 -*-
"""
others/generate_index.py
────────────────────────────────────────────────────────────────────────────────
Generates  /index.json  at your site root — the search index that fuse.js reads.
Run from your SITE ROOT:   python others/generate_index.py

WHAT IT INDEXES:
  • All publications from Publication_Details.csv
  • Research pages:  research/*/index.html  (full body text)
  • Project pages:   project/*/index.html   (full body text)
  • Extra pages listed in EXTRA_PAGES below

Re-run whenever you add new pages or publications.
────────────────────────────────────────────────────────────────────────────────
"""

import csv, os, re, json

# ── CONFIG ────────────────────────────────────────────────────────────────────
SITE_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE     = os.path.join(SITE_ROOT, "Publication_Details.csv")
OUTPUT_FILE  = os.path.join(SITE_ROOT, "index.json")

# Extra standalone pages to index manually
EXTRA_PAGES = [
    {
        "url":     "/others/other_experiance/",
        "title":   "Other Experiences",
        "type":    "page",
        "body":    "Equator Geo Stand For Forests NSS IFSA intern remote sensing GIS carbon "
                   "National Service Scheme Recreation Secretary Mess Committee IIRS Dehradun "
                   "Race to Net Zero GHG estimation Google Earth Engine forestry voluntary"
    },
    {
        "url":     "/project/",
        "title":   "Projects",
        "type":    "project",
        "body":    "Fire flux carbon grassland Himalaya CLM5-FATES remote sensing machine learning "
                   "PFT plant functional type cyclone vulnerability flood forecast WRF HEC-RAS"
    },
    {
        "url":     "/publication/",
        "title":   "Publications & Conferences",
        "type":    "page",
        "body":    "publications conferences journal book chapter poster presentation"
    },
]

# Folders to auto-scan for index.html pages
SCAN_DIRS = ["research", "project"]
# ─────────────────────────────────────────────────────────────────────────────


def strip_html(text):
    """Remove all HTML tags and collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"&[a-zA-Z]+;", " ", text)       # remove HTML entities
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_title(html):
    """Extract the first <h1> tag text."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if m:
        return strip_html(m.group(1))
    return None


def extract_body(html):
    """Extract text from article-style or main content divs — full text, no truncation."""
    # Try article-style div first (research/project pages)
    m = re.search(r'class="article-style"[^>]*>(.*?)</div>\s*<!--\s*/article-style', html, re.DOTALL)
    if m:
        return strip_html(m.group(1))

    # Fallback: everything inside <body>, stripped of nav/footer/scripts
    body_m = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
    if body_m:
        body = body_m.group(1)
        # Remove script and style blocks
        body = re.sub(r"<script[^>]*>.*?</script>", " ", body, flags=re.DOTALL)
        body = re.sub(r"<style[^>]*>.*?</style>",  " ", body, flags=re.DOTALL)
        # Remove nav, footer, aside
        body = re.sub(r"<nav[^>]*>.*?</nav>",       " ", body, flags=re.DOTALL)
        body = re.sub(r"<footer[^>]*>.*?</footer>", " ", body, flags=re.DOTALL)
        body = re.sub(r"<aside[^>]*>.*?</aside>",   " ", body, flags=re.DOTALL)
        return strip_html(body)

    return strip_html(html)


def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return re.sub(r"-+", "-", s)


entries = []

# ── 1. Publications from CSV ──────────────────────────────────────────────────
pub_count = 0
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            title   = (row.get("Title",  "") or "").strip()
            year    = (row.get("Year",   "") or "").strip()
            ptype   = (row.get("Type",   "") or "").strip()
            authors = [v.strip() for k, v in row.items()
                       if k.startswith("Author") and v.strip()]
            doi     = (row.get("DOI",    "") or "").strip()
            url_path = "/publication/" + slugify(title)[:60] + "/"

            # Body = everything concatenated so all words are searchable
            body = " ".join(filter(None, [title, year, ptype, " ".join(authors), doi]))

            entries.append({
                "objectID":     url_path,
                "url":          url_path,
                "relpermalink": url_path,
                "title":        title,
                "section":      "publication",
                "type":         ptype.lower() if ptype else "publication",
                "tags":         [ptype] if ptype else [],
                "body":         body,
                "snippet":      f"{', '.join(authors[:3])} ({year})" if authors else year,
            })
            pub_count += 1
    print(f"  Publications indexed: {pub_count}")
else:
    print(f"  WARNING: {CSV_FILE} not found")

# ── 2. Auto-scan research/ and project/ folders ───────────────────────────────
page_count = 0
for folder in SCAN_DIRS:
    scan_path = os.path.join(SITE_ROOT, folder)
    if not os.path.isdir(scan_path):
        continue
    for project in sorted(os.listdir(scan_path)):
        idx = os.path.join(scan_path, project, "index.html")
        if not os.path.isfile(idx):
            continue
        with open(idx, encoding="utf-8", errors="ignore") as f:
            html = f.read()

        title = extract_title(html) or project.replace("-", " ").replace("_", " ").title()
        body  = extract_body(html)
        url_path = f"/{folder}/{project}/"

        entries.append({
            "objectID":     url_path,
            "url":          url_path,
            "relpermalink": url_path,
            "title":        title,
            "section":      folder,
            "type":         "project",
            "tags":         [folder],
            "body":         body,
            "snippet":      body[:150] + "…" if len(body) > 150 else body,
        })
        page_count += 1
        print(f"    indexed: /{folder}/{project}/  ({len(body)} chars)")

print(f"  Pages indexed: {page_count}")

# ── 3. Extra pages ────────────────────────────────────────────────────────────
for p in EXTRA_PAGES:
    entries.append({
        "objectID":     p["url"],
        "url":          p["url"],
        "relpermalink": p["url"],
        "title":        p["title"],
        "section":      p.get("type", "page"),
        "type":         p.get("type", "page"),
        "tags":         [],
        "body":         p.get("body", ""),
        "snippet":      p.get("body", "")[:150],
    })
print(f"  Extra pages indexed: {len(EXTRA_PAGES)}")

# ── 4. Write index.json ───────────────────────────────────────────────────────
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))

print(f"\n  index.json written → {OUTPUT_FILE}")
print(f"   Total entries : {len(entries)}")
print(f"   File size     : {os.path.getsize(OUTPUT_FILE) // 1024} KB")
