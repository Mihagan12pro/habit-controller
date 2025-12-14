from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Habit(Base):
    __tablename__ = "habits_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)  # Исправил tittle на title
    status: Mapped[str] = mapped_column(default="start")

    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))

    # Связи строками, чтобы избежать ошибок
    user: Mapped["User"] = relationship(back_populates="habits")

    # Важно: Прогресса много, поэтому List
    progress: Mapped[List["Progress"]] = relationship(back_populates="habit")

    started = "started"#Привычку начали вырабатывать
    frozen = "frozen"#Привычку перестали вырабатывать
    ended = "ended"#Привычка выработана
