from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.cessation import Cessation
    from src.models.habit import Habit


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    habits: Mapped[List["Habit"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    cessation: Mapped[List["Cessation"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
