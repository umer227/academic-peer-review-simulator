from __future__ import annotations

import httpx


async def search_semantic_scholar(title: str, domain: str, limit: int = 3) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params={
                    "query": f"{title} {domain}",
                    "limit": limit,
                    "fields": "title,authors,year,url",
                },
            )
            response.raise_for_status()
        papers = []
        for item in response.json().get("data", []):
            papers.append(
                {
                    "title": item.get("title", ""),
                    "authors": [author.get("name", "") for author in item.get("authors", [])],
                    "year": item.get("year"),
                    "doi": None,
                    "url": item.get("url"),
                    "source": "Semantic Scholar",
                }
            )
        return papers
    except Exception:
        return []
