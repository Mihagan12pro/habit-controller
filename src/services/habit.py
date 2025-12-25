from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src import schemas
from src.repositories.habits import HabitsRepository
from src.repositories.users import UsersRepository
from src.schemas import HabitOut
from src.services.shared.httpExceptions import check_errors


async def create_new_habit(
    db: AsyncSession, user_id: int, habit_dto: schemas.HabitCreate
) -> HabitOut:  # Теперь сервис возвращает Pydantic-схему
    users_repository = UsersRepository(db)
    user_result = await users_repository.get_by_id(
        user_id
    )

    if user_result is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    habits_repository = HabitsRepository(db)
    habits_result = await habits_repository.create(user_id, habit_dto)

    if habits_result is None:
        raise HTTPException(
            status_code=400, detail="Привычка с таким названием уже существует"
        )

    return HabitOut.model_validate(habits_result)


async def get_all_habits(db: AsyncSession, user_id: int):
    habits_repository = HabitsRepository(db)
    habits = await habits_repository.get_habits(user_id)

    # Проверка на пустоту (опционально, зависит от вашей check_errors)
    if not habits:
        # check_errors(habits, 404)
        return []

    # Превращаем список объектов БД в список Pydantic-схем
    return [HabitOut.model_validate(habit) for habit in habits]


async def delete(db: AsyncSession, habit_id: int):
    habits_repository = HabitsRepository(db)
    result = await habits_repository.delete(habit_id)
    check_errors(result, 404)

    return result


async def change_status(db: AsyncSession, habit_id: int, status: str):
    habits_repository = HabitsRepository(db)
    result = await habits_repository.change_status(habit_id, status)
    check_errors(result, 404)

    return result

