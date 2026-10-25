from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ForecastBase(BaseModel):
    department_id: int
    forecast_period: str = Field(..., min_length=1, max_length=50)
    forecasted_employee_count: int = Field(..., ge=0)
    model_name: str = Field(..., min_length=2, max_length=100)
    confidence_score: float = Field(..., ge=0, le=1)


class ForecastGenerateRequest(BaseModel):
    department_id: int | None = None
    months_ahead: int = Field(default=6, ge=1, le=24)


class ForecastCreate(ForecastBase):
    pass


class ForecastUpdate(BaseModel):
    department_id: int | None = None
    forecast_period: str | None = Field(default=None, min_length=1, max_length=50)
    forecasted_employee_count: int | None = Field(default=None, ge=0)
    model_name: str | None = Field(default=None, min_length=2, max_length=100)
    confidence_score: float | None = Field(default=None, ge=0, le=1)


class ForecastResponse(ForecastBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
