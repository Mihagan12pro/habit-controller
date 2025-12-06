from .Base import Base
from .User import User
from .Progress import Progress
from __future__ import annotations
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

def start_habit():
    return "start"
def end_habit():
    return "end"
def frozen_habit():
    return "frozen"
def delete_habit():
    return "delete"


class Habit(Base):
    __tablename__ = "habits_table"
    
    tittle : Mapped[str] = mapped_column(nullable=False)

    id : Mapped[int] = mapped_column(primary_key=True)
    
    status = mapped_column(nullable=False, default=start_habit())

    user_id : Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    user : Mapped["User"] = relationship(back_populates="habits")

    progress : Mapped["Progress"] = relationship()

    