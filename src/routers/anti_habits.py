from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database import get_db
from src.services.anti_habit_service import (
    create_anti_habit,
    get_all_anti_habits,
    reset_anti_habit_counter,
)

router = APIRouter(prefix="/anti-habits", tags=["Anti-Habits"])


@router.post("/{user_id}/create", response_model=schemas.AntiHabitOut)
async def create_anti_habit_endpoint(
    user_id: int,
    anti_habit: schemas.AntiHabitCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new anti-habit"""
    return await create_anti_habit(db, user_id, anti_habit)


@router.get("/{user_id}", response_model=List[schemas.AntiHabitOut])
async def get_all_anti_habits_endpoint(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    """Get all anti-habits for a user"""
    return await get_all_anti_habits(db, user_id)


@router.post("/{id}/reset", response_model=schemas.AntiHabitOut)
async def reset_anti_habit_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    """Reset the counter for an anti-habit"""
    return await reset_anti_habit_counter(db, id)
