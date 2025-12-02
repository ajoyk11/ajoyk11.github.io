from scholarly import scholarly, ProxyGenerator
import json

SCHOLAR_ID = "ObfU_PwAAAAJ"

def fetch_stats():
    # use free rotating proxies (old version supports this)
    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)

    try:
        author = scholarly.search_author_id(SCHOLAR_ID)
        filled = scholarly.fill(author, sections=["indices"])

        stats = {
            "citations": filled.get("citedby", "Unavailable"),
            "h_index": filled.get("hindex", "Unavailable"),
            "i10_index": filled.get("i10index", "Unavailable")
        }

    except Exception:
        stats = {
            "citations": "Unavailable",
            "h_index": "Unavailable",
            "i10_index": "Unavailable"
        }

    with open("google_scholar_crawler/stats.json", "w") as f:
        json.dump(stats, f, indent=4)

    print("Updated stats:", stats)


if __name__ == "__main__":
    fetch_stats()
