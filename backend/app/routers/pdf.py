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

    # Try: "Abstract" as a standalone heading followed by text on next lines
    abstract_match = re.search(
        r"(?:^|\n)\s*abstract\s*[:\-]?\s*\n([\s\S]{40,1500}?)(?=\n\s*(?:introduction|keywords|1[\.\s]|background|objective|method)\s*(?:\n|$)|$)",
        text,
        re.IGNORECASE,
    )
    # Try: "Abstract:" or "Abstract—" with text on the SAME line
    if not abstract_match:
        abstract_match = re.search(
            r"(?:^|\n)\s*abstract\s*[:\-—]\s*(.{40,1500}?)(?=\n\s*(?:introduction|keywords|1[\.\s]|background|objective|method)\s*(?:\n|$)|\n\n|$)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
    if abstract_match:
        abstract = abstract_match.group(1).strip()

    # Fallback: look for Objective/Overview/Summary sections (common in lab reports)
    if not abstract:
        obj_match = re.search(
            r"(?:^|\n)\s*(?:objective|overview|summary|purpose)\s*[:\-]?\s*\n?([\s\S]{40,800}?)(?=\n\s*(?:introduction|theory|background|method|procedure|1[\.\s])\s*(?:\n|$)|\n\n\n|$)",
            text,
            re.IGNORECASE,
        )
        if obj_match:
            abstract = obj_match.group(1).strip()

    # Last fallback: use the first long paragraph after the title line
    if not abstract and len(lines) > 1:
        candidate_lines = []
        for line in lines[1:15]:
            if len(line) > 60:
                candidate_lines.append(line)
            if len(" ".join(candidate_lines)) > 200:
                break
        if candidate_lines:
            abstract = " ".join(candidate_lines)[:800]

    intro_match = re.search(r"\n\s*(?:1[\.\s]+)?introduction\s*\n", text, re.IGNORECASE)
    if intro_match:
        content = text[intro_match.start():].strip()
    elif abstract:
        abs_pos = text.find(abstract[:80])
        if abs_pos != -1:
            content = text[abs_pos + len(abstract):].strip()

    if not content.strip():
        content = text

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
