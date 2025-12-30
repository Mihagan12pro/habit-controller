from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.repositories.cessations import CessationsRepository  # проверь имя файла
from src.repositories.users import UsersRepository


async def create_cessation_service(
    db: AsyncSession, user_id: int, cessation_dto: schemas.CessationCreate
):
    users_repo = UsersRepository(db)
    cessations_repo = CessationsRepository(db)

    user = await users_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    created = await cessations_repo.create(user_id, cessation_dto)

    duration = int((datetime.now() - created.started_at).total_seconds())

    return schemas.CessationOut(
        id=created.id,
        title=created.title,
        started_at=created.started_at,
        user_id=created.user_id,
        status=created.status,
        duration_seconds=duration,
    )


async def get_all_cessations_service(
    db: AsyncSession, user_id: int, status: Optional[str] = None
):
    repo = CessationsRepository(db)
    cessations = await repo.get_by_user_id(user_id, status=status)

    now = datetime.now()
    results = []
    for c in cessations:
        duration = int((now - c.started_at).total_seconds())
        results.append(
            schemas.CessationOut(
                id=c.id,
                title=c.title,
                started_at=c.started_at,
                user_id=c.user_id,
                status=c.status,
                duration_seconds=duration,
            )
        )
    return results


async def update_cessation_service(
    db: AsyncSession, cessation_id: int, updates: schemas.CessationUpdate
):
    repo = CessationsRepository(db)
    updated = await repo.update(
        cessation_id, title=updates.title, status=updates.status
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Cessation not found")

    duration = int((datetime.now() - updated.started_at).total_seconds())
    return schemas.CessationOut(
        id=updated.id,
        title=updated.title,
        started_at=updated.started_at,
        user_id=updated.user_id,
        status=updated.status,
        duration_seconds=duration,
    )


async def change_cessation_status_service(
    db: AsyncSession, cessation_id: int, status: str
):
    repo = CessationsRepository(db)
    updated = await repo.change_status(cessation_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Cessation not found")

    duration = int((datetime.now() - updated.started_at).total_seconds())
    return schemas.CessationOut(
        id=updated.id,
        title=updated.title,
        started_at=updated.started_at,
        user_id=updated.user_id,
        status=updated.status,
        duration_seconds=duration,
    )


async def delete_cessation_service(db: AsyncSession, cessation_id: int):
    repo = CessationsRepository(db)
    # Используем мягкое удаление из репозитория
    deleted = await repo.delete(cessation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cessation not found")
    return {"message": "Cessation deleted"}


async def reset_cessation_counter(db: AsyncSession, cessation_id: int):
    repo = CessationsRepository(db)
    updated = await repo.reset_counter(cessation_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Anti-habit not found")

    return schemas.CessationOut(
        id=updated.id,
        title=updated.title,
        started_at=updated.started_at,
        user_id=updated.user_id,
        status=updated.status,
        duration_seconds=0,
    )
