# Backend

FastAPI backend for the Multi-Agent Academic Peer Review Simulator.

## Run

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

## Environment

Copy `.env.example` to `.env`. If `DATABASE_URL` is omitted, the app uses local SQLite at `peer_review.db`.

PostgreSQL example:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/peer_review
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

Without LLM keys, the app returns professional mock agent responses.
