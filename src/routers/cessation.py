from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.database import get_db
from src.services.cessation import (
    create_cessation_service,
    reset_cessation_counter,
    delete_cessation_service,
    change_cessation_status_service,
    get_all_cessations_service,
    update_cessation_service,
)

router = APIRouter(tags=["Cessations"])


# --- БЛОК 1: Списки и Создание ---
@router.post("/users/{user_id}/cessations", response_model=schemas.CessationOut)
async def create_cessation_endpoint(
    user_id: int,
    cessation: schemas.CessationCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_cessation_service(db, user_id, cessation)


@router.get("/users/{user_id}/cessations", response_model=List[schemas.CessationOut])
async def get_cessations_list_endpoint(
    user_id: int,
    status: schemas.StatusUpdate = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_cessations_service(db, user_id, status)


# --- БЛОК 2: Действия ---
@router.patch("/cessations/{id}", response_model=schemas.CessationOut)
async def update_cessation_endpoint(
    id: int, updates: schemas.CessationUpdate, db: AsyncSession = Depends(get_db)
):
    """Редактировать название или статус"""
    return await update_cessation_service(db, id, updates)


@router.post("/cessations/{id}/reset", response_model=schemas.CessationOut)
async def reset_cessation_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    """Я сорвался (сброс таймера)"""
    return await reset_cessation_counter(db, id)


# @router.patch("/cessations/{id}/status", response_model=schemas.CessationOut)
# async def update_status_endpoint(
#     id: int, status_update: schemas.StatusUpdate, db: AsyncSession = Depends(get_db)
# ):
#     """Сменить статус (например, в архив)"""
#     return await change_cessation_status_service(db, id, status_update.status)


@router.delete("/cessations/{id}")
async def delete_cessation_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    """Мягкое удаление"""
    return await delete_cessation_service(db, id)
