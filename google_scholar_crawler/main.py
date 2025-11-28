import json
from scholarly import scholarly
import requests

# Your Google Scholar ID
scholar_id = "ObfU_PwAAAAJ"

# ---- FREE ROTATING PROXY ----
# No signup, no phone, no API key needed
proxy_url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all"
proxies_list = requests.get(proxy_url).text.splitlines()

proxies = []
for p in proxies_list:
    if ":" in p:
        proxies.append({
            "http" : f"http://{p}",
            "https": f"http://{p}"
        })

print(f"Found {len(proxies)} proxies")

# Try proxies one-by-one until one works
author = None
for proxy in proxies[:20]:  # test first 20
    try:
        print(f"Trying proxy: {proxy}")
        scholarly.use_proxy(proxy)
        temp = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(temp, sections=['indices'])
        break
    except Exception as e:
        print(f"Proxy failed: {e}")
        continue

if author is None:
    raise RuntimeError("All proxies failed")

stats = {
    "citations": author.get('citedby', 0),
    "h_index": author.get('hindex', 0),
    "i10_index": author.get('i10index', 0)
}

with open("google_scholar_crawler/stats.json", "w") as f:
    json.dump(stats, f, indent=4)

print("Updated stats.json successfully:", stats)

