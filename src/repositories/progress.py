from datetime import date

from sqlalchemy.future import select

from models import habit as h
from models import progress as p
from repositories.base import RepositoryBase


class ProgressRepository(RepositoryBase):  # Репозиторий для прогресса по привычке
    def __init__(self, session):
        super().__init__(session)

    """
    Добавить статистику по привычке. Стоит вызывать в сервисе после успешного добавления новой привычки
    """

    async def add_async(self, habit):
        start_date = date.today()

        progress = p.Progress()
        progress.habit_id = habit.habit_id
        progress.start_date = start_date

        self.session.add(progress)
        await self.session.commit()

    """
    Получить прогресс по привычке
    """

    async def get_by_habit_async(self, habit):
        progress = await self.session.execute(
            select(h.Habit).where(h.Habit.id == habit.id)
        )

        record = progress.first()
        if record is None:
            return None

        return record[0]

    async def delete_async(self, progress):
        await self.session.delete(progress)
        await self.session.commit()
