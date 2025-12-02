# researchgate_crawler/fetch.py
import requests
from fake_useragent import UserAgent

ua = UserAgent()

def fetch_profile_html(url):
    headers = {"User-Agent": ua.random}
    r = requests.get(url, headers=headers, timeout=10)

    if r.status_code != 200:
        raise Exception(f"Failed to fetch profile page. Status: {r.status_code}")

    return r.text
