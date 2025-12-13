from __future__ import annotations

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base  # Импортируем Base из database.py


class User(Base):
    __tablename__ = "users_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    # Используем строку "Habit", чтобы не импортировать файл habit.py и не ломать код
    habits: Mapped[List["Habit"]] = relationship(back_populates="user")
