from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database import get_db
from src.services.habits_service import create_new_habit, get_all_habits
from src.services.progress_service import track_habit_progress

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.post("/{user_id}/habits")
async def create_habit(
    user_id: int, 
    habit: schemas.HabitCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await create_new_habit(db, user_id, habit)

@router.get('/{user_id}/all', response_model=List(schemas.HabitOut))
async def get_all_habits(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_all_habits(db, user_id)


@router.get("/track/{habit_id}")
async def track_habit(
    habit_id: int, 
    db: AsyncSession = Depends(get_db)
):
    return await track_habit_progress(db, habit_id)

#TODO: Добавить ручки для редактирования статуса и удаления привычки
