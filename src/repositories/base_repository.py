class RepositoryBase:  # Базовый класс для всех репозиториев
    def __init__(self, database):
        self._database = database  # Даем ссылку репозиторию на объект класса бд
