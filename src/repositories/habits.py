from repositories.base import RepositoryBase
from models import user as u, habit as h
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class HabitsRepository(RepositoryBase):  # Репозиторий для привычек
    def __init__(self, session):
        super().__init__(session)

    """
    Добавление асинхронно
    """
    async def add_async(self, habit):
        errors = []#Массив ошибок
        id = habit.user_id
        result = await self.session.execute(select(u.User).filter_by(u.User.id == id))

        if result == None:
            errors.append("Пользователя не существует!")
            return errors
        
        self.session.add(habit)

        await self.session.commit()

    """
    Обновление статуса привычки
    """
    async def update_status_async(self, id, status):
         errors = []#Массив ошибок
         result = await self.session.execute(select(h.Habit).filter_by(h.Habit.id == id))

         if result == None:
            errors.append("Такой привычки не существует!")
            return errors
         
         result.first().status = status

         await self.session.commit()

    """
    Получить привычку по ее названию
    """
    async def get_by_name_async(self, name):
        errors = []#Массив ошибок
        result = await self.session.execute(select(h.Habit).filter_by(h.Habit.name == name))

        if result == None:
            errors.append("Такой привычки не существует!")
            return errors
        
        return result
    
    """
    Получить все привычки
    """
    async def get_habits(self):
        result = await self.session.execute(select(h.Habit))

        return result
    
    """
    Получить все привычки с определенным статусом
    """
    async def get_habits_by_status(self, status):
         result = await self.session.execute(select(h.Habit).filter_by(h.Habit.status == status))

         return result



        
