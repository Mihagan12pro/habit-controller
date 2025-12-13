from sqlalchemy import select
from sqlalchemy.orm import Session

from src import schemas
from src.models.habit import Habit
from src.models.Progress import Progress


def create_new_habit(db: Session, user_id: int, habit_dto: schemas.HabitCreate):
    new_habit = Habit(title=habit_dto.title, user_id=user_id)
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit


def track_progress(db: Session, habit_id: int, date: str):
    # Проверка на дубликаты
    stmt = select(Progress).where(
        Progress.habit_id == habit_id, Progress.start_date == date
    )
    existing = db.execute(stmt).scalar_one_or_none()

    if existing:
        return None  # Уже отмечено

    new_record = Progress(habit_id=habit_id, start_date=date)
    db.add(new_record)
    db.commit()
    return new_record


def get_user_stats(db: Session, user_id: int):
    # 1. Получаем все привычки
    stmt = select(Habit).where(Habit.user_id == user_id)
    habits = db.execute(stmt).scalars().all()

    stats = []
    for h in habits:
        # 2. Получаем прогресс
        p_stmt = select(Progress).where(Progress.habit_id == h.id)
        records = db.execute(p_stmt).scalars().all()

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
