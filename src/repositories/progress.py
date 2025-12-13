from repositories.base import RepositoryBase
from models import progress as p
from models import habit as h
from sqlalchemy.future import select
import datetime


class ProgressRepository(RepositoryBase):  # Репозиторий для прогресса по привычке
    def __init__(self, session):
        super().__init__(session)
    
    """
    Добавить статистику по привычке. Стоит вызывать в сервисе после успешного добавления новой привычки
    """
    async def add_async(self, habit):
        errors = []#Массив ошибок

        start_date = datetime.datetime.now()

        progress = p.Progress()
        progress.habit_id = habit.habit_id
        progress.start_date = start_date

        self.session.add(progress)
        await self.session.commit()

    """
    Получить прогресс по привычке
    """
    async def get_by_habit_async(self, habit):
        errors = []#Массив ошибок

        progress = await self.session.execute(select(h.Habit).filter_by(h.Habit.id == habit.id)).first()

        if progress == None:
            errors.append("Привычка не найдена!")
            return errors
        
        return progress

    async def delete_async(self, progress):
        await self.session.delete(progress)
        await self.session.commit()
