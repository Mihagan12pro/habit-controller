from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src import schemas
from src.repositories.habits import HabitsRepository
from src.repositories.users import UsersRepository
from src.schemas import HabitOut


async def create_new_habit(
    db: AsyncSession, user_id: int, habit_dto: schemas.HabitCreate
) -> HabitOut:
    users_repo = UsersRepository(db)
    user = await users_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    habits_repo = HabitsRepository(db)
    # Убрали try/except, так как уникальность нам больше не нужна
    created_habit = await habits_repo.create(user_id, habit_dto)

    return HabitOut.model_validate(created_habit)


async def delete_habit_service(db: AsyncSession, habit_id: int):
    habits_repo = HabitsRepository(db)
    result = await habits_repo.delete(habit_id)
    if not result:
        raise HTTPException(status_code=404, detail="Привычка не найдена")
    return {"message": "Habit deleted (moved to trash)"}


async def change_habit_status_service(db: AsyncSession, habit_id: int, status: str):
    habits_repo = HabitsRepository(db)
    result = await habits_repo.change_status(habit_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="Привычка не найдена")
    return HabitOut.model_validate(result)
