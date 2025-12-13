import database as data_access
from repositories import habits_repository as habits_rep
from repositories import progress_repository as progress_rep
from repositories import users_repository as users_rep

"""
Файл внедрения зависимостей
"""

database = data_access.get_db()  # Объект базы данных

users_repository = users_rep.UsersRepository(database=database)
habits_repository = habits_rep.HabitsRepository(database=database)
progress_repository = progress_rep.ProgressRepository(database=database)
