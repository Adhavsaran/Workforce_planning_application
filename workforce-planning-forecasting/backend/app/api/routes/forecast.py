from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.forecast import ForecastGenerateRequest
from app.services.forecast_service import generate_all_department_forecasts, generate_department_forecast, get_department_forecast, get_forecasts

router = APIRouter(prefix="/api/forecast", tags=["Forecasting"])


@router.post(
    "",
    summary="Generate workforce forecast",
    description="Train a lightweight linear-regression model using department workforce history and generate a future staffing forecast.",
    status_code=status.HTTP_201_CREATED,
)
def create_forecast(payload: ForecastGenerateRequest, db: Session = Depends(get_db)):
    if payload.department_id is not None:
        return generate_department_forecast(db, payload.department_id, months_ahead=payload.months_ahead)
    return generate_all_department_forecasts(db, months_ahead=payload.months_ahead)


@router.get(
    "",
    summary="List forecasts",
    description="Return all saved department forecast records.",
)
def list_forecasts(db: Session = Depends(get_db)):
    return get_forecasts(db)


@router.get(
    "/{department_id}",
    summary="Get department forecast",
    description="Return the latest forecast for a specific department.",
)
def read_department_forecast(department_id: int, db: Session = Depends(get_db)):
    return get_department_forecast(db, department_id)
