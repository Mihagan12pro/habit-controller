from .Base import Base
from .Habit import Habit
from __future__ import annotations
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Progress(Base):
    __tablename__ = "progress_table"

    start_date : Mapped[str] = mapped_column(nullable=False)

    habit_id : Mapped[int] = mapped_column(ForeignKey("habits_table.id"))
    habit : Mapped["Habit"] = relationship(back_populates = "progress")

    def days_passes(self):
        pass