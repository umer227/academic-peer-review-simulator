# Multi-Agent Academic Peer Review Simulator

A full-stack MVP web application for simulating academic peer review with multiple AI-style agents. The backend uses FastAPI and SQLAlchemy with PostgreSQL support plus a SQLite fallback. The frontend uses React and Vite with a polished dark research-dashboard interface inspired by the provided Stitch design.

## What Is Implemented

- Paper submission form for title, abstract, content, and domain.
- Seven-step agent workflow: submission, three reviewers, aggregation, decision, and author response.
- Mock LLM responses when `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` are absent.
- Optional GPT-4o and Claude 3.5 calls when keys are configured.
- Related paper lookup through arXiv, Semantic Scholar, and CrossRef with safe failure handling.
- SQLite local database fallback at `backend/peer_review.db`.
- Review history and single-review retrieval.

## Run Backend

```powershell
cd peer-review-simulator/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

## Run Frontend

```powershell
cd peer-review-simulator/frontend
npm install
npm run dev
```

Frontend URL: `http://127.0.0.1:5173`

## Environment

Create `backend/.env` from `backend/.env.example`.

```env
DATABASE_URL=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
FRONTEND_ORIGIN=http://127.0.0.1:5173
```

If `DATABASE_URL` is empty, SQLite is used automatically.

PostgreSQL example:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/peer_review
```

Create `frontend/.env` only if needed:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## API Endpoints

- `GET /health` checks service status.
- `POST /api/review-paper` runs the complete review workflow.
- `GET /api/reviews` returns saved review history.
- `GET /api/reviews/{paper_id}` returns one complete review.

Example request:

```json
{
  "title": "AI-Supported Peer Feedback for Reflective Learning",
  "abstract": "This study explores AI-supported peer feedback in higher education.",
  "content": "Full paper text goes here...",
  "domain": "Education"
}
```

## Demo Flow

1. Start the backend.
2. Start the frontend.
3. Open `http://127.0.0.1:5173`.
4. Submit the prefilled sample paper or paste your own manuscript.
5. Watch the agent workflow progress.
6. Review the formatted submission, three expert reviews, aggregate report, decision, author response letter, related papers, and saved history.

## How Agents Work

Each agent is a small Python function in `backend/app/agents`. Agents call the isolated `LLMService` in `backend/app/services/llm_service.py`. When API keys are available, the service tries OpenAI first and Anthropic second. If keys are missing or a provider call fails, it returns professional mock output so the MVP remains runnable locally.
