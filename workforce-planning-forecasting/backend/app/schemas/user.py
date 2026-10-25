from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: Literal["HR_ADMIN", "HR_MANAGER"] = "HR_MANAGER"


class UserCreate(UserBase):
    password_hash: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    email: EmailStr | None = None
    role: Literal["HR_ADMIN", "HR_MANAGER"] | None = None
    is_active: bool | None = None
    password_hash: str | None = Field(default=None, min_length=8)


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
