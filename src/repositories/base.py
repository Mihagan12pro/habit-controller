from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryBase:  # Базовый класс для всех репозиториев
    def __init__(self, session: AsyncSession):
        self.session = session  # Даем ссылку репозиторию на объект класса бд
