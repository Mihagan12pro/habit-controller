from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.database import get_db
from src.services.cessation import (
    create_cessation_service,
    reset_cessation_counter,
    delete_cessation_service,
    change_cessation_status_service,
)

router = APIRouter(tags=["Cessations"])


# --- БЛОК 1: Создание ---
@router.post("/users/{user_id}/cessations", response_model=schemas.CessationOut)
async def create_cessation_endpoint(
    user_id: int,
    cessation: schemas.CessationCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_cessation_service(db, user_id, cessation)


# --- БЛОК 2: Действия ---
@router.post("/cessations/{id}/reset", response_model=schemas.CessationOut)
async def reset_cessation_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    """Я сорвался (сброс таймера)"""
    return await reset_cessation_counter(db, id)


@router.patch("/cessations/{id}/status", response_model=schemas.CessationOut)
async def update_status_endpoint(
    id: int, status_update: schemas.StatusUpdate, db: AsyncSession = Depends(get_db)
):
    """Сменить статус (например, в архив)"""
    return await change_cessation_status_service(db, id, status_update.status)


@router.delete("/cessations/{id}")
async def delete_cessation_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    """Мягкое удаление"""
    return await delete_cessation_service(db, id)
