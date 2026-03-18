"""
app/database.py

SQLAlchemy setup: engine, session factory, declarative base, and a
FastAPI dependency (get_db) that manages session lifecycle per request.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------
# pool_pre_ping ensures stale connections are detected and recycled.

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# ---------------------------------------------------------------------------
# Session factory
# ---------------------------------------------------------------------------
# autocommit=False  → transactions must be committed explicitly.
# autoflush=False   → changes are not flushed to DB until commit / explicit flush.

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# ---------------------------------------------------------------------------
# Declarative base
# ---------------------------------------------------------------------------
# All ORM models should inherit from this Base.

Base = declarative_base()

# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------


def get_db():
    """
    Yield a database session for the duration of a single request,
    then close it cleanly regardless of whether an exception occurred.

    Usage inside a route:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_db_connection() -> dict:
    """
    Execute a trivial SELECT 1 to verify the MySQL connection is live.

    Returns:
        {"status": "ok",    "database": "connected"} on success.
        {"status": "error", "detail": <message>}      on failure.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}

