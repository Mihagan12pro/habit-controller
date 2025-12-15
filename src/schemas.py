from typing import List
from datetime import date
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
        from_attributes = True  # Исправили (было orm_mode)


# --- Habit DTOs ---
class HabitCreate(BaseModel):
    title: str


class HabitOut(BaseModel):
    id: int
    title: str
    status: str

    class Config:
        from_attributes = True  # Исправили (было orm_mode)


# --- Progress DTOs ---
class ProgressCreate(BaseModel):
    date: date  # YYYY-MM-DD


class StatsOut(BaseModel):
    habit_id: int
    habit_title: str
    total_completions: int
    current_streak: int
    dates: List[date]

    class Config:
        from_attributes = True  # Добавили на всякий случай
