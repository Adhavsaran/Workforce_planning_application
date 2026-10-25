from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.base import Base

if False:
    from app.models.employee import Employee
    from app.models.forecast import Forecast
    from app.models.recommendation import Recommendation
    from app.models.workforce_history import WorkforceHistory


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    employees: Mapped[list["Employee"]] = relationship(back_populates="department")
    workforce_history: Mapped[list["WorkforceHistory"]] = relationship(back_populates="department")
    forecasts: Mapped[list["Forecast"]] = relationship(back_populates="department")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="department")
