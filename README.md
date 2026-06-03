# Multi-Agent Academic Peer Review Simulator

A clean full-stack MVP scaffold for a 5-day university demo. This project is intentionally simple and runnable locally.

The current version includes:

- FastAPI backend with SQLAlchemy, Pydantic, SQLite-by-default config, CORS, and `GET /health`
- React + Vite + Tailwind CSS frontend with Axios and React Router
- Optional PostgreSQL service via Docker Compose for future deployment

AI agents and arXiv integrations are not implemented yet.

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

## Run Locally

### 1. Run the Backend Without Docker

```bash
cd backend
copy .env.example .env
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL: `http://localhost:8000`

Health check: `http://localhost:8000/health`

By default, the backend uses SQLite at `backend/peer_review.db`. Docker and PostgreSQL are optional for the local MVP.

### 2. Optional PostgreSQL With Docker

```bash
docker compose up -d
```

PostgreSQL will be available at `localhost:5432`. To use it later during deployment or integration testing, set `DATABASE_URL` in `backend/.env` to a PostgreSQL URL, for example:

```env
DATABASE_URL=postgresql+psycopg2://peer_review_user:peer_review_password@localhost:5432/peer_review_db
```

### 3. Run the Frontend

Open a new terminal:

```bash
cd frontend
copy .env.example .env
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

## Environment

Backend environment variables are in `backend/.env.example`.

Frontend environment variables are in `frontend/.env.example`.

## Notes

This scaffold is designed for fast iteration during a university demo. Keep future features small and visible:

- Upload or paste paper text
- Create simulated reviewer roles
- Generate review summaries
- Compare reviewer feedback
- Show an editor decision screen
