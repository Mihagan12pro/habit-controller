from datetime import datetime
from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.cessation import Cessation
from src.repositories.base import RepositoryBase


class CessationsRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, cessation: Cessation) -> Cessation:
        """Создать новую анти-привычку"""
        self.session.add(cessation)
        await self.session.commit()
        await self.session.refresh(cessation)
        return cessation

    async def get_by_id(self, cessation_id: int) -> Optional[Cessation]:
        """Получить анти-привычку по id"""
        stmt = select(Cessation).where(Cessation.id == cessation_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> List[Cessation]:
        """Получить все анти-привычки пользователя"""
        stmt = select(Cessation).where(Cessation.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def reset_counter(self, cessation_id: int) -> Optional[Cessation]:
        """Сбросить счетчик, обновив started_at на текущее время"""
        # Сначала получаем объект
        habit = await self.get_by_id(cessation_id)
        if not habit:
            return None

        # Обновляем поле
        habit.started_at = datetime.now()

        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def delete(self, cessation_id: int) -> bool:
        """Удалить анти-привычку"""
        stmt = delete(Cessation).where(Cessation.id == cessation_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
