from sqlalchemy.future import select
from sqlalchemy import and_
from models import user as u
from repositories.base import RepositoryBase


class UsersRepository(RepositoryBase):  # Репозиторий для юзеров
    def __init__(self, session):
        super().__init__(session)

    """
    Добавление нового юзера в бд. Используется при регистрации
    """
    async def add_async(self, user):
        errors = []  # Массив ошибок
        user.email = user.email.lower()
        result = await self.session.execute(select(u.User).filter_by(email=user.email))
        existing_user = result.scalar_one_or_none()

        if existing_user is not None:
            errors.append("Пользователь с данной почтой уже существует!")
            return errors

        self.session.add(user)

        await self.session.commit()

    """
    Получение пароля пользователя по логину
    """
    async def get_password_async(self, id):
        errors = []#Массив ошибок

        user = await self.session.execute(select(u.User).filter_by(u.User.id == id))

        if user == None:
            errors.append("Неверный логин или пароль!")
            return errors
        
        return user.hashed_password
    
    """
    Получение логина пользователя
    """
    async def get_user_name_async(self, id):
        errors = []#Массив ошибок

        user = await self.session.execute(select(u.User).filter_by(u.User.id == id))

        if user == None:
            errors.append("Пользователя с данным id не существует!")
            return errors
        
        return user.name
