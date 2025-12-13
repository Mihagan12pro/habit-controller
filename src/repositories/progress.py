from repositories.base import RepositoryBase


class ProgressRepository(RepositoryBase):  # Репозиторий для прогресса по привычке
    def __init__(self, session):
        super().__init__(session)

    async def add_async(self, progress):
        pass

    async def get_by_habit_async(self, habit):
        pass

    async def update_async(self, habit):
        pass
