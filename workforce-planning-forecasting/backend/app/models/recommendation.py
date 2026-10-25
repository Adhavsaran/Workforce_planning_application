from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if False:
    from app.models.department import Department


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), index=True, nullable=True)
    recommendation_type: Mapped[str] = mapped_column(String(40), nullable=False, default="HIRE")
    recommendation_text: Mapped[str] = mapped_column(String(500), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIUM")
    recommended_employee_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    department: Mapped["Department"] = relationship(back_populates="recommendations")
