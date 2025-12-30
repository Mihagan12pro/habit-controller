from datetime import datetime, date
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.habits import HabitsRepository
from src.repositories.progress import ProgressRepository
from src.schemas import ProgressOut  


async def track_habit_progress(db: AsyncSession, habit_id: int):
    # 1. Проверяем, существует ли привычка
    habits_repo = HabitsRepository(db)
    # Предполагаем, что get_by_id возвращает объект или None
    habit = await habits_repo.get_by_id(
        habit_id
    )
    if habit is None:
        raise HTTPException(status_code=404, detail="Привычка не найдена")

    # 2. Ищем прогресс
    progress_repo = ProgressRepository(db)
    progress = await progress_repo.get_by_habit_id(habit_id)

    # 3. Логика: Если прогресса НЕТ, значит пользователь трекает привычку первый раз
    if progress is None:
        # Вариант А: Создать прогресс автоматически (начало отсчета - сегодня)
        progress = await progress_repo.create(habit_id)
        # Так как создали сегодня, прошло времени: 0 дней
        return ProgressOut(time_passed="0 days, 0:00:00")

        # Вариант Б: Вернуть ошибку 404 (если вы хотите, чтобы прогресс создавался отдельно)
        # raise HTTPException(status_code=404, detail="Прогресс для этой привычки не начат")

    # 4. Если прогресс ЕСТЬ, считаем разницу
    # Учитываем, что start_date в базе может быть строкой
    if isinstance(progress.start_date, str):
        date_start = datetime.strptime(progress.start_date, "%Y-%m-%d").date()
    else:
        # Если в базе тип Date, то strptime не нужен
        date_start = progress.start_date

    now = date.today()
    delta = now - date_start

    # 5. Возвращаем Pydantic схему
    return ProgressOut(time_passed=str(delta))
