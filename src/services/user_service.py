from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.models.user import User
from src.repositories.users import UsersRepository


async def create_user(db: AsyncSession, user_dto: schemas.UserCreate):
    users_repo = UsersRepository(db)
    
    # Проверяем, занят ли email
    existing_user = await users_repo.get_by_email(user_dto.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Тут можно добавить хеширование пароля
    fake_hashed_pw = user_dto.password + "notreallyhashed"

    new_user = User(
        name=user_dto.name, email=user_dto.email, hashed_password=fake_hashed_pw
    )
    
    try:
        return await users_repo.create(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")


async def get_user_by_id(db: AsyncSession, user_id: int):
    users_repo = UsersRepository(db)
    return await users_repo.get_by_id(user_id)


async def get_user_by_email(db: AsyncSession, email: str):
    users_repo = UsersRepository(db)
    return await users_repo.get_by_email(email)
