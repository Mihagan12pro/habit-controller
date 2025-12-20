from typing import Union

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.models.user import User
from src.repositories.users import UsersRepository


async def create_user(db: AsyncSession, user_dto: schemas.UserCreate) -> Union[int, str]:
    users_repo = UsersRepository(db)
    result = await users_repo.create(user_dto)
    return result


async def get_user_by_id(db: AsyncSession, user_id: int):
    users_repo = UsersRepository(db)
    return await users_repo.get_by_id(user_id)


async def get_user_by_email(db: AsyncSession, email: str):
    users_repo = UsersRepository(db)
    return await users_repo.get_by_email(email)
