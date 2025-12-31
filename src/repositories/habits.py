from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.habit import Habit
from src.repositories.base import RepositoryBase
from src.schemas import HabitCreate


class HabitsRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
    
    progress_repository = None

    async def get_by_id(self, habit_id: int) -> Optional[Habit]:
        stmt = select(Habit).where(Habit.id == habit_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_habits(self, user_id: int, status: str = None) -> List[Habit]:
        """
        Получить привычки.
        По умолчанию НЕ возвращает удаленные (status='deleted'), если явно не запрошено.
        """
        stmt = select(Habit).where(Habit.user_id == user_id)

        if status:
            stmt = stmt.where(Habit.status == status)
        else:
            # Если статус не указан, возвращаем всё, КРОМЕ удаленных
            stmt = stmt.where(Habit.status != "deleted")

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, user_id: int, habit_dto: HabitCreate) -> Habit:
        # УБРАНА проверка на уникальность названия (get_by_title)

        habit = Habit()
        habit.user_id = user_id
        habit.title = habit_dto.title

        if hasattr(habit_dto, "status") and habit_dto.status:
            habit.status = habit_dto.status
        else:
            habit.status = "start"

        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def update(
        self, habit_id: int, title: str = None, status: str = None
    ) -> Optional[Habit]:
        """Обновление полей привычки"""
        habit = await self.get_by_id(habit_id)
        if habit is None:
            return None

        if title:
            habit.title = title
        if status:
            habit.status = status

        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def delete(self, habit_id: int):
        """Мягкое удаление (смена статуса на deleted)"""
        habit = await self.get_by_id(habit_id)
        if habit is None:
            return None

        habit.status = "deleted"
        await self.session.commit()

        return True

    async def change_status(self, habit_id: int, new_status: str):
        habit = await self.get_by_id(habit_id)
        if habit is None:
            return None

        habit.status = new_status
        await self.session.commit()
        await self.session.refresh(habit)
        return habit
    
    async def get_status(self, habit_id: int):
        habit = await self.get_by_id(habit_id)

        if habit is None:
            return None
        
        return habit.status
        

