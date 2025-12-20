from datetime import date
from typing import List, Optional, Union

from src.models.habit import Habit

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.progress import Progress
from src.repositories.base import RepositoryBase


class ProgressRepository(RepositoryBase):  # Репозиторий для прогресса по привычке
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    """
    Получить прогресс по id привычки
    """
    async def get_by_habit_id(self, habit_id: int) -> Union[Progress, str]:
        stmt = select(Progress).where(Progress.habit_id == habit_id)
        result = await self.session.execute(stmt)

        if result == None:
            return "Прогресс по привычке не был найден!"

        return result.scalar_one()

    """
    Создать новую запись прогресса
    """
    async def create(self, habit: Habit) -> int:

        progress = Progress()
        progress.habit_id = habit.id
        progress.start_date = date.today()

        self.session.add(progress)
        await self.session.commit()
        await self.session.refresh(progress)
        return progress
