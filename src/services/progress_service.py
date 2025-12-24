from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.habits import HabitsRepository
from src.repositories.progress import ProgressRepository
from src.services.shared.httpExceptions import check_errors


async def track_habit_progress(db: AsyncSession, habit_id: int):
    habits_repository = HabitsRepository(db)
    habit_result = await habits_repository.get_by_id(habit_id)
    check_errors(habit_result, 404)

    progress_repository = ProgressRepository(db)
    progress_result = await progress_repository.get_by_habit(habit_result)
    check_errors(progress_result, 404)

    return progress_result
