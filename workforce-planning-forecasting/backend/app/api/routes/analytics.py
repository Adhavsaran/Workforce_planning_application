from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.analytics_service import get_attrition_summary, get_dashboard_summary, get_gap_analysis, get_recommendations

router = APIRouter(tags=["Analytics"])


@router.get("/api/analytics/summary", summary="Dashboard analytics summary")
def analytics_summary(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)


@router.get("/api/workforce-gap", summary="Workforce gap analysis")
def workforce_gap(db: Session = Depends(get_db)):
    return get_gap_analysis(db)


@router.get("/api/attrition", summary="Attrition overview")
def attrition_summary(db: Session = Depends(get_db)):
    return get_attrition_summary(db)


@router.get("/api/recommendations", summary="Explainable HR recommendations")
def recommendations(db: Session = Depends(get_db)):
    return get_recommendations(db)
