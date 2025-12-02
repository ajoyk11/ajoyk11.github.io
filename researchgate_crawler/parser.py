# researchgate_crawler/parser.py
from bs4 import BeautifulSoup

def parse_profile(html):
    soup = BeautifulSoup(html, "html.parser")

    data = {
        "name": None,
        "citations": None,
        "reads": None,
        "recommendations": None,
        "publications": []
    }

    # Extract name
    name_tag = soup.find("h1")
    if name_tag:
        data["name"] = name_tag.get_text(strip=True)

    # Extract stats (Reads, Citations)
    for stat in soup.find_all("div", class_="nova-e-text"):
        text = stat.get_text(" ", strip=True)
        if "Reads" in text:
            data["reads"] = text.replace("Reads", "").strip()
        if "Citations" in text:
            data["citations"] = text.replace("Citations", "").strip()
        if "Recommendations" in text:
            data["recommendations"] = text.replace("Recommendations", "").strip()

    # Extract publications
    pubs = soup.find_all("div", class_="nova-e-text--spacing-none")
    for p in pubs:
        title = p.get_text(strip=True)
        if title and len(title) > 5:
            data["publications"].append(title)

    return data
