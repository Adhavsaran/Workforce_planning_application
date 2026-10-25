from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AttritionPredictionBase(BaseModel):
    employee_id: int
    prediction_date: date
    attrition_probability: float = Field(..., ge=0, le=1)
    risk_level: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    model_name: str = Field(..., min_length=2, max_length=80)


class AttritionPredictionCreate(AttritionPredictionBase):
    pass


class AttritionPredictionUpdate(BaseModel):
    employee_id: int | None = None
    prediction_date: date | None = None
    attrition_probability: float | None = Field(default=None, ge=0, le=1)
    risk_level: Literal["LOW", "MEDIUM", "HIGH"] | None = None
    model_name: str | None = Field(default=None, min_length=2, max_length=80)


class AttritionPredictionResponse(AttritionPredictionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
