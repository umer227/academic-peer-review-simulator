import re
from urllib.parse import quote, urlencode
from urllib.request import urlopen
import xml.etree.ElementTree as ET


ARXIV_API_URL = "http://export.arxiv.org/api/query"
ARXIV_NAMESPACE = {"atom": "http://www.w3.org/2005/Atom"}
EDUCATION_WORDS = {
    "education",
    "educational",
    "learning",
    "teaching",
    "student",
    "students",
    "classroom",
    "curriculum",
    "pedagogy",
    "personalized",
}
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


def _clean_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(value.split())


def _normalize_query(query: str) -> str:
    return _clean_text(query)


def _important_words(query: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9]+", query)
    important_words = [word for word in words if word.lower() not in STOP_WORDS]
    return important_words or words


def _build_url(arxiv_query: str, max_results: int) -> str:
    params = urlencode(
        {
            "search_query": arxiv_query,
            "start": 0,
            "max_results": max(1, min(max_results, 10)),
        },
        quote_via=quote,
        safe=":",
    )
    return f"{ARXIV_API_URL}?{params}"


def _fetch_arxiv_entries(arxiv_query: str, max_results: int):
    url = _build_url(arxiv_query, max_results)
    print(f"Trying arXiv query URL: {url}")

    try:
        with urlopen(url, timeout=15) as response:
            xml_data = response.read()
    except Exception as exc:
        print(f"arXiv request failed: {exc}")
        return []

    try:
        root = ET.fromstring(xml_data)
    except Exception as exc:
        print(f"arXiv XML parse failed: {exc}")
        return []

    related_papers = []
    for entry in root.findall("atom:entry", ARXIV_NAMESPACE):
        title = _clean_text(entry.findtext("atom:title", default="", namespaces=ARXIV_NAMESPACE))
        summary = _clean_text(entry.findtext("atom:summary", default="", namespaces=ARXIV_NAMESPACE))
        published = entry.findtext("atom:published", default="", namespaces=ARXIV_NAMESPACE)
        arxiv_id_url = entry.findtext("atom:id", default="", namespaces=ARXIV_NAMESPACE)
        authors = [
            _clean_text(author.findtext("atom:name", default="", namespaces=ARXIV_NAMESPACE))
            for author in entry.findall("atom:author", ARXIV_NAMESPACE)
        ]

        related_papers.append(
            {
                "source": "arXiv",
                "title": title,
                "authors": ", ".join(author for author in authors if author),
                "year": published[:4] if published else "",
                "url": arxiv_id_url,
                "summary": summary,
            }
        )

    return related_papers


def _build_query_attempts(query: str) -> list[str]:
    normalized_query = _normalize_query(query)
    attempts = [f"all:{normalized_query}"]

    first_important_words = " ".join(_important_words(normalized_query)[:3])
    if first_important_words and first_important_words != normalized_query:
        attempts.append(f"all:{first_important_words}")

    normalized_words = {word.lower() for word in _important_words(normalized_query)}
    if normalized_words.intersection(EDUCATION_WORDS):
        attempts.append("all:machine learning education")

    unique_attempts = []
    for attempt in attempts:
        if attempt not in unique_attempts:
            unique_attempts.append(attempt)

    return unique_attempts


def search_related_papers(query: str, max_results: int = 5):
    normalized_query = _normalize_query(query)
    if not normalized_query:
        return []

    for arxiv_query in _build_query_attempts(normalized_query):
        related_papers = _fetch_arxiv_entries(arxiv_query, max_results)
        if related_papers:
            return related_papers

    return []
