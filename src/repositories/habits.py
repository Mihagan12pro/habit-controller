from repositories.base import RepositoryBase


class HabitsRepository(RepositoryBase):  # Репозиторий для привычек
    def __init__(self, session):
        super().__init__(session)

    async def add_async(habit):
        pass

    async def update_status_async(status):
        pass

    async def get_by_name_async(name):
        pass
