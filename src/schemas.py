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
class HabitBase(BaseModel):
    title: str
    # status делаем опциональным со значением по умолчанию,
    # чтобы не обязательно было отправлять его при создании
    status: str = "start"

class HabitCreate(HabitBase):
    pass

class HabitOut(HabitBase):
    id: int

    class Config:
        from_attributes = True  # Исправили (было orm_mode)


# --- Progress DTOs ---
class ProgressCreate(BaseModel):
    date: date  # YYYY-MM-DD


class ProgressOut(BaseModel):
    time_passed: str

class StatsOut(BaseModel):
    habit_id: int
    habit_title: str
    total_completions: int
    current_streak: int
    dates: list[date]

    class Config:
        from_attributes = True 


# --- AntiHabit DTOs ---
class CessationCreate(BaseModel):
    pass


class CessationOut(BaseModel):
    id: int
    title: str
    started_at: date
    user_id: int
    duration_seconds: int = 0  # Это поле мы вычисляем в сервисе

    class Config:
        from_attributes = True