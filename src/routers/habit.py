from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.database import get_db
from src.services.habit import (
    create_new_habit,
    change_habit_status_service,
    delete_habit_service,
    get_all_habits_service,
    get_habit_details_service,
    update_habit_service,
)
from src.services.progress import track_habit_progress

router = APIRouter(tags=["Habits"])

# --- БЛОК 1: Списки и Создание (Привязано к Юзеру) ---


@router.post("/users/{user_id}/habits", response_model=schemas.HabitOut)
async def create_habit_endpoint(
    user_id: int, habit: schemas.HabitCreate, db: AsyncSession = Depends(get_db)
):
    return await create_new_habit(db, user_id, habit)


@router.get("/users/{user_id}/habits", response_model=List[schemas.HabitOut])
async def get_habits_list_endpoint(
    user_id: int,
    # Фильтр: ?status=archived. Если пусто - вернет все (кроме удаленных)
    status: schemas.StatusUpdate = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_habits_service(db, user_id, status)


# --- БЛОК 2: Действия с Привычкой ---


@router.get("/habits/{habit_id}", response_model=schemas.HabitOut)
async def get_habit_details_endpoint(habit_id: int, db: AsyncSession = Depends(get_db)):
    """Получить детали одной привычки"""
    return await get_habit_details_service(db, habit_id)


@router.patch("/habits/{habit_id}", response_model=schemas.HabitOut)
async def update_habit_endpoint(
    habit_id: int,
    updates: schemas.HabitUpdate,  # JSON Body: { "title": "...", "status": "..." }
    db: AsyncSession = Depends(get_db),
):
    """Редактировать название или статус"""
    return await update_habit_service(db, habit_id, updates)


@router.post("/habits/{habit_id}/track")
async def track_habit_endpoint(habit_id: int, db: AsyncSession = Depends(get_db)):
    return await track_habit_progress(db, habit_id)


# # Оставил старый эндпоинт для совместимости, но PATCH /{id} выше его заменяет
# @router.patch("/habits/{habit_id}/status", response_model=schemas.HabitOut)
# async def update_status_endpoint(
#     habit_id: int,
#     status_update: schemas.StatusUpdate,
#     db: AsyncSession = Depends(get_db),
# ):
#     """Сменить статус (active, archived, deleted)"""
#     return await change_habit_status_service(db, habit_id, status_update.status)


@router.delete("/habits/{habit_id}")
async def delete_habit_endpoint(habit_id: int, db: AsyncSession = Depends(get_db)):
    """Мягкое удаление (перенос в статус deleted)"""
    return await delete_habit_service(db, habit_id)
