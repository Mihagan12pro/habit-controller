import database as data_access
from repositories import habits as habits_rep
# from repositories import progress_repository as progress_rep
from repositories import progress as progress_rep
from repositories import users as users_rep

"""
Файл внедрения зависимостей
"""

database = data_access.get_db_session()  # Объект базы данных

async def get_users_repository(session: data_access.Session = data_access.get_db_session) -> users_rep.UsersRepository: 
    return users_rep.UsersRepository(session)

async def get_habits_repository(session: data_access.Session = data_access.get_db_session) ->  habits_rep.HabitsRepository: 
    return habits_rep.HabitsRepository(session)

async def get_progress_repository(session: data_access.Session = data_access.get_db_session) -> progress_rep.ProgressRepository: 
    return progress_rep.ProgressRepository(session)

