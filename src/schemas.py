from typing import List

from pydantic import BaseModel


# --- User DTOs ---
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


# --- Habit DTOs ---
class HabitCreate(BaseModel):
    title: str


class HabitOut(BaseModel):
    id: int
    title: str
    status: str

    class Config:
        orm_mode = True


# --- Progress DTOs ---
class ProgressCreate(BaseModel):
    date: str  # YYYY-MM-DD


class StatsOut(BaseModel):
    habit_id: int
    habit_title: str
    total_completions: int
    current_streak: int  # Добавим расчет серии!
    dates: List[str]
