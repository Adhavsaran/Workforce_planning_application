from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if False:
    from app.models.department import Department


class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), index=True, nullable=False)
    forecast_period: Mapped[str] = mapped_column(String(50), nullable=False)
    forecasted_employee_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False, default="Linear Regression")
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    department: Mapped["Department"] = relationship(back_populates="forecasts")
