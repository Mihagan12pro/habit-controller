from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.anti_habit import AntiHabit
from src.repositories.base import RepositoryBase


class AntiHabitsRepository(RepositoryBase):  # Репозиторий для анти-привычек
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, anti_habit: AntiHabit) -> AntiHabit:
        """Создать новую анти-привычку"""
        pass

    async def get_by_id(self, anti_habit_id: int) -> Optional[AntiHabit]:
        """Получить анти-привычку по id"""
        pass

    async def get_by_user_id(self, user_id: int) -> List[AntiHabit]:
        """Получить все анти-привычки пользователя"""
        pass

    async def reset_counter(self, anti_habit_id: int) -> Optional[AntiHabit]:
        """Сбросить счетчик, обновив started_at на текущее время"""
        pass

    async def delete(self, anti_habit_id: int) -> bool:
        """Удалить анти-привычку"""
        pass
