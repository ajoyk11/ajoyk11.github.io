import json
import requests
from scholarly import scholarly

scholar_id = "ObfU_PwAAAAJ"

# 1. Get 50 proxies
proxy_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
raw = requests.get(proxy_url).text.splitlines()
proxies = [p.strip() for p in raw if ":" in p][:50]

print(f"Loaded {len(proxies)} proxies")

author = None

# 2. Try proxies one by one
for proxy in proxies:
    proxy_dict = {"http": "http://" + proxy, "https": "http://" + proxy}
    print(f"Trying proxy {proxy}")

    try:
        scholarly.use_proxy(proxy_dict)
        temp = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(temp, sections=["indices"])
        print("SUCCESS with proxy:", proxy)
        break
    except Exception as e:
        print(f"Failed: {e}")
        continue

# 3. If still None → write fallback
if author is None:
    print("Google Scholar fetch failed. Writing fallback stats.")

    stats = {
        "citations": "Unavailable",
        "h_index": "Unavailable",
        "i10_index": "Unavailable"
    }
else:
    stats = {
        "citations": author.get("citedby", "Unavailable"),
        "h_index": author.get("hindex", "Unavailable"),
        "i10_index": author.get("i10index", "Unavailable")
    }

# 4. Save JSON
with open("google_scholar_crawler/stats.json", "w") as f:
    json.dump(stats, f, indent=4)

print("Written stats:", stats)
