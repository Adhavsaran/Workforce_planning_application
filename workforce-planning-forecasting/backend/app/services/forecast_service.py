from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import HTTPException, status
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.forecast import Forecast
from app.models.workforce_history import WorkforceHistory

MODEL_ROOT = Path(__file__).resolve().parents[3] / "ml" / "trained_models"
MODEL_ROOT.mkdir(parents=True, exist_ok=True)


def _build_feature_frame(history_rows: list[WorkforceHistory]) -> pd.DataFrame:
    if not history_rows:
        return pd.DataFrame(columns=["period_index", "employees_hired", "employees_left", "business_growth", "project_count"]) 

    ordered_rows = sorted(history_rows, key=lambda row: (row.year, row.month))
    start_year = ordered_rows[0].year
    start_month = ordered_rows[0].month

    records: list[dict[str, Any]] = []
    for row in ordered_rows:
        period_index = (row.year - start_year) * 12 + (row.month - start_month) + 1
        records.append(
            {
                "period_index": period_index,
                "employees_hired": row.employees_hired,
                "employees_left": row.employees_left,
                "business_growth": float(row.business_growth),
                "project_count": row.project_count,
                "employee_count": row.employee_count,
            }
        )
    return pd.DataFrame(records)


def _train_model_for_department(history_rows: list[WorkforceHistory]) -> tuple[LinearRegression, dict[str, float], pd.DataFrame]:
    if not history_rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No historical workforce data is available for this department")

    df = _build_feature_frame(history_rows)
    feature_columns = ["period_index", "employees_hired", "employees_left", "business_growth", "project_count"]
    target_column = "employee_count"

    if df.empty or len(df) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient workforce history to train the forecasting model")

    X = df[feature_columns]
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    metrics = {
        "r2_score": float(r2_score(y_test, predictions)),
        "mae": float(mean_absolute_error(y_test, predictions)),
        "rmse": float(mean_squared_error(y_test, predictions, squared=False)),
    }
    return model, metrics, df


def _persist_model(department_id: int, model: LinearRegression, department_name: str) -> Path:
    target_path = MODEL_ROOT / f"department_{department_id}_{department_name.lower().replace(' ', '_')}_model.joblib"
    joblib.dump(model, target_path)
    return target_path


def _predict_future_headcount(model: LinearRegression, df: pd.DataFrame, months_ahead: int) -> list[int]:
    if df.empty:
        return []

    last_index = int(df["period_index"].max())
    mean_metrics = {
        "employees_hired": float(df["employees_hired"].mean()),
        "employees_left": float(df["employees_left"].mean()),
        "business_growth": float(df["business_growth"].mean()),
        "project_count": float(df["project_count"].mean()),
    }

    forecasts: list[int] = []
    for month_offset in range(1, months_ahead + 1):
        future_period = last_index + month_offset
        features = [[
            future_period,
            mean_metrics["employees_hired"],
            mean_metrics["employees_left"],
            mean_metrics["business_growth"],
            mean_metrics["project_count"],
        ]]
        prediction = model.predict(features)[0]
        forecasts.append(max(0, int(round(prediction))))
    return forecasts


def _get_department_history(db: Session, department_id: int) -> list[WorkforceHistory]:
    return db.query(WorkforceHistory).filter(WorkforceHistory.department_id == department_id).order_by(WorkforceHistory.year.asc(), WorkforceHistory.month.asc()).all()


def generate_department_forecast(db: Session, department_id: int, months_ahead: int = 6) -> dict[str, Any]:
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    if months_ahead < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="months_ahead must be at least 1")

    history_rows = _get_department_history(db, department_id)
    model, metrics, df = _train_model_for_department(history_rows)
    predicted_counts = _predict_future_headcount(model, df, months_ahead)

    if not predicted_counts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The department forecast could not be computed")

    latest_count = predicted_counts[-1]
    confidence = max(0.0, min(1.0, float(metrics["r2_score"])))
    if confidence < 0:
        confidence = 0.0

    save_path = _persist_model(department_id, model, department.name)

    db.query(Forecast).filter(Forecast.department_id == department_id).delete()
    forecast_record = Forecast(
        department_id=department_id,
        forecast_period=f"{months_ahead}-month horizon",
        forecasted_employee_count=latest_count,
        model_name="Linear Regression",
        confidence_score=confidence,
    )
    db.add(forecast_record)
    db.commit()
    db.refresh(forecast_record)

    return {
        "id": forecast_record.id,
        "department_id": department_id,
        "department_name": department.name,
        "forecast_period": forecast_record.forecast_period,
        "forecasted_employee_count": latest_count,
        "model_name": forecast_record.model_name,
        "confidence_score": round(float(forecast_record.confidence_score), 4),
        "metrics": {
            "r2_score": round(metrics["r2_score"], 4),
            "mae": round(metrics["mae"], 4),
            "rmse": round(metrics["rmse"], 4),
        },
        "months_ahead": months_ahead,
        "predicted_counts": predicted_counts,
        "model_path": str(save_path),
    }


def generate_all_department_forecasts(db: Session, months_ahead: int = 6) -> list[dict[str, Any]]:
    departments = db.query(Department).order_by(Department.name.asc()).all()
    results: list[dict[str, Any]] = []
    for department in departments:
        try:
            results.append(generate_department_forecast(db, department.id, months_ahead=months_ahead))
        except HTTPException:
            continue
    return results


def get_forecasts(db: Session) -> list[dict[str, Any]]:
    forecasts = db.query(Forecast).join(Department).order_by(Forecast.created_at.desc()).all()
    results: list[dict[str, Any]] = []
    for forecast in forecasts:
        results.append(
            {
                "id": forecast.id,
                "department_id": forecast.department_id,
                "department_name": forecast.department.name,
                "forecast_period": forecast.forecast_period,
                "forecasted_employee_count": forecast.forecasted_employee_count,
                "model_name": forecast.model_name,
                "confidence_score": round(float(forecast.confidence_score), 4),
                "created_at": forecast.created_at.isoformat(),
            }
        )
    return results


def get_department_forecast(db: Session, department_id: int) -> dict[str, Any]:
    forecast = db.query(Forecast).filter(Forecast.department_id == department_id).order_by(Forecast.created_at.desc()).first()
    if forecast is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forecast not found for this department")

    department = db.query(Department).filter(Department.id == department_id).first()
    return {
        "id": forecast.id,
        "department_id": department_id,
        "department_name": department.name if department else "Unknown",
        "forecast_period": forecast.forecast_period,
        "forecasted_employee_count": forecast.forecasted_employee_count,
        "model_name": forecast.model_name,
        "confidence_score": round(float(forecast.confidence_score), 4),
        "created_at": forecast.created_at.isoformat(),
    }
