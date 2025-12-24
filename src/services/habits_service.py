from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.repositories.habits import HabitsRepository
from src.repositories.users import UsersRepository
from src.schemas import HabitOut
from src.services.shared.httpExceptions import check_errors


async def create_new_habit(
    db: AsyncSession, user_id: int, habit_dto: schemas.HabitCreate
):
    users_repository = UsersRepository(db)
    user_result = await users_repository.get_by_id(user_id)
    check_errors(user_result, 404)

    habits_repository = HabitsRepository(db)
    habits_result = await habits_repository.create(user_id, habit_dto)
    check_errors(habits_result, 400)

    return habits_result


async def get_all_habits(db: AsyncSession, user_id: int):
    habits_repository = HabitsRepository(db)
    result = await habits_repository.get_habits(user_id)
    check_errors(result, 404)

    habits_out = []

    for i in result:
        habit_out = HabitOut(i.id, i.title, i.status)
        habits_out.append(habit_out)

    return habits_out


async def delete(db: AsyncSession, habit_id: int):
    habits_repository = HabitsRepository(db)
    result = await habits_repository.delete(habit_id)
    check_errors(result, 404)

    return result


async def change_status(db: AsyncSession, habit_id: int, status: str):
    habits_repository = HabitsRepository(db)
    result = await habits_repository.change_status(habit_id, status)
    check_errors(result, 404)

    return result


# async def track_progress(db: AsyncSession, habit_id: int, day: date):
#     progress_repo = ProgressRepository(db)

#     # Проверка на дубликаты
#     existing = await progress_repo.get_by_habit_id_and_date(habit_id, day)

#     if existing:
#         return {"message": "Already tracked or error"}

#     new_record = Progress(habit_id=habit_id, start_date=day)
#     await progress_repo.create(new_record)
#     return {"message": "Success", "date": day}


# async def get_user_stats(db: AsyncSession, user_id: int):
#     habits_repo = HabitsRepository(db)
#     progress_repo = ProgressRepository(db)

#     # Получаем все привычки пользователя
#     habits = await habits_repo.get_habits(user_id)

#     stats = []
#     for h in habits:
#         # Получаем прогресс по привычке
#         records = await progress_repo.get_by_habit_id(h.id)

#         # Сортируем даты
#         dates = sorted([r.start_date for r in records])

#         # Простой расчет серии (streak) - заглушка логики
#         streak = 0
#         if dates:
#             streak = 1  # Тут можно написать сложную логику проверки подряд идущих дней

#         stats.append(
#             {
#                 "habit_id": h.id,
#                 "habit_title": h.title,
#                 "total_completions": len(dates),
#                 "current_streak": streak,
#                 "dates": dates,
#             }
#         )
#     return stats
