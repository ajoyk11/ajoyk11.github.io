# -*- coding: utf-8 -*-
"""
update_publications.py
Reads Publication_Details.csv and updates TWO files:
  1. publication/index-section.html  — homepage fragment (top N entries)
  2. publication/index.html          — full filterable listing (all entries)
Run:  python update_publications.py
"""
import csv, os, re, shutil

# CONFIG
ME         = "Ajoy Karmakar"
TOP_N      = 5
CSV_FILE   = "Publication_Details.csv"
PUB_DIR    = "publication"

APA_TYPES = {"journal", "book chapter", "book"}


def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return re.sub(r"-+", "-", s)


def author_display(authors, bold_me=True):
    """Render author list with hyperlinks to /authors/<slug>/ pages."""
    parts = []
    for a in authors:
        slug = slugify(a)
        if bold_me and a == ME:
            parts.append(f'<a href="/authors/admin/"><strong>{a}</strong></a>')
        else:
            parts.append(f'<a href="/authors/{slug}/">{a}</a>')
    return ", ".join(parts)


def apa_last_init(name):
    p = name.strip().split()
    if not p:
        return name
    last = p[-1]
    inits = " ".join(x[0].upper() + "." for x in p[:-1] if x)
    return f"{last}, {inits}" if inits else last


def apa_authors(authors, bold_me=True):
    fmt = []
    for a in authors:
        apa = apa_last_init(a)
        slug = slugify(a)
        href = "/authors/admin/" if a == ME else f"/authors/{slug}/"
        if bold_me and a == ME:
            apa = f'<a href="{href}"><strong>{apa}</strong></a>'
        else:
            apa = f'<a href="{href}">{apa}</a>'
        fmt.append(apa)
    if len(fmt) == 1:
        return fmt[0]
    if len(fmt) == 2:
        return f"{fmt[0]}, &amp; {fmt[1]}"
    return ", ".join(fmt[:-1]) + f", &amp; {fmt[-1]}"


def get_url(pub):
    doi  = (pub.get("DOI",  "") or "").strip()
    link = (pub.get("Link", "") or "").strip()
    if doi and doi.upper() != "NA":
        return f"https://doi.org/{doi}" if not doi.startswith("http") else doi
    if link and link.upper() != "NA":
        return link
    return None


def doi_btn(pub, na_to_404=False):
    doi_raw = (pub.get("DOI", "") or "").strip()
    url = get_url(pub)
    if doi_raw.upper() == "NA" and na_to_404:
        return '<a class="btn btn-outline-primary my-1 mr-1 btn-sm" href="/404.html">DOI / Link</a>'
    if url:
        return (f'<a class="btn btn-outline-primary my-1 mr-1 btn-sm" '
                f'href="{url}" target="_blank" rel="noopener">DOI / Link</a>')
    return ""


def type_badge(pub_type):
    ltype = pub_type.lower()
    cls = "badge-primary" if ltype in ("journal", "book chapter", "book") else "badge-secondary"
    return f'<span class="badge {cls}" style="font-size:0.75em;">{pub_type}</span>'


# ── 1. HOMEPAGE SECTION ───────────────────────────────────────────────────────

def homepage_item(pub):
    title    = pub.get("Title", "").strip()
    year     = pub.get("Year", "").strip()
    pub_type = pub.get("Type", "").strip()
    pub_slug = slugify(title)[:60]
    authors  = author_display(pub["_authors"], bold_me=True)
    btn      = doi_btn(pub, na_to_404=False)
    badge    = type_badge(pub_type)
    # DOI/Link on the same line as year and badge
    btn_inline = f"&nbsp;{btn}" if btn else ""

    return (
        f'<div class="media stream-item">\n'
        f'  <div class="media-body">\n'
        f'    <h3 class="article-title mb-0 mt-0">\n'
        f'      <a href="/publication/{pub_slug}/">{title}</a>\n'
        f'    </h3>\n'
        f'    <div class="stream-meta article-metadata">\n'
        f'      <div>\n'
        f'        <span class="article-metadata li-cite-author">{authors}</span>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'    <div class="stream-meta article-metadata">\n'
        f'      <div>\n'
        f'        <span class="article-date">({year}).</span>&nbsp;{badge}{btn_inline}\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</div>\n'
    )


def build_homepage_section(pubs):
    items = "\n".join(homepage_item(p) for p in pubs)
    n = len(pubs)
    return (
        '<section id="publications" class="home-section wg-pages">\n'
        '  <div class="container">\n'
        '    <div class="row">\n'
        '      <div class="col-12 col-lg-4 section-heading">\n'
        '        <h1>Publications &amp; Conferences</h1>\n'
        '        <p><a href="/publication/">View all &rarr;</a></p>\n'
        '      </div>\n'
        '      <div class="col-12 col-lg-8">\n'
        '        <div class="alert alert-note">\n'
        '          <div>\n'
        '            Quickly discover relevant content by'
        ' <a href="/publication/">filtering publications</a>.\n'
        '          </div>\n'
        '        </div>\n'
        f'        <p style="font-size:0.88em;color:#777;">Showing {n} most recent works,'
        ' sorted by date. <a href="/publication/">See full list.</a></p>\n'
        f'{items}\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


# ── 2. FULL PUBLICATION PAGE ──────────────────────────────────────────────────

def full_item(pub):
    title    = pub.get("Title", "").strip()
    year     = pub.get("Year", "").strip()
    pub_type = pub.get("Type", "").strip()
    pub_slug = slugify(title)[:60]
    ltype    = pub_type.lower()
    authors  = author_display(pub["_authors"], bold_me=True)
    badge    = type_badge(pub_type)
    url      = get_url(pub)
    btn      = doi_btn(pub, na_to_404=True)
    # DOI/Link on the same line as year and badge
    btn_inline = f"&nbsp;{btn}" if btn else ""

    apa_block = ""
    if ltype in APA_TYPES:
        apa_str  = apa_authors(pub["_authors"], bold_me=True)
        doi_link = f' <a href="{url}" target="_blank">{url}</a>' if url else ""
        citation = f"{apa_str} ({year}). <em>{title}</em>.{doi_link}"
        apa_block = (
            '\n  <details style="margin-top:6px;">'
            '\n    <summary style="cursor:pointer;font-size:0.82em;color:#888;">&#9656; Cite (APA 7)</summary>'
            '\n    <blockquote style="font-size:0.82em;margin:6px 0 0 12px;color:#444;'
            'border-left:3px solid #ccc;padding-left:8px;">'
            f'\n      {citation}'
            '\n    </blockquote>'
            '\n  </details>'
        )

    return (
        f'<div class="pub-list-item" data-type="{pub_type.lower()}" data-year="{year}"\n'
        f'     style="margin-bottom:1.2rem;padding-bottom:1rem;border-bottom:1px solid #eee;">\n'
        f'  <div style="font-weight:600;">\n'
        f'    <a href="/publication/{pub_slug}/">{title}</a>\n'
        f'  </div>\n'
        f'  <div style="font-size:0.88em;color:#555;margin-top:3px;">{authors}</div>\n'
        f'  <div style="margin-top:4px;">'
        f'<span style="font-size:0.85em;color:#777;">({year}).</span>&nbsp;{badge}{btn_inline}</div>'
        f'{apa_block}\n'
        f'</div>\n'
    )


def build_pub_page(pubs):
    types = sorted(set(p.get("Type","").strip() for p in pubs if p.get("Type","").strip()))
    years = sorted(set(p.get("Year","").strip() for p in pubs if p.get("Year","").strip()), reverse=True)
    type_opts = "\n".join(f'            <option value="{t.lower()}">{t}</option>' for t in types)
    year_opts = "\n".join(f'            <option value="{y}">{y}</option>' for y in years)
    listing   = "\n".join(full_item(p) for p in pubs)

    return (
'<!DOCTYPE html>\n'
'<html lang="en-us">\n'
'<head>\n'
'  <meta charset="utf-8">\n'
'  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
'  <meta name="author" content="Ajoy Karmakar">\n'
'  <title>Publications | Ajoy Karmakar</title>\n'
'  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/academicons/1.8.6/css/academicons.min.css" crossorigin="anonymous">\n'
'  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css" crossorigin="anonymous">\n'
'  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap">\n'
'  <link rel="stylesheet" href="/css/academic.css">\n'
'  <link rel="manifest" href="/index.webmanifest">\n'
'  <link rel="icon" type="image/png" href="/img/icon-32.png">\n'
'  <style>\n'
'    body { padding-top:70px; font-family:"Roboto",sans-serif; }\n'
'    .pub-filters { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:1.2rem; }\n'
'    .pub-filters input, .pub-filters select { font-size:0.88rem; padding:4px 10px; border:1px solid #ccc; border-radius:4px; }\n'
'    .pub-list-item.hidden { display:none; }\n'
'    details > summary { list-style:none; }\n'
'    details > summary::-webkit-details-marker { display:none; }\n'
'  </style>\n'
'</head>\n'
'<body>\n'
'\n'
'<nav class="navbar navbar-light fixed-top navbar-expand-lg py-0" id="navbar-main">\n'
'  <div class="container">\n'
'    <a class="navbar-brand" href="/">Ajoy Karmakar</a>\n'
'    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar">\n'
'      <span><i class="fas fa-bars"></i></span>\n'
'    </button>\n'
'    <div class="collapse navbar-collapse" id="navbar">\n'
'      <ul class="navbar-nav mr-auto">\n'
'        <li class="nav-item"><a class="nav-link" href="/#research"><span>Research</span></a></li>\n'
'        <li class="nav-item"><a class="nav-link" href="/#experience"><span>Experience</span></a></li>\n'
'        <li class="nav-item"><a class="nav-link active" href="/publication/"><span>Publications</span></a></li>\n'
'        <li class="nav-item"><a class="nav-link" href="/#contact"><span>Contact</span></a></li>\n'
'        <li class="nav-item"><a class="nav-link" href="/files/Ajoy_CV.pdf"><span>CV</span></a></li>\n'
'      </ul>\n'
'    </div>\n'
'  </div>\n'
'</nav>\n'
'\n'
'<div class="container" style="max-width:860px;margin-bottom:4rem;">\n'
'  <div class="row"><div class="col-12">\n'
'    <h2 style="margin-bottom:1.2rem;">Publications &amp; Conferences</h2>\n'
'\n'
'    <div class="pub-filters">\n'
'      <input id="pub-search" type="search" placeholder="Search title or author..." style="min-width:220px;">\n'
'      <select id="pub-type">\n'
'        <option value="">All types</option>\n'
f'{type_opts}\n'
'      </select>\n'
'      <select id="pub-year">\n'
'        <option value="">All years</option>\n'
f'{year_opts}\n'
'      </select>\n'
'      <button id="pub-reset" class="btn btn-sm btn-outline-secondary">Reset</button>\n'
'    </div>\n'
'    <div id="pub-count" style="font-size:0.85em;color:#888;margin-bottom:1rem;"></div>\n'
'\n'
'    <div id="pub-container">\n'
f'{listing}\n'
'    </div>\n'
'  </div></div>\n'
'</div>\n'
'\n'
'<footer class="site-footer">\n'
'  <p class="powered-by"><a href="/">Ajoy Karmakar</a></p>\n'
'</footer>\n'
'\n'
'<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js" crossorigin="anonymous"></script>\n'
'<script src="/js/academic.min.d6bd04fdad2ad213aa8111c5a3b72fc5.js"></script>\n'
'<script>\n'
'(function() {\n'
'  var items   = Array.from(document.querySelectorAll(".pub-list-item"));\n'
'  var search  = document.getElementById("pub-search");\n'
'  var selType = document.getElementById("pub-type");\n'
'  var selYear = document.getElementById("pub-year");\n'
'  var reset   = document.getElementById("pub-reset");\n'
'  var countEl = document.getElementById("pub-count");\n'
'  function norm(s) { return (s||"").toLowerCase(); }\n'
'  function filter() {\n'
'    var q = norm(search.value), type = norm(selType.value), year = selYear.value;\n'
'    var v = 0;\n'
'    items.forEach(function(el) {\n'
'      var show = (!q    || norm(el.innerText).indexOf(q) !== -1)\n'
'              && (!type || norm(el.dataset.type) === type)\n'
'              && (!year || el.dataset.year === year);\n'
'      el.classList.toggle("hidden", !show);\n'
'      if (show) v++;\n'
'    });\n'
'    countEl.textContent = v + " of " + items.length + " entries shown";\n'
'  }\n'
'  search.addEventListener("input",  filter);\n'
'  selType.addEventListener("change", filter);\n'
'  selYear.addEventListener("change", filter);\n'
'  reset.addEventListener("click", function() {\n'
'    search.value=""; selType.value=""; selYear.value=""; filter();\n'
'  });\n'
'  filter();\n'
'})();\n'
'</script>\n'
'\n'
'</body>\n'
'</html>'
    )


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    script_dir        = os.path.dirname(os.path.abspath(__file__))
    csv_path          = os.path.join(script_dir, CSV_FILE)
    pub_dir           = os.path.join(script_dir, PUB_DIR)
    pub_idx_path      = os.path.join(pub_dir, "index.html")
    pub_section_path  = os.path.join(pub_dir, "index-section.html")

    if not os.path.exists(csv_path):
        print(f"Not found: {csv_path}"); return

    publications = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row["_authors"] = [v.strip() for k,v in row.items()
                               if k.startswith("Author") and v.strip()]
            publications.append(row)

    publications.sort(key=lambda r: r.get("Date_for_Sorting","0"), reverse=True)
    top_pubs = publications[:TOP_N]

    print(f"Total in CSV : {len(publications)}")
    print(f"Homepage section shows top {len(top_pubs)}")
    for p in top_pubs:
        print(f"  [{p.get('Year','')}] {p.get('Title','')[:70]}")

    os.makedirs(pub_dir, exist_ok=True)

    # 1. publication/index-section.html  <- loaded by index.html via fetch()
    if os.path.exists(pub_section_path):
        shutil.copy(pub_section_path, pub_section_path + ".bak")
    with open(pub_section_path, "w", encoding="utf-8") as f:
        f.write("<!-- AUTO-GENERATED by update_publications.py - do not edit manually -->\n")
        f.write(build_homepage_section(top_pubs))
    print("publication/index-section.html updated  (homepage fragment)")

    # 2. publication/index.html  <- standalone full filterable page
    if os.path.exists(pub_idx_path):
        shutil.copy(pub_idx_path, pub_idx_path + ".bak")
    with open(pub_idx_path, "w", encoding="utf-8") as f:
        f.write(build_pub_page(publications))
    print("publication/index.html updated  (full standalone page)")
    print("Done!")


if __name__ == "__main__":
    main()
