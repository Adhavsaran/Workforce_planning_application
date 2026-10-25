from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkforceHistoryBase(BaseModel):
    department_id: int
    year: int = Field(..., ge=2000)
    month: int = Field(..., ge=1, le=12)
    employee_count: int = Field(..., ge=0)
    employees_hired: int = Field(..., ge=0)
    employees_left: int = Field(..., ge=0)
    business_growth: float
    project_count: int = Field(..., ge=0)


class WorkforceHistoryCreate(WorkforceHistoryBase):
    pass


class WorkforceHistoryUpdate(BaseModel):
    department_id: int | None = None
    year: int | None = Field(default=None, ge=2000)
    month: int | None = Field(default=None, ge=1, le=12)
    employee_count: int | None = Field(default=None, ge=0)
    employees_hired: int | None = Field(default=None, ge=0)
    employees_left: int | None = Field(default=None, ge=0)
    business_growth: float | None = None
    project_count: int | None = Field(default=None, ge=0)


class WorkforceHistoryResponse(WorkforceHistoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
