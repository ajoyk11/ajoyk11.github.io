# researchgate_crawler/main.py
from fetch import fetch_profile_html
from parser import parse_profile
import json
import os


PROFILE_URL = "https://www.researchgate.net/profile/Ajoy-Karmakar"

def fetch_stats():
    html = fetch_profile_html(PROFILE_URL)
    stats = parse_profile(html)

    # Save output as JSON for GitHub Actions
    out_path = os.path.join(os.path.dirname(__file__), "researchgate_stats.json")
    with open(out_path, "w") as f:
        json.dump(stats, f, indent=4)

    print("Successfully fetched ResearchGate stats:")
    print(json.dumps(stats, indent=4))


if __name__ == "__main__":
    fetch_stats()
