from datetime import date
import datetime

from typing import Union

from src.schemas import ProgressOut

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
    async def get_by_habit(self, habit: Habit) -> Union[Progress, str]:
        stmt = select(Progress).where(Progress.habit_id == habit.id)
        result = await self.session.execute(stmt)

        if result == None:
            return "Привычка не найдена!"
        
        date_start = datetime.strptime(result.scalar_one().start_date, '%Y-%m-%d').date()
        now = date.today()

        progress_result = ProgressOut(str(now - date_start))

        return progress_result

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
    
        
    """
    Удалить прогресс. 
    Метод вызывается, когда статус 
    привычки меняется на 'выработана'/'заморожена' 
    или привычка удаляется
    """
    async def delete(self, habit : Habit):
        habit_id = habit.id

        progress_result = await self.get_by_id(habit)

        if isinstance(progress_result, str):
            return progress_result

        await self.session.delete(progress_result)
        await self.session.commit()
    
    

