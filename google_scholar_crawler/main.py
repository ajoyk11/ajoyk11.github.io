import json
from scholarly import scholarly

# ---- SET YOUR GOOGLE SCHOLAR ID HERE ----
scholar_id = "ObfU_PwAAAAJ"   # change to ------ to test

print(f"Fetching data for Google Scholar ID: {scholar_id}")

# Fetch author profile
author = scholarly.search_author_id(scholar_id)
author = scholarly.fill(author, sections=['indices'])

stats = {
    "citations": author['citedby'],
    "h_index": author['hindex'],
    "i10_index": author['i10index'],
}

# Save JSON
with open("stats.json", "w") as f:
    json.dump(stats, f, indent=4)

print("stats.json updated successfully!")

