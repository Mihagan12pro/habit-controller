from typing import List, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.habit import Habit
from src.repositories.base import RepositoryBase
from src.schemas import HabitCreate


class HabitsRepository(RepositoryBase):  # Репозиторий для привычек
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    progress_repository = None  # Обязательно надо инициализировать поле

    async def get_by_title(self, title: str, user_id: int) -> Optional[Habit]:
        """Получить id привычки"""
        stmt = select(Habit).where(Habit.title == title)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, habit_id: int) -> Optional[Habit]:
        """Получить привычку по id"""
        stmt = select(Habit).where(Habit.id == habit_id)
        result = await self.session.execute(stmt)

        if result == None:
            return "Привычка не найдена!"

        return result.scalar_one_or_none()

    async def get_habits(self, user_id: int) -> List[Habit]:
        """Получить все привычки пользователя"""
        stmt = select(Habit).where(Habit.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, user_id: int, habit_dto: HabitCreate) -> Union[int, str]:
        """Создать новую привычку"""
        habit = Habit()
        habit.user_id = user_id
        habit.title = habit_dto.title

        if await self.get_by_title(habit.title, user_id) != None:
            return "Привычка с данным названием уже существует!"

        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)

        return habit.id

    async def delete(self, habit_id: int):
        """Удалить привычку"""
        habit = await self.get_by_id(habit_id)
        if habit == None:
            return "Привычка не найдена!"

        await self.progress_repository.delete(habit)

        await self.session.delete(habit)
        await self.session.commit()

    """
    Обновление статуса привычки
    """

    async def change_status(self, habit_id: int, new_status: str):
        habit = await self.get_by_id(habit_id)
        if habit == None:
            return "Привычка не найдена!"

        habit.status = new_status

        if new_status == habit.started:
            await self.progress_repository.create(habit)
        else:
            await self.progress_repository.delete(habit)

        await self.session.commit()
