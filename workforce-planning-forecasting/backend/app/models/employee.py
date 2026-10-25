from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if False:
    from app.models.attrition_prediction import AttritionPrediction
    from app.models.department import Department


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), index=True, nullable=False)
    job_role: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(30), nullable=False)
    experience_years: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    joining_date: Mapped[date] = mapped_column(Date, nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    performance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    satisfaction_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    employment_type: Mapped[str] = mapped_column(String(30), nullable=False, default="FULL_TIME")
    location: Mapped[str] = mapped_column(String(150), nullable=False, default="Unknown")
    attrition_status: Mapped[str] = mapped_column(String(30), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    department: Mapped["Department"] = relationship(back_populates="employees")
    attrition_predictions: Mapped[list["AttritionPrediction"]] = relationship(back_populates="employee")
