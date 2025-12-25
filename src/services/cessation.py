from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.models.cessation import Cessation
from src.repositories.cessations import CessationsRepository
from src.repositories.users import UsersRepository


async def create_cessation(
    db: AsyncSession, user_id: int, cessation_dto: schemas.CessationCreate
):
    """Create a new anti-habit with started_at set to current time"""
    users_repo = UsersRepository(db)
    cessations_repo = CessationsRepository(db)

    # Проверяем, существует ли пользователь
    user = await users_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_cessation = Cessation(
        title=cessation_dto.title, user_id=user_id, started_at=datetime.now()
    )

    try:
        created = await cessations_repo.create(new_cessation)
        # Calculate duration for response
        duration_seconds = int((datetime.now() - created.started_at).total_seconds())
        return {
            "id": created.id,
            "title": created.title,
            "started_at": created.started_at,
            "user_id": created.user_id,
            "duration_seconds": duration_seconds,
        }
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create anti-habit")


async def get_all_cessations(db: AsyncSession, user_id: int):
    """Get all anti-habits for a user with calculated duration"""
    cessations_repo = CessationsRepository(db)

    cessations = await cessations_repo.get_by_user_id(user_id)

    now = datetime.now()
    result = []
    for ah in cessations:
        duration_seconds = int((now - ah.started_at).total_seconds())
        result.append(
            {
                "id": ah.id,
                "title": ah.title,
                "started_at": ah.started_at,
                "user_id": ah.user_id,
                "duration_seconds": duration_seconds,
            }
        )

    return result


async def reset_cessation_counter(db: AsyncSession, cessation_id: int):
    """Reset the counter by updating started_at to current time"""
    cessations_repo = CessationsRepository(db)

    updated = await cessations_repo.reset_counter(cessation_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Anti-habit not found")

    # Calculate duration for response (should be 0 or very small)
    duration_seconds = int((datetime.now() - updated.started_at).total_seconds())
    return {
        "id": updated.id,
        "title": updated.title,
        "started_at": updated.started_at,
        "user_id": updated.user_id,
        "duration_seconds": duration_seconds,
    }
