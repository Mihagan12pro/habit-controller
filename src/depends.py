import database as data_access
# from repositories import progress_repository as progress_rep
from repositories import habits as habits_rep
from repositories import progress as progress_rep
from repositories import users as users_rep

"""
Файл внедрения зависимостей
"""

database = data_access.get_db()  # Объект базы данных


async def get_users_repository(
    session: data_access.Session = data_access.get_db,
) -> users_rep.UsersRepository:
    return users_rep.UsersRepository(session)


async def get_habits_repository(
    session: data_access.Session = data_access.get_db,
) -> habits_rep.HabitsRepository:
    progress_repository = await progress_rep.ProgressRepository(session)

    habits_repository = habits_rep.HabitsRepository(session)
    habits_repository.progress_repository = progress_repository

    return habits_repository


async def get_progress_repository(
    session: data_access.Session = data_access.get_db,
) -> progress_rep.ProgressRepository:
    return progress_rep.ProgressRepository(session)
