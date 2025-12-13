from base_repository import RepositoryBase


class ProgressRepository(RepositoryBase):  # Репозиторий для прогресса по привычке
    def __init__(self, database):
        super().__init__(database)

    async def add_async(progress):
        pass

    async def get_by_habit_async(habit):
        pass

    async def update_async(habit):
        pass
