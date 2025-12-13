from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import schemas
from src.database import get_db
from src.services.habit import create_new_habit, get_user_stats, track_progress
from src.services.user import get_user_by_id  # Для проверки юзера

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.post("/{user_id}/create", response_model=schemas.HabitOut)
def create_habit(
    user_id: int, habit: schemas.HabitCreate, db: Session = Depends(get_db)
):
    if not get_user_by_id(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

    return create_new_habit(db, user_id, habit)


@router.post("/track/{habit_id}")
def track_habit(
    habit_id: int, progress: schemas.ProgressCreate, db: Session = Depends(get_db)
):
    result = track_progress(db, habit_id, progress.date)
    if not result:
        return {"message": "Already tracked or error"}
    return {"message": "Success", "date": progress.date}


@router.get("/{user_id}/stats", response_model=List[schemas.StatsOut])
def get_stats(user_id: int, db: Session = Depends(get_db)):
    return get_user_stats(db, user_id)
