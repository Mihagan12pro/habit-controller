from typing import Optional
from datetime import date
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.progress import Progress
from src.repositories.base import RepositoryBase


class ProgressRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_habit_id(self, habit_id: int) -> Optional[Progress]:
        """
        Получить объект прогресса по ID привычки.
        Возвращает None, если прогресс не найден.
        """
        stmt = select(Progress).where(Progress.habit_id == habit_id)
        result = await self.session.execute(stmt)

        # Используем scalar_one_or_none - он безопасен и не роняет сервер
        return result.scalar_one_or_none()

    async def create(self, habit_id: int) -> Progress:
        """Создать новую запись прогресса"""
        progress = Progress()
        progress.habit_id = habit_id

        # ВАЖНО: Приводим дату к строке, если у вас в БД поле String
        # Если в БД поле Date, то str() не нужен
        progress.start_date = date.today()

        self.session.add(progress)
        await self.session.commit()
        await self.session.refresh(progress)
        return progress

    async def delete_by_habit_id(self, habit_id: int):
        """Удалить прогресс по id привычки"""
        stmt = delete(Progress).where(Progress.habit_id == habit_id)
        await self.session.execute(stmt)
        await self.session.commit()
