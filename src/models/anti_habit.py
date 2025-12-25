from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class AntiHabit(Base):
    __tablename__ = "anti_habits_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    pass
