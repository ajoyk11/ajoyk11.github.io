from scholarly import scholarly
import json

def fetch_stats():
    try:
        author = scholarly.search_author_id("ObfU_PwAAAAJ")
        filled = scholarly.fill(author, sections=["indices"])

        stats = {
            "citations": filled.get("citedby", "Unavailable"),
            "h_index": filled.get("hindex", "Unavailable"),
            "i10_index": filled.get("i10index", "Unavailable")
        }

    except Exception as e:
        stats = {
            "citations": "Unavailable",
            "h_index": "Unavailable",
            "i10_index": "Unavailable"
        }

    with open("google_scholar_crawler/stats.json", "w") as f:
        json.dump(stats, f, indent=4)


fetch_stats()
