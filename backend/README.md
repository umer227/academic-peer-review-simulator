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

## Deploy Backend on Vercel

Create a separate Vercel project for the backend.

- Root Directory: `backend`
- Framework Preset: `Other`
- Build Command: leave empty, or use `pip install -r requirements.txt` if your Vercel setup asks for one
- Output Directory: leave empty

Environment variables:

```env
FRONTEND_ORIGIN=https://your-frontend.vercel.app
OPENAI_API_KEY=optional
ANTHROPIC_API_KEY=optional
DATABASE_URL=optional
```

Routes after deployment:

- `GET /`
- `GET /health`
- `POST /api/review-paper`
- `GET /api/reviews`
- `GET /api/reviews/{paper_id}`

Database note: Vercel serverless storage is temporary. If `DATABASE_URL` is missing on Vercel, the app uses SQLite at `/tmp/peer_review.db` only for demo runtime behavior. For persistent production history, set `DATABASE_URL` to PostgreSQL.
