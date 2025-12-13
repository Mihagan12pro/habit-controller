from base_repository import RepositoryBase

class HabitsRepository(RepositoryBase):#Репозиторий для привычек
    def __init__(self, database):
        super().__init__(database)
    
    async def add_async(habit):
        pass

    async def update_status_async(status):
        pass

    async def get_by_name_async(name):
        pass