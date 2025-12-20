from datetime import date

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.models.habit import Habit
from src.models.progress import Progress
from src.repositories.habits import HabitsRepository
from src.repositories.progress import ProgressRepository
from src.repositories.users import UsersRepository


async def create_new_habit(
    db: AsyncSession, user_id: int, habit_dto: schemas.HabitCreate
):
    users_repo = UsersRepository(db)
    habits_repo = HabitsRepository(db)

    # Проверяем, существует ли пользователь
    user = await users_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Проверяем, существует ли уже привычка с таким названием
    existing_habit = await habits_repo.get_by_title(habit_dto.title)
    if existing_habit:
        raise HTTPException(
            status_code=400, detail="Habit with this title already exists"
        )

    new_habit = Habit(title=habit_dto.title, user_id=user_id)

    try:
        return await habits_repo.create(new_habit)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Habit with this title already exists"
        )


async def track_progress(db: AsyncSession, habit_id: int, day: date):
    progress_repo = ProgressRepository(db)

    # Проверка на дубликаты
    existing = await progress_repo.get_by_habit_id_and_date(habit_id, day)

    if existing:
        return {"message": "Already tracked or error"}

    new_record = Progress(habit_id=habit_id, start_date=day)
    await progress_repo.create(new_record)
    return {"message": "Success", "date": day}


async def get_user_stats(db: AsyncSession, user_id: int):
    habits_repo = HabitsRepository(db)
    progress_repo = ProgressRepository(db)

    # Получаем все привычки пользователя
    habits = await habits_repo.get_by_user_id(user_id)

    stats = []
    for h in habits:
        # Получаем прогресс по привычке
        records = await progress_repo.get_by_habit_id(h.id)

        # Сортируем даты
        dates = sorted([r.start_date for r in records])

        # Простой расчет серии (streak) - заглушка логики
        streak = 0
        if dates:
            streak = 1  # Тут можно написать сложную логику проверки подряд идущих дней

        stats.append(
            {
                "habit_id": h.id,
                "habit_title": h.title,
                "total_completions": len(dates),
                "current_streak": streak,
                "dates": dates,
            }
        )
    return stats
