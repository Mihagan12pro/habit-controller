from shared.httpExceptions import check_errors

from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.repositories.habits import HabitsRepository
from src.repositories.progress import ProgressRepository
from src.repositories.users import UsersRepository

async def track_habit_progress(
    db: AsyncSession, habit_title : str, user_id : int
):
    users_repository = UsersRepository(db)
    user_result = await users_repository.get_by_id(user_id)
    check_errors(user_result, 404)
    
    habits_repository = HabitsRepository(db)
    habit_result = await habits_repository.get_by_title(habit_title, user_id)
    check_errors(habit_result, 404)

    progress_repository = ProgressRepository(db)
    progress_result = await progress_repository.get_by_habit(habit_result)
    check_errors(progress_result, 404)

    return progress_result