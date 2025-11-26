# google_scholar_crawler/main.py
import os
import json
from datetime import datetime
import requests

SERPAPI_KEY = os.environ.get("SERPAPI_API_KEY")
AUTHOR_ID = os.environ.get("GOOGLE_SCHOLAR_ID")

if not SERPAPI_KEY:
    raise SystemExit("Missing SERPAPI_API_KEY environment variable (set as repo secret).")
if not AUTHOR_ID:
    raise SystemExit("Missing GOOGLE_SCHOLAR_ID environment variable (set as repo secret).")

print(f"Fetching SerpAPI Google Scholar author data for: {AUTHOR_ID}")

# SerpAPI endpoint for Google Scholar Author
url = "https://serpapi.com/search.json"
params = {
    "engine": "google_scholar_author",
    "author_id": AUTHOR_ID,
    "hl": "en",
    "api_key": SERPAPI_KEY,
    # no_cache param if you prefer fresh every run; not needed here
}

resp = requests.get(url, params=params, timeout=30)
resp.raise_for_status()
data = resp.json()

# Save full raw response for debugging/inspection
os.makedirs("results", exist_ok=True)
with open("results/gs_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Try to extract citations, h_index and i10_index from the response.
# SerpApi structures vary slightly; check common paths robustly.
def extract_table(d):
    # common patterns: data['cited_by']['table'] or data['author']['cited_by']['table']
    if not isinstance(d, dict):
        return {}
    if "cited_by" in d and isinstance(d["cited_by"], dict):
        tb = d["cited_by"].get("table") or d["cited_by"].get("table_data") or {}
        if isinstance(tb, dict) and tb:
            return tb
    if "author" in d and isinstance(d["author"], dict):
        cited = d["author"].get("cited_by") or {}
        tb = cited.get("table") if isinstance(cited, dict) else None
        if isinstance(tb, dict) and tb:
            return tb
    # top-level table
    if "table" in d and isinstance(d["table"], dict):
        return d["table"]
    return {}

table = extract_table(data)

# fallback extraction keys
citations = None
h_index = None
i10_index = None

if table:
    # keys may be 'citations', 'h_index', 'i10_index' or numeric lists
    citations = table.get("citations") or table.get("total_citations") or table.get("total")
    # h_index might be 'h_index' or 'h-index'
    h_index = table.get("h_index") or table.get("h-index") or table.get("hindex")
    i10_index = table.get("i10_index") or table.get("i10-index") or table.get("i10index")

# Some SerpAPI responses use slightly different nesting; try additional heuristics
if citations is None:
    # try path: data['author']['author_stats']['table'] etc.
    try:
        author = data.get("author") or {}
        author_cited = author.get("cited_by") or {}
        if isinstance(author_cited, dict):
            tb = author_cited.get("table") or {}
            citations = citations or tb.get("citations")
            h_index = h_index or tb.get("h_index") or tb.get("h-index")
            i10_index = i10_index or tb.get("i10_index")
    except Exception:
        pass

# Final fallback: look for digits in top-level keys
if citations is None:
    for k, v in data.items():
        if isinstance(v, dict):
            # if v has 'citations' key
            if "citations" in v:
                citations = citations or v.get("citations")
                h_index = h_index or v.get("h_index")
                i10_index = i10_index or v.get("i10_index")

# Convert to int if possible
def to_int(x):
    try:
        return int(x)
    except Exception:
        return None

citations = to_int(citations)
h_index = to_int(h_index)
i10_index = to_int(i10_index)

# Build minimal stats (used by site)
stats = {
    "citations": citations if citations is not None else 0,
    "h_index": h_index if h_index is not None else 0,
    "i10_index": i10_index if i10_index is not None else 0,
    "updated": datetime.utcnow().isoformat() + "Z",
    "author_id": AUTHOR_ID
}

# Write site stats to google_scholar_crawler/stats.json
os.makedirs("google_scholar_crawler", exist_ok=True)
with open("google_scholar_crawler/stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print("Written google_scholar_crawler/stats.json:", stats)

# Also write SerpAPI-friendly shields.io JSON (similar to reference repo)
shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{stats['citations']}",
}
with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
    json.dump(shieldio_data, f, ensure_ascii=False, indent=2)

print("All done.")
