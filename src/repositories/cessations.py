from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.cessation import Cessation
from src.repositories.base import RepositoryBase
from src.schemas import CessationCreate


class CessationsRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, user_id: int, cessation_dto: CessationCreate) -> Cessation:
        cessation = Cessation()
        cessation.title = cessation_dto.title
        cessation.user_id = user_id
        cessation.started_at = datetime.now()
        cessation.status = cessation_dto.status if cessation_dto.status else "active"

        self.session.add(cessation)
        await self.session.commit()
        await self.session.refresh(cessation)
        return cessation

    async def get_by_id(self, cessation_id: int) -> Optional[Cessation]:
        stmt = select(Cessation).where(Cessation.id == cessation_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int, status: str = None) -> List[Cessation]:
        """Получить отвыкания с фильтром по статусу"""
        stmt = select(Cessation).where(Cessation.user_id == user_id)

        if status:
            stmt = stmt.where(Cessation.status == status)
        else:
            # По умолчанию скрываем удаленные
            stmt = stmt.where(Cessation.status != "deleted")

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(
        self, cessation_id: int, title: str = None, status: str = None
    ) -> Optional[Cessation]:
        habit = await self.get_by_id(cessation_id)
        if not habit:
            return None

        if title:
            habit.title = title
        if status:
            habit.status = status

        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def reset_counter(self, cessation_id: int) -> Optional[Cessation]:
        habit = await self.get_by_id(cessation_id)
        if not habit:
            return None

        habit.started_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def change_status(
        self, cessation_id: int, new_status: str
    ) -> Optional[Cessation]:
        habit = await self.get_by_id(cessation_id)
        if not habit:
            return None

        habit.status = new_status
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def delete(self, cessation_id: int) -> bool:
        """Мягкое удаление"""
        habit = await self.get_by_id(cessation_id)
        if not habit:
            return False

        habit.status = "deleted"
        await self.session.commit()
        return True
