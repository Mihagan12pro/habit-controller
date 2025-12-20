from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.base import RepositoryBase
import src.schemas as dto


class UsersRepository(RepositoryBase):  # Репозиторий для юзеров
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_email(self, email: str) -> Union[User, str]:
        """Получить пользователя по email"""
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    """
    Получить пользователя по id
    """
    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    """
    Создание нового пользователя
    """
    async def create(self, user_dto: dto.UserCreate) -> Union[int, str]:
        user = User()
        user.email = user_dto.email
        user.name = user_dto.name
        user.hashed_password = user_dto.password

        email_result = await self.get_by_email(user.email)

        if isinstance(email_result, User) == False:
            return 'Данная почта уже занята!'
                
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user.id
