from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.habit import Habit
from src.repositories.base import RepositoryBase


class HabitsRepository(RepositoryBase):  # Репозиторий для привычек
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_title(self, title: str) -> Optional[Habit]:
        """Получить привычку по названию"""
        stmt = select(Habit).where(Habit.title == title)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, habit_id: int) -> Optional[Habit]:
        """Получить привычку по id"""
        stmt = select(Habit).where(Habit.id == habit_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> List[Habit]:
        """Получить все привычки пользователя"""
        stmt = select(Habit).where(Habit.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, habit: Habit) -> Habit:
        """Создать новую привычку"""
        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)
        return habit
