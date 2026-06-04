from __future__ import annotations

import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

import httpx


async def search_arxiv(title: str, domain: str, limit: int = 3) -> list[dict]:
    query = quote_plus(f'{title} {domain}')
    url = f"https://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={limit}"
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(url)
            response.raise_for_status()
        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []
        for entry in root.findall("atom:entry", ns):
            papers.append(
                {
                    "title": " ".join((entry.findtext("atom:title", default="", namespaces=ns)).split()),
                    "authors": [author.findtext("atom:name", default="", namespaces=ns) for author in entry.findall("atom:author", ns)],
                    "year": (entry.findtext("atom:published", default="", namespaces=ns) or "")[:4],
                    "doi": None,
                    "url": entry.findtext("atom:id", default="", namespaces=ns),
                    "source": "arXiv",
                }
            )
        return papers
    except Exception:
        return []
