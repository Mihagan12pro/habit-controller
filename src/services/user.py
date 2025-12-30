from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.repositories.users import UsersRepository

async def create_user(
    db: AsyncSession, user_dto: schemas.UserCreate
):
    users_repo = UsersRepository(db)
    result = await users_repo.create(user_dto)
    check_errors(result, 409)

    return result


async def get_user_by_id(db: AsyncSession, user_id: int):
    users_repo = UsersRepository(db)
    result = await users_repo.get_by_id(user_id)
    check_errors(result, 404)

    return result


async def get_user_by_email(db: AsyncSession, email: str):
    users_repo = UsersRepository(db)
    result = await users_repo.get_by_email(email)
    check_errors(result, 404)

    return result
