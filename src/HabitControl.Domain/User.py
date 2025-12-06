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

class User(Base):
    __tablename__ = "users_table"
    
    name : Mapped[str] = mapped_column(nullable=False)

    id: Mapped[int] = mapped_column(primary_key=True)

    hashed_password : Mapped[str] = mapped_column(nullable=False)

    email :  Mapped[str] = mapped_column(nullable=False)

    habits : Mapped[List["Habit"]] = relationship( back_populates= "user")


