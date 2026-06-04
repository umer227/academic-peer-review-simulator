from __future__ import annotations

import httpx


async def search_crossref(title: str, domain: str, limit: int = 3) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(
                "https://api.crossref.org/works",
                params={"query.bibliographic": f"{title} {domain}", "rows": limit},
            )
            response.raise_for_status()
        papers = []
        for item in response.json().get("message", {}).get("items", []):
            authors = [
                " ".join(filter(None, [author.get("given"), author.get("family")]))
                for author in item.get("author", [])
            ]
            year_parts = item.get("published-print", item.get("published-online", {})).get("date-parts", [[None]])
            papers.append(
                {
                    "title": (item.get("title") or [""])[0],
                    "authors": authors,
                    "year": year_parts[0][0],
                    "doi": item.get("DOI"),
                    "url": item.get("URL"),
                    "source": "CrossRef",
                }
            )
        return papers
    except Exception:
        return []
