from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routers.pdf import router as pdf_router
from app.routers.review import router as review_router
from app.services.llm_service import llm_service


settings = get_settings()
app = FastAPI(title=settings.app_name)

origins = [
    settings.frontend_origin,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def root() -> dict[str, str]:
    mode = "live" if llm_service.live_mode_enabled else "demo"
    return {"status": "ok", "service": settings.app_name, "mode": mode}


@app.get("/health")
def health() -> dict[str, str]:
    mode = "live" if llm_service.live_mode_enabled else "demo"
    return {"status": "ok", "service": settings.app_name, "mode": mode}


app.include_router(review_router)
app.include_router(pdf_router)
