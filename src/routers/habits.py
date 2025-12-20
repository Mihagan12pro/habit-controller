from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database import get_db
from src.services.habit_service import create_new_habit, get_user_stats, track_progress

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.post("/{user_id}/create", response_model=schemas.HabitOut)
async def create_habit(
    user_id: int, habit: schemas.HabitCreate, db: AsyncSession = Depends(get_db)
):
    return await create_new_habit(db, user_id, habit)


@router.post("/track/{habit_id}")
async def track_habit(
    habit_id: int, progress: schemas.ProgressCreate, db: AsyncSession = Depends(get_db)
):
    return await track_progress(db, habit_id, progress.date)


@router.get("/{user_id}/stats", response_model=List[schemas.StatsOut])
async def get_stats(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_stats(db, user_id)
