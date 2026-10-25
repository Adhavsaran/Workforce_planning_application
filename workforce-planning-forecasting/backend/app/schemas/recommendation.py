from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RecommendationBase(BaseModel):
    department_id: int | None = None
    recommendation_type: Literal["HIRE", "NO_HIRING", "RESKILL", "INTERNAL_TRANSFER", "MONITOR"] = "HIRE"
    recommendation_text: str = Field(..., min_length=5, max_length=500)
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    recommended_employee_count: int = Field(..., ge=0)


class RecommendationCreate(RecommendationBase):
    pass


class RecommendationUpdate(BaseModel):
    department_id: int | None = None
    recommendation_type: Literal["HIRE", "NO_HIRING", "RESKILL", "INTERNAL_TRANSFER", "MONITOR"] | None = None
    recommendation_text: str | None = Field(default=None, min_length=5, max_length=500)
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None
    recommended_employee_count: int | None = Field(default=None, ge=0)


class RecommendationResponse(RecommendationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
