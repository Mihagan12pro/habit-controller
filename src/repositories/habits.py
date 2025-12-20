from src.schemas import HabitCreate

from datetime import date

from typing import List, Optional, Union

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

    """
    Создать новую привычку
    """
    async def create(self, user_id : int, habit_dto: HabitCreate) -> Union[int, str]:
        habit = Habit()
        habit.user_id = user_id
        habit.started = date.today()
        habit.title = habit_dto.title

        if await self.get_by_title(habit.title) != None:
            return 'Привычка с данным названием уже существует!'
        
        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)
        
        return habit.id
