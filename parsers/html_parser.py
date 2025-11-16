from bs4 import BeautifulSoup

def parse_html(raw: bytes):
    soup = BeautifulSoup(raw, "html.parser")
    out = {
        "title": soup.title.string if soup.title else None,
        "meta": {m.get("name"): m.get("content") for m in soup.find_all("meta") if m.get("name")},
        "headings": {h.name: h.get_text(strip=True) for h in soup.find_all(["h1","h2","h3","h4","h5","h6"])},
        "links": [a.get("href") for a in soup.find_all("a", href=True)],
        "paragraphs": [p.get_text(strip=True) for p in soup.find_all("p")],
        "tables": []
    }

    # Extract tables
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all(["td","th"])]
            rows.append(cells)
        out["tables"].append(rows)

    out["raw_text"] = soup.get_text(separator=" ", strip=True)
    return [out]
