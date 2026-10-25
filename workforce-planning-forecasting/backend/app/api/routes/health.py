from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import get_db

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Check whether the API is running and the database is reachable.",
)
def health_check(db: Session = Depends(get_db)):
    settings = get_settings()
    try:
        db.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception:
        database_status = "disconnected"

    return {
        "status": "healthy" if database_status == "connected" else "degraded",
        "database": database_status,
        "environment": settings.ENVIRONMENT,
    }
