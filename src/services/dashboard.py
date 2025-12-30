from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.repositories.habits import HabitsRepository
from src.repositories.cessations import CessationsRepository


async def get_dashboard_service(db: AsyncSession, user_id: int) -> schemas.DashboardOut:
    """
    Бизнес-логика сборки Дашборда:
    1. Получает привычки и отвыкания из репозиториев.
    2. Фильтрует только активные привычки.
    3. Считает время (duration) для отвыканий.
    4. Формирует подсказки (meta).
    """
    habits_repo = HabitsRepository(db)
    cessations_repo = CessationsRepository(db)

    # 1. Загрузка данных (параллельно или последовательно)
    all_habits = await habits_repo.get_habits(user_id)
    cessations_db = await cessations_repo.get_by_user_id(user_id)

    # 2. Фильтрация активных привычек
    # Согласно твоей модели статус по умолчанию "start".
    # Добавляем сюда "started", если статус меняется на него.
    active_habits = [h for h in all_habits if h.status in ["start", "started"]]

    # 3. Обработка отвыканий (расчет времени)
    cessation_dtos = []
    now = datetime.now()

    for item in cessations_db:
        # Считаем разницу в секундах
        diff = (now - item.started_at).total_seconds()
        duration = int(diff) if diff > 0 else 0

        # Преобразуем в Pydantic-схему
        dto = schemas.CessationOut(
            id=item.id,
            title=item.title,
            started_at=item.started_at,
            user_id=item.user_id,
            duration_seconds=duration,
        )
        cessation_dtos.append(dto)

    # 4. Логика подсказок
    show_warning = len(active_habits) > 5

    # 5. Сборка итогового объекта
    return schemas.DashboardOut(
        habits=[schemas.HabitOut.model_validate(h) for h in active_habits],
        cessations=cessation_dtos,
        meta=schemas.DashboardMeta(show_overload_warning=show_warning),
    )
