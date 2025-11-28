# google_scholar_crawler/main.py
import os
import json
from datetime import datetime
from scholarly import scholarly

# Try to read ID from GitHub Secret
author_id = os.environ.get("GOOGLE_SCHOLAR_ID", "").strip()

# Fallback to your ID
if not author_id:
    author_id = "ObfU_PwAAAAJ"

print(f"Fetching Google Scholar data for: {author_id}")

# Clear scholarly cache
scholarly._SESSION.cookies.clear()

# Fetch author
author = scholarly.search_author_id(author_id)
author = scholarly.fill(author, sections=["basics", "indices"])

# Extract stats
citations = author.get("citedby", 0)
h_index = author.get("hindex", 0)
i10_index = author.get("i10index", 0)

stats = {
    "citations": citations,
    "h_index": h_index,
    "i10_index": i10_index,
    "updated": datetime.utcnow().isoformat() + "Z",
    "author_id": author_id
}

# Save stats.json for website
os.makedirs("google_scholar_crawler", exist_ok=True)
with open("google_scholar_crawler/stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)

# Also save full output
os.makedirs("results", exist_ok=True)
with open("results/gs_data.json", "w", encoding="utf-8") as f:
    json.dump(author, f, indent=2, ensure_ascii=False)

# Also write shield.io JSON
shield_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": str(citations)
}

with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
    json.dump(shield_data, f, indent=2, ensure_ascii=False)

print("Done. Stats updated.")
