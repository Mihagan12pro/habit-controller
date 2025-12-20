from src.schemas import HabitCreate

from typing import List, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.habit import Habit
from src.repositories.base import RepositoryBase


class HabitsRepository(RepositoryBase):  # Репозиторий для привычек
    def __init__(self, session: AsyncSession):
        super().__init__(session)
    
    progress_repository = None  # Обязательно надо инициализировать поле

    """
    Получить привычку по названию
    """
    async def get_by_title(self, title: str) -> Optional[Habit]:
        stmt = select(Habit).where(Habit.title == title)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    """
    Получить привычку по id
    """
    async def get_by_id(self, habit_id: int) -> Optional[Habit]:
        stmt = select(Habit).where(Habit.id == habit_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    """
    Получить все привычки пользователя
    """
    async def get_habits(self, user_id: int) -> List[Habit]:
        stmt = select(Habit).where(Habit.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    """
    Создать новую привычку
    """
    async def create(self, user_id : int, habit_dto: HabitCreate) -> Union[int, str]:
        habit = Habit()
        habit.user_id = user_id
        habit.title = habit_dto.title

        if await self.get_by_title(habit.title) != None:
            return 'Привычка с данным названием уже существует!'
        
        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)

        # await self.progress_repository.cre

        return habit.id
    
    """
    Удалить привычку
    """
    async def delete(self, habit_id : int):
        habit = await self.get_by_id(habit_id)
        if habit == None:
            return "Привычка не найдена!"
        
        await self.progress_repository.delete(habit)
        
        await self.session.delete(habit)
        await self.session.commit()
        

    

