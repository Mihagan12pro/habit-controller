from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.habit import Habit
from src.repositories.base import RepositoryBase
from src.schemas import HabitCreate


class HabitsRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_title(self, title: str, user_id: int) -> Optional[Habit]:
        stmt = select(Habit).where(
            Habit.title == title,
            Habit.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, habit_id: int) -> Optional[Habit]:
        stmt = select(Habit).where(Habit.id == habit_id)
        result = await self.session.execute(stmt)
        # ИСПРАВЛЕНО: Возвращаем None, а не строку, чтобы сервис мог выкинуть 404
        return result.scalar_one_or_none()

    async def get_habits(self, user_id: int, status: str = None) -> List[Habit]:
        """
        Получить привычки.
        Если передан status (например, 'active'), фильтруем по нему.
        """
        stmt = select(Habit).where(Habit.user_id == user_id)

        if status:
            stmt = stmt.where(Habit.status == status)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, user_id: int, habit_dto: HabitCreate) -> Optional[Habit]:
        if await self.get_by_title(habit_dto.title, user_id) is not None:
            return None

        habit = Habit()
        habit.user_id = user_id
        habit.title = habit_dto.title
        # Если в DTO есть статус, используем его, иначе дефолтный из модели
        if hasattr(habit_dto, "status"):
            habit.status = habit_dto.status

        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def delete(self, habit_id: int):
        habit = await self.get_by_id(habit_id)
        if habit is None:
            return None  # Или вызывать ошибку в сервисе

        await self.session.delete(habit)
        await self.session.commit()
        return True

    async def change_status(self, habit_id: int, new_status: str):
        habit = await self.get_by_id(habit_id)
        if habit is None:
            return None

        habit.status = new_status
        await self.session.commit()
        return habit
