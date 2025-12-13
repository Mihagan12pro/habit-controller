from repositories.base_repository import RepositoryBase

class UsersRepository(RepositoryBase):#Репозиторий для юзеров
    def __init__(self, database):
        super().__init__(database)
    
    async def add_async(user):
        pass

    async def get_password(name):
        pass
