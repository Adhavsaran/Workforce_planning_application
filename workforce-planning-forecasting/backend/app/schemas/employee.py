from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=2, max_length=150)
    department_id: int
    job_role: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    experience_years: float = Field(..., ge=0)
    joining_date: date
    salary: float = Field(..., ge=0)
    performance_score: float = Field(..., ge=0, le=100)
    satisfaction_score: float = Field(..., ge=0, le=10)
    employment_type: Literal["FULL_TIME", "PART_TIME", "CONTRACT", "INTERN"] = "FULL_TIME"
    location: str = Field(..., min_length=2, max_length=150)
    attrition_status: Literal["ACTIVE", "LEFT"] = "ACTIVE"


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    employee_id: str | None = Field(default=None, min_length=3, max_length=50)
    name: str | None = Field(default=None, min_length=2, max_length=150)
    department_id: int | None = None
    job_role: str | None = Field(default=None, min_length=2, max_length=100)
    age: int | None = Field(default=None, ge=18, le=100)
    gender: str | None = Field(default=None, min_length=1, max_length=30)
    experience_years: float | None = Field(default=None, ge=0)
    joining_date: date | None = None
    salary: float | None = Field(default=None, ge=0)
    performance_score: float | None = Field(default=None, ge=0, le=100)
    satisfaction_score: float | None = Field(default=None, ge=0, le=10)
    employment_type: Literal["FULL_TIME", "PART_TIME", "CONTRACT", "INTERN"] | None = None
    location: str | None = Field(default=None, min_length=2, max_length=150)
    attrition_status: Literal["ACTIVE", "LEFT"] | None = None


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
