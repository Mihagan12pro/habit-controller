class RepositoryBase:  # Базовый класс для всех репозиториев
    def __init__(self, session):
        self._database = session  # Даем ссылку репозиторию на объект класса бд
