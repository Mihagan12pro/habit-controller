from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Progress(Base):
    __tablename__ = "progress_table"

    id: Mapped[int] = mapped_column(primary_key=True)  # Обязательно нужен PK
    start_date: Mapped[str] = mapped_column(nullable=False)

    habit_id: Mapped[int] = mapped_column(ForeignKey("habits_table.id"))

    habit: Mapped["Habit"] = relationship(back_populates="progress")
