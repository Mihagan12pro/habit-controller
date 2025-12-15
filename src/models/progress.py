from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.habit import Habit  # pragma: no cover


class Progress(Base):
    __tablename__ = "progress_table"

    id: Mapped[int] = mapped_column(primary_key=True)  # Обязательно нужен PK
    # Храним календарную дату (без времени)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    habit_id: Mapped[int] = mapped_column(ForeignKey("habits_table.id"))

    habit: Mapped["Habit"] = relationship(back_populates="progress")
