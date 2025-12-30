from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.database import get_db
from src.services.habit import (
    create_new_habit,
    change_habit_status_service,
    delete_habit_service,
)
from src.services.progress import track_habit_progress

router = APIRouter(tags=["Habits"])


# --- БЛОК 1: Создание (через Юзера) ---
@router.post("/users/{user_id}/habits", response_model=schemas.HabitOut)
async def create_habit_endpoint(
    user_id: int, habit: schemas.HabitCreate, db: AsyncSession = Depends(get_db)
):
    return await create_new_habit(db, user_id, habit)


# --- БЛОК 2: Действия с Привычкой ---
@router.post("/habits/{habit_id}/track")
async def track_habit_endpoint(habit_id: int, db: AsyncSession = Depends(get_db)):
    return await track_habit_progress(db, habit_id)


@router.patch("/habits/{habit_id}/status", response_model=schemas.HabitOut)
async def update_status_endpoint(
    habit_id: int,
    status_update: schemas.StatusUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Сменить статус (active, archived, deleted)"""
    return await change_habit_status_service(db, habit_id, status_update.status)


@router.delete("/habits/{habit_id}")
async def delete_habit_endpoint(habit_id: int, db: AsyncSession = Depends(get_db)):
    """Мягкое удаление (перенос в статус deleted)"""
    return await delete_habit_service(db, habit_id)
