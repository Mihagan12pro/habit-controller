from repositories.base import RepositoryBase
from models import user as u, habit as h
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

class HabitsRepository(RepositoryBase):  # Репозиторий для привычек
    def __init__(self, session):
        super().__init__(session)

    """
    Добавление асинхронно
    """
    async def add_async(self, user_id, title):
        errors = []#Массив ошибок
        check_user_existing = await self.session.execute(select(u.User).filter_by(u.User.id == user_id))

        if check_user_existing == None:
            errors.append("Пользователя не существует!")
            return errors
        
        check_habit_exists = await self.session.execute(select(h.Habit).filter_by(
                and_(
                    h.Habit.title == habit.title,
                    h.Habit.user_id == habit.user_id
                )
            ))
        
        if check_habit_exists != None:
            errors.append("Привычка с данным названием уже существует!")
            return errors
        
        
        habit = h.Habit()
        habit.status = habit.started
        habit.title = title
        habit.user_id = user_id
        
        self.session.add(habit)

        await self.session.commit()

        result = await self.session.execute(select(u.User.id).filter_by(
                and_(
                    h.Habit.title == habit.title,
                    h.Habit.user_id == habit.user_id
                )
            ))
        
        return result.first().id



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
    
    """
    Удалить привычку
    """
    async def delete_habit(self, id):
         errors = []#Массив ошибок

         habit = await self.session.execute(select(h.Habit).filter_by(h.Habit.id == id))

         if habit.first() == None:
             errors.append("Данной привычки не существует!")

             return errors
        
         await self.session.delete(habit)
         await self.session.commit()

         return id

         




        
