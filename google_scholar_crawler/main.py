from scholarly import scholarly, ProxyGenerator
import json
import os

def fetch_stats():
    pg = ProxyGenerator()
    pg.FreeProxies()  # Uses free rotating proxies
    scholarly.use_proxy(pg)

    try:
        author = scholarly.search_author_id("ObfU_PwAAAAJ")
        filled = scholarly.fill(author, sections=["indices"])

        stats = {
            "citations": filled["citedby"],
            "h_index": filled["hindex"],
            "i10_index": filled["i10index"]
        }

    except Exception as e:
        stats = {
            "citations": "Unavailable",
            "h_index": "Unavailable",
            "i10_index": "Unavailable"
        }

    # Write stats.json
    with open("google_scholar_crawler/stats.json", "w") as f:
        json.dump(stats, f, indent=4)

fetch_stats()
