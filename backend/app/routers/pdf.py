import io
import re

from fastapi import APIRouter, HTTPException, UploadFile, File
from pypdf import PdfReader

router = APIRouter(prefix="/api", tags=["pdf"])


def _extract_text(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def _parse_sections(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    title = ""
    abstract = ""
    content = text

    if lines:
        title = lines[0][:200]

    abstract_match = re.search(
        r"(?:^|\n)\s*abstract\s*[:\-]?\s*\n?([\s\S]{80,1500?}?)(?=\n\s*(?:introduction|keywords|1\.|background)\s*|$)",
        text,
        re.IGNORECASE,
    )
    if abstract_match:
        abstract = abstract_match.group(1).strip()

    intro_match = re.search(r"\n\s*(?:1[\.\s]+)?introduction\s*\n", text, re.IGNORECASE)
    if intro_match:
        content = text[intro_match.start():].strip()
    elif abstract:
        content = text[text.find(abstract) + len(abstract):].strip()

    return {
        "title": title,
        "abstract": abstract[:1000],
        "content": content[:8000],
        "full_text": text,
    }


@router.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10 MB.")

    try:
        text = _extract_text(file_bytes)
    except Exception:
        raise HTTPException(status_code=422, detail="Could not read the PDF. Make sure it contains selectable text.")

    if not text:
        raise HTTPException(status_code=422, detail="No text found in the PDF. Scanned image PDFs are not supported.")

    return _parse_sections(text)
