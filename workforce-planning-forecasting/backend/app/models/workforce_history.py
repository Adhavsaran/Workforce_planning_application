from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if False:
    from app.models.department import Department


class WorkforceHistory(Base):
    __tablename__ = "workforce_history"
    __table_args__ = (
        UniqueConstraint("department_id", "year", "month", name="uq_workforce_history_department_year_month"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), index=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    employee_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    employees_hired: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    employees_left: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    business_growth: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    project_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    department: Mapped["Department"] = relationship(back_populates="workforce_history")
