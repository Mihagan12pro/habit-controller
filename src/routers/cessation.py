from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database import get_db
from src.services.cessation import (
    create_cessation,
    get_all_cessations,
    reset_cessation_counter,
)

router = APIRouter(prefix="/cessations", tags=["Cessations"])


@router.post("/{user_id}/create", response_model=schemas.CessationOut)
async def create_anti_habit_endpoint(
    user_id: int,
    anti_habit: schemas.CessationCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new anti-habit"""
    return await create_cessation(db, user_id, anti_habit)


@router.get("/{user_id}", response_model=List[schemas.CessationOut])
async def get_all_anti_habits_endpoint(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    """Get all anti-habits for a user"""
    return await get_all_cessations(db, user_id)


@router.post("/{id}/reset", response_model=schemas.CessationOut)
async def reset_anti_habit_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    """Reset the counter for an anti-habit"""
    return await reset_cessation_counter(db, id)
