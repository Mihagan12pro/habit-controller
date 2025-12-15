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
        check_user_existing = (
            await self.session.execute(select(u.User).where(u.User.id == user.id))
        ).scalar_one_or_none()

        if check_user_existing is None:
            errors.append("Пользователя не существует!")
            return errors
        
        check_habit_exists = (
            await self.session.execute(
                select(h.Habit).where(
                    and_(h.Habit.title == title, h.Habit.user_id == user.id)
                )
            )
        ).scalar_one_or_none()
        
        if check_habit_exists is not None:
            errors.append("Привычка с данным названием уже существует!")
            return errors
        
        
        habit = h.Habit()
        habit.status = habit.started
        habit.title = title
        habit.user_id = user.id
        
        self.session.add(habit)

        await self.session.commit()

        if self.progress_repository:
            await self.progress_repository.add_async(habit)#Привычка создается - создаается статистика

    """
    Обновление статуса привычки
    """
    async def update_status_async(self, id, status):
         errors = []#Массив ошибок
         result = await self.session.execute(
             select(h.Habit).where(h.Habit.id == id)
         )

         habit = result.scalar_one_or_none()

         if habit is None:
            errors.append("Такой привычки не существует!")
            return errors
         
         habit.status = status

         await self.session.commit()

         if self.progress_repository:
             progress = await self.progress_repository.get_by_habit_async(habit)#По любому при изменении статуса привычки статистика сбросится
             if progress:
                 await self.progress_repository.delete_async(progress)

         if self.progress_repository and status == habit.started:#Но статус "start", то создастся новая статистика, т.к. человек, к примеру, хотел бросить курить, но сорвался и покурил, тем самым начал как-бы заново
            await self.progress_repository.add_async(habit)

    """
    Получить привычку по ее названию
    """
    async def get_by_name_async(self, name):
        errors = []#Массив ошибок
        result = await self.session.execute(select(h.Habit).where(h.Habit.title == name))

        if result is None:
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
         result = await self.session.execute(select(h.Habit).where(h.Habit.status == status))

         return result
    
    """
    Удалить привычку
    """
    async def delete_habit(self, habit):
         errors = []#Массив ошибок

         result = await self.session.execute(select(h.Habit).where(h.Habit.id == habit.id))

         if result.first() is None:
             errors.append("Данной привычки не существует!")

             return errors
         
         if self.progress_repository:
             progress = await self.progress_repository.get_by_habit_async(habit)
             if progress:
                 await self.progress_repository.delete_async(progress)#Сперва удалим прогресс, т.к. в нем содержится внешний ключ на привычку

         await self.session.delete(habit)
         await self.session.commit()

         




        
