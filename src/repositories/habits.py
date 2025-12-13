from repositories.base import RepositoryBase
from models import user as u, habit as h
from sqlalchemy.future import select
from sqlalchemy import and_

class HabitsRepository(RepositoryBase):  # Репозиторий для привычек
    def __init__(self, session):
        super().__init__(session)
    
    progress_repository = None#Обязательно надо инициализировать поле

    """
    Добавление асинхронно
    """
    async def add_async(self, user, title):
        errors = []#Массив ошибок
        check_user_existing = await self.session.execute(select(u.User).filter_by(u.User.id == user.id))

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
        habit.user_id = user.id
        
        self.session.add(habit)

        await self.session.commit()

        await self.session.progress_repository.add_async(self, habit)#Привычка создается - создаается статистика

    """
    Обновление статуса привычки
    """
    async def update_status_async(self, id, status):
         errors = []#Массив ошибок
         result = await self.session.execute(select(h.Habit).filter_by(h.Habit.id == id))

         if result == None:
            errors.append("Такой привычки не существует!")
            return errors
         
         habit = result.first()
         habit.status = status

         await self.session.commit()

         if status != habit.start:
             progress = await self.progress_repository.get_by_habit_async(habit).first()
             await self.progress_repository.delete_async(progress)

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
    async def delete_habit(self, habit):
         errors = []#Массив ошибок

         result = await self.session.execute(select(h.Habit).filter_by(h.Habit.id == habit.id))

         if result.first() == None:
             errors.append("Данной привычки не существует!")

             return errors
         
         progress = await self.progress_repository.get_by_habit_async(habit).first()
         await self.progress_repository.delete_async(progress)#Сперва удалим прогресс, т.к. в нем содержится внешний ключ на привычку

         await self.session.delete(habit)
         await self.session.commit()

         return id

         




        
