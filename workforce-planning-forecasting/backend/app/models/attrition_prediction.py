from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if False:
    from app.models.employee import Employee


class AttritionPrediction(Base):
    __tablename__ = "attrition_predictions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True, nullable=False)
    prediction_date: Mapped[date] = mapped_column(Date, nullable=False)
    attrition_probability: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False, default="LOW")
    model_name: Mapped[str] = mapped_column(String(80), nullable=False, default="Logistic Regression")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    employee: Mapped["Employee"] = relationship(back_populates="attrition_predictions")
