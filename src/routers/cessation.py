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

router = APIRouter(tags=["Cessations"])


@router.post("/users/{user_id}/cessation", response_model=schemas.CessationOut)
async def introduce_cessation(
    user_id: int,
    anti_habit: schemas.CessationCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new anti-habit"""
    return await create_cessation(db, user_id, anti_habit)


# @router.get("/{user_id}", response_model=List[schemas.CessationOut])
# async def show_cessations(
#     user_id: int, db: AsyncSession = Depends(get_db)
# ):
#     """Get all anti-habits for a user"""
#     return await get_all_cessations(db, user_id)


@router.post("/cessations/{id}/reset", response_model=schemas.CessationOut)
async def start_over_cessation(id: int, db: AsyncSession = Depends(get_db)):
    """Reset the counter for an anti-habit"""
    return await reset_cessation_counter(db, id)
