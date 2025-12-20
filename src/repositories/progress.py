from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.progress import Progress
from src.repositories.base import RepositoryBase


class ProgressRepository(RepositoryBase):  # Репозиторий для прогресса по привычке
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_habit_id(self, habit_id: int) -> List[Progress]:
        """Получить весь прогресс по привычке"""
        stmt = select(Progress).where(Progress.habit_id == habit_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_habit_id_and_date(self, habit_id: int, day: date) -> Optional[Progress]:
        """Получить прогресс по привычке и дате"""
        stmt = select(Progress).where(
            Progress.habit_id == habit_id, Progress.start_date == day
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, progress: Progress) -> Progress:
        """Создать новую запись прогресса"""
        self.session.add(progress)
        await self.session.commit()
        await self.session.refresh(progress)
        return progress
