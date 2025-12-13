from repositories.base import RepositoryBase


class ProgressRepository(RepositoryBase):  # Репозиторий для прогресса по привычке
    def __init__(self, session):
        super().__init__(session)

    async def add_async(progress):
        pass

    async def get_by_habit_async(habit):
        pass

    async def update_async(habit):
        pass
