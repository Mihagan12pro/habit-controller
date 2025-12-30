from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database import get_db
from src.services.habit import create_new_habit
from src.services.progress import track_habit_progress

router = APIRouter(tags=["Habits"])


@router.post("/users/{user_id}/habit", response_model=schemas.HabitOut)
async def create_habit(
    user_id: int, habit: schemas.HabitCreate, db: AsyncSession = Depends(get_db)
):
    return await create_new_habit(db, user_id, habit)

# @router.get("/{habit_id}", response_model=schemas.HabitOut)
# async def create_habit(
#     user_id: int, habit: schemas.HabitCreate, db: AsyncSession = Depends(get_db)
# ):
#     return await get_habit(db, user_id, habit)

# @router.get("/{user_id}/all", response_model=List[schemas.HabitOut])
# async def show_all_habits(user_id: int, db: AsyncSession = Depends(get_db)):
#     return await get_all_habits(db, user_id)


@router.post("/habits/{habit_id}/track")
async def track_habit(habit_id: int, db: AsyncSession = Depends(get_db)):
    return await track_habit_progress(db, habit_id)


# TODO: Добавить ручки для редактирования статуса и удаления привычки
