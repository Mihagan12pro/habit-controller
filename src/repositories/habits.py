from repositories.base import RepositoryBase


class HabitsRepository(RepositoryBase):  # Репозиторий для привычек
    def __init__(self, session):
        super().__init__(session)

    async def add_async(self, habit):
        pass

    async def update_status_async(self, id, status):
        pass

    async def get_by_name_async(self, name):
        pass
