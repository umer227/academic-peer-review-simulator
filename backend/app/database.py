from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings


settings = get_settings()
database_url = settings.resolved_database_url
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

engine = create_engine(database_url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DATABASE_AVAILABLE = True


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    global DATABASE_AVAILABLE
    from app import models

    try:
        Base.metadata.create_all(bind=engine)
        _ensure_optional_columns()
        DATABASE_AVAILABLE = True
    except SQLAlchemyError:
        DATABASE_AVAILABLE = False


def _ensure_optional_columns() -> None:
    inspector = inspect(engine)
    if "paper_reviews" not in inspector.get_table_names():
        return

    existing = {column["name"] for column in inspector.get_columns("paper_reviews")}
    optional_columns = {
        "decision_reason": "TEXT DEFAULT ''",
    }

    with engine.begin() as connection:
        for column_name, column_type in optional_columns.items():
            if column_name not in existing:
                connection.execute(text(f"ALTER TABLE paper_reviews ADD COLUMN {column_name} {column_type}"))
