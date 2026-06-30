# -*- coding: utf-8 -*-
"""
generate_authors.py
────────────────────────────────────────────────────────────────────────────────
Reads  Publication_Details.csv  and generates the full  authors/  folder tree
that the Hugo Academic theme expects — one sub-folder per unique co-author,
each containing an index.html.

USAGE
  1. Place this script in the SAME folder as Publication_Details.csv
     e.g.  C:/Users/HP/Downloads/Ajoy_New\generate_authors.py
  2. Open Command Prompt in that folder and run:
        python generate_authors.py
  3. The script creates / updates  .\authors\  next to itself.
────────────────────────────────────────────────────────────────────────────────
"""

import csv
import os
import re

# ── CONFIG ────────────────────────────────────────────────────────────────────
ME            = "Ajoy Karmakar"       
SITE_TITLE    = "Ajoy Karmakar"       
SITE_OWNER    = "Ajoy Karmakar"       
OWNER_ROLE    = "Junior Research Fellow"
CV_PATH       = "/files/Ajoy_CV.pdf"
CSV_FILE      = "Publication_Details.csv"   
# ─────────────────────────────────────────────────────────────────────────────


def slugify(name: str) -> str:
    """'Ajoy K Karmakar' → 'ajoy-k-karmakar'"""
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name)   # remove punctuation
    name = re.sub(r"\s+", "-", name)            # spaces → hyphens
    name = re.sub(r"-+", "-", name)             # collapse multiple hyphens
    return name


def apa_initial(full_name: str) -> str:
    """'Ajoy Karmakar' → 'Karmakar, A.'   (for APA citation display)"""
    parts = full_name.strip().split()
    if not parts:
        return full_name
    last  = parts[-1]
    inits = " ".join(p[0].upper() + "." for p in parts[:-1] if p)
    return f"{last}, {inits}" if inits else last


# ── HTML TEMPLATES ────────────────────────────────────────────────────────────

HEAD_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en-us">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="generator" content="Source Themes Academic 4.5.0">
  <meta name="author" content="{site_owner}">
  <meta name="description" content="{owner_role}">
  <link rel="alternate" hreflang="en-us" href="/authors/{slug}/">
  <meta name="theme-color" content="#556b2f">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/academicons/1.8.6/css/academicons.min.css" integrity="sha256-uFVgMKfistnJAfoCUQigIl+JfUaP47GrRKjf6CTPVmw=" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css" integrity="sha256-+N4/V/SbAFiW1MPBCXnfnP9QSN3+Keu+NlB+0ev/YKQ=" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.5.7/jquery.fancybox.min.css" integrity="sha256-Vzbj7sDDS/woiFS3uNKo8eIuni59rjyNGtXfstRzStA=" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/styles/github.min.css" crossorigin="anonymous" title="hl-light">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/styles/dracula.min.css" crossorigin="anonymous" title="hl-dark" disabled>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.5.1/leaflet.css" integrity="sha256-SHMGCYmST46SoyGgo4YR/9AlK1vf3ff84Aq9yK4hdqM=" crossorigin="anonymous">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Cutive+Mono%7CLora:400,700%7CRoboto:400,700&display=swap">
  <link rel="stylesheet" href="/css/academic.css">
  <link rel="alternate" href="/authors/{slug}/index.xml" type="application/rss+xml" title="{site_title}">
  <link rel="manifest" href="/index.webmanifest">
  <link rel="icon" type="image/png" href="/img/icon-32.png">
  <link rel="apple-touch-icon" type="image/png" href="/img/icon-192.png">
  <link rel="canonical" href="/authors/{slug}/">
  <meta property="og:site_name" content="{site_title}">
  <meta property="og:url" content="/authors/{slug}/">
  <meta property="og:title" content="{display_name} | {site_title}">
  <meta property="og:description" content="{owner_role}">
  <meta property="og:image" content="/img/avatar.jpg">
  <meta property="og:locale" content="en-us">
  <title>{display_name} | {site_title}</title>
</head>"""

NAVBAR_TEMPLATE = """\
<body id="top" data-spy="scroll" data-offset="70" data-target="#TableOfContents">

<aside class="search-results" id="search">
  <div class="container">
    <section class="search-header">
      <div class="row no-gutters justify-content-between mb-3">
        <div class="col-6"><h1>Search</h1></div>
        <div class="col-6 col-search-close">
          <a class="js-search" href="#"><i class="fas fa-times-circle text-muted" aria-hidden="true"></i></a>
        </div>
      </div>
      <div id="search-box">
        <input name="q" id="search-query" placeholder="Search..." autocapitalize="off"
               autocomplete="off" autocorrect="off" spellcheck="false" type="search">
      </div>
    </section>
    <section class="section-search-results">
      <div id="search-hits"></div>
    </section>
  </div>
</aside>

<nav class="navbar navbar-light fixed-top navbar-expand-lg py-0 compensate-for-scrollbar" id="navbar-main">
  <div class="container">
    <a class="navbar-brand" href="/">{site_title}</a>
    <button type="button" class="navbar-toggler" data-toggle="collapse"
            data-target="#navbar" aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation">
      <span><i class="fas fa-bars"></i></span>
    </button>
    <div class="collapse navbar-collapse" id="navbar">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item"><a class="nav-link" href="/#research"><span>Research</span></a></li>
        <li class="nav-item"><a class="nav-link" href="/#experience"><span>Experience</span></a></li>
        <li class="nav-item"><a class="nav-link" href="/#publications"><span>Publications</span></a></li>
        <li class="nav-item"><a class="nav-link" href="/#contact"><span>Contact</span></a></li>
        <li class="nav-item"><a class="nav-link" href="{cv_path}"><span>CV</span></a></li>
      </ul>
      <ul class="navbar-nav ml-auto">
        <li class="nav-item"><a class="nav-link js-search" href="#"><i class="fas fa-search" aria-hidden="true"></i></a></li>
        <li class="nav-item"><a class="nav-link js-dark-toggle" href="#"><i class="fas fa-moon" aria-hidden="true"></i></a></li>
      </ul>
    </div>
  </div>
</nav>"""

PROFILE_TEMPLATE = """\
<div class="universal-wrapper pt-3">
  <h1>{display_name}</h1>
</div>

<section id="profile-page" class="pt-5">
  <div class="container">
    <div class="article-widget content-widget-hr">
      <h3>Common research with {me_name}</h3>
      <ul>
{pub_list_items}
      </ul>
    </div>
  </div>
</section>"""

SCRIPTS_TEMPLATE = """\
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.imagesloaded/4.1.4/imagesloaded.pkgd.min.js" integrity="sha256-lqvxZrPLtfffUl2G/e7szqSvPBILGbwmsGE1MKlOi0Q=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.isotope/3.0.6/isotope.pkgd.min.js" integrity="sha256-CBrpuqrMhXwcLLUd5tvQ4euBHCdh7wGlDfNz8vbu/iI=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.5.7/jquery.fancybox.min.js" integrity="sha256-yt2kYMy0w8AbtF89WXb2P1rfjcP/HTHLT7097U8Y5b8=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/highlight.min.js" integrity="sha256-1zu+3BnLYV9LdiY85uXMzii3bdrkelyp37e0ZyTAQh0=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.5.1/leaflet.js" integrity="sha256-EErZamuLefUnbMBQbsEqu1USa+btR2oIlCpBJbyD4/g=" crossorigin="anonymous"></script>
    <script>hljs.initHighlightingOnLoad();</script>
    <script>
      const search_config = {"indexURI":"/index.json","minLength":1,"threshold":0.3};
      const i18n = {"no_results":"No results found","placeholder":"Search...","results":"results found"};
      const content_type = {'post':"Posts",'project':"Projects",'publication':"Publications",'talk':"Talks"};
    </script>
    <script src="/js/academic.min.d6bd04fdad2ad213aa8111c5a3b72fc5.js"></script>
</body>
</html>"""


def build_author_page(display_name, slug, pubs_for_author):
    """Returns full HTML string for one author's index.html"""

    # Build publication list items
    items = []
    for pub in pubs_for_author:
        title = pub["Title"]
        # link to publication slug if available, else just text
        pub_slug = slugify(pub["Title"])[:60]   # trim long titles
        item = f'        <li><a href="/publication/{pub_slug}/">{title}</a></li>'
        items.append(item)
    pub_list_html = "\n".join(items) if items else "        <li>No publications found.</li>"

    head    = HEAD_TEMPLATE.format(
                slug=slug, display_name=display_name,
                site_title=SITE_TITLE, site_owner=SITE_OWNER,
                owner_role=OWNER_ROLE)
    navbar  = NAVBAR_TEMPLATE.format(site_title=SITE_TITLE, cv_path=CV_PATH)
    profile = PROFILE_TEMPLATE.format(
                display_name=display_name,
                me_name=ME,
                pub_list_items=pub_list_html)
    scripts = SCRIPTS_TEMPLATE

    return f"{head}\n{navbar}\n{profile}\n{scripts}"


def build_admin_page(pubs):
    """Special fuller page for authors/admin/ (that's YOU — Ajoy Karmakar)"""
    items = []
    for pub in pubs:
        title = pub["Title"]
        pub_slug = slugify(title)[:60]
        item = f'        <li><a href="/publication/{pub_slug}/">{title}</a></li>'
        items.append(item)
    pub_list_html = "\n".join(items)

    head = HEAD_TEMPLATE.format(
                slug="admin", display_name=ME,
                site_title=SITE_TITLE, site_owner=SITE_OWNER,
                owner_role=OWNER_ROLE)
    navbar = NAVBAR_TEMPLATE.format(site_title=SITE_TITLE, cv_path=CV_PATH)
    profile = f"""\
<div class="universal-wrapper pt-3">
  <h1>{ME}</h1>
</div>

<section id="profile-page" class="pt-5">
  <div class="container">
    <div class="row">
      <div class="col-12 col-lg-4">
        <div id="profile">
          <img class="portrait" src="/authors/admin/avatar.jpg" alt="Avatar">
          <div class="portrait-title">
            <h2>{ME}</h2>
            <h3>{OWNER_ROLE}</h3>
            <h3><span>GB Pant National Institute of Himalayan Environment, Ladakh</span></h3>
          </div>
          <ul class="network-icon" aria-hidden="true">
            <li><a href="mailto:ajoy.iirs@gmail.com"><i class="fas fa-envelope big-icon"></i></a></li>
            <li><a href="https://github.com/ajoyk11" target="_blank"><i class="fab fa-github big-icon"></i></a></li>
            <li><a href="https://www.researchgate.net/profile/Ajoy-Karmakar" target="_blank"><i class="ai ai-researchgate big-icon"></i></a></li>
            <li><a href="https://orcid.org/0009-0004-4978-8908" target="_blank"><i class="fab fa-orcid big-icon"></i></a></li>
          </ul>
        </div>
      </div>
      <div class="col-12 col-lg-8">
        <div class="article-widget content-widget-hr">
          <h3>All Publications</h3>
          <ul>
{pub_list_html}
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>"""

    return f"{head}\n{navbar}\n{profile}\n{SCRIPTS_TEMPLATE}"


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path   = os.path.join(script_dir, CSV_FILE)
    authors_dir = os.path.join(script_dir, "authors")

    if not os.path.exists(csv_path):
        print(f"❌  CSV not found: {csv_path}")
        return

    # ── Read CSV ──────────────────────────────────────────────────────────────
    publications = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # collect all non-empty author columns
            authors = []
            for key, val in row.items():
                if key.startswith("Author") and val.strip():
                    authors.append(val.strip())
            row["_authors"] = authors
            publications.append(row)

    # Sort by Date_for_Sorting descending (newest first)
    publications.sort(key=lambda r: r.get("Date_for_Sorting", "0"), reverse=True)

    # ── Build author → pubs mapping ───────────────────────────────────────────
    author_pubs = {}   # display_name → [pub, pub, ...]
    for pub in publications:
        for author in pub["_authors"]:
            if author not in author_pubs:
                author_pubs[author] = []
            author_pubs[author].append(pub)

    print(f"📖  Found {len(publications)} publications")
    print(f"👥  Found {len(author_pubs)} unique authors:\n")
    for name in sorted(author_pubs.keys()):
        slug = slugify(name)
        marker = "  ← YOU (admin)" if name == ME else ""
        print(f"   {name:35s}  →  authors/{slug}/{marker}")

    print()

    # ── Create authors/ directory ─────────────────────────────────────────────
    os.makedirs(authors_dir, exist_ok=True)

    created = 0
    for display_name, pubs in author_pubs.items():
        slug = slugify(display_name)

        if display_name == ME:
            folder = os.path.join(authors_dir, "admin")
            os.makedirs(folder, exist_ok=True)
            html = build_admin_page(pubs)
            # Also create a sreenathpaleri-style named folder as alias
            alias_folder = os.path.join(authors_dir, slug)
            os.makedirs(alias_folder, exist_ok=True)
            with open(os.path.join(alias_folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
        else:
            folder = os.path.join(authors_dir, slug)
            os.makedirs(folder, exist_ok=True)
            html = build_author_page(display_name, slug, pubs)

        out_path = os.path.join(folder, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        created += 1
        print(f"  ✅  authors/{slug}/index.html")

    print(f"\n🎉  Done!  {created} author pages created in:  {authors_dir}")


if __name__ == "__main__":
    main()
