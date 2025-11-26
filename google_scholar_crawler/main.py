import scholarly
import json
import os

# YOUR GOOGLE SCHOLAR ID
scholar_id = "TgCHPTYAAAAJ"

def fetch_stats():
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["indices"])

    stats = {
        "citations": author["citedby"],
        "h_index": author["hindex"],
        "i10_index": author["i10index"]
    }

    # Save stats to JSON file in assets/data
    os.makedirs("assets/data", exist_ok=True)
    with open("assets/data/google_scholar_stats.json", "w") as f:
        json.dump(stats, f)

if __name__ == "__main__":
    fetch_stats()

