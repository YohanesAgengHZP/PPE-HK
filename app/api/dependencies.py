"""
FastAPI dependencies.
"""

from core.database import SessionLocal


def get_db():
    """Get database session."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
