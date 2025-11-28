import json
from scholarly import scholarly

# ---- SET YOUR GOOGLE SCHOLAR ID HERE ----
scholar_id = "ObfU_PwAAAAJ"

print(f"Fetching Google Scholar data for: {scholar_id}")

try:
    # Get author object
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["indices"])

    stats = {
        "citations": author.get("citedby", "N/A"),
        "h_index": author.get("hindex", "N/A"),
        "i10_index": author.get("i10index", "N/A"),
    }

    # Save to stats.json
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)

    print("Updated stats.json successfully!")
    print(stats)

except Exception as e:
    print("Error while fetching data:", e)
