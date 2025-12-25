from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.anti_habit import AntiHabit
from src.repositories.base import RepositoryBase


class AntiHabitsRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, anti_habit: AntiHabit) -> AntiHabit:
        """Создать новую анти-привычку"""
        self.session.add(anti_habit)
        await self.session.commit()
        await self.session.refresh(anti_habit)
        return anti_habit

    async def get_by_id(self, anti_habit_id: int) -> Optional[AntiHabit]:
        """Получить анти-привычку по id"""
        stmt = select(AntiHabit).where(AntiHabit.id == anti_habit_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> List[AntiHabit]:
        """Получить все анти-привычки пользователя"""
        stmt = select(AntiHabit).where(AntiHabit.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def reset_counter(self, anti_habit_id: int) -> Optional[AntiHabit]:
        """Сбросить счетчик, обновив started_at на текущее время"""
        # Сначала получаем объект
        habit = await self.get_by_id(anti_habit_id)
        if not habit:
            return None

        # Обновляем поле
        habit.started_at = datetime.now()

        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def delete(self, anti_habit_id: int) -> bool:
        """Удалить анти-привычку"""
        stmt = delete(AntiHabit).where(AntiHabit.id == anti_habit_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
