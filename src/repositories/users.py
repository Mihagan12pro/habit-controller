from repositories.base import RepositoryBase


class UsersRepository(RepositoryBase):  # Репозиторий для юзеров
    def __init__(self, session):
        super().__init__(session)

    async def add_async(user):
        pass

        

    async def get_password(name):
        pass
