from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


# эта схема нужна для понимания какие статусы есть в принципе в бд
class Status(str, Enum):
    START = "start"  # Начал, в процессе
    FROZEN = "frozen"  # Заморожена (отпуск/болезнь)
    ARCHIVED = "archived"  # В архиве (надоела или выполнена)
    DELETED = "deleted"  # Удалена (в корзине)


class StatusInput(str, Enum):
    START = "start"  # Начал, в процессе
    FROZEN = "frozen"  # Заморожена (отпуск/болезнь)
    ARCHIVED = "archived"  # В архиве (надоела или выполнена)


# --- Общая схема для обновления статуса ---
class StatusUpdate(BaseModel):
    status: StatusInput


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
        from_attributes = True


# --- Habit DTOs ---
class HabitBase(BaseModel):
    title: str
    status: str = "start"


class HabitCreate(HabitBase):
    pass


# Схема для редактирования (имя и/или статус)
class HabitUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[StatusInput] = None


class HabitOut(HabitBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# --- Progress DTOs ---
class ProgressCreate(BaseModel):
    date: date


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


# --- Cessation DTOs ---
class CessationCreate(BaseModel):
    title: str
    status: str = "start"  # Или active, смотря что в модели по дефолту


# Схема для редактирования отвыкания
class CessationUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[StatusInput] = None


class CessationOut(CessationCreate):
    id: int
    started_at: datetime
    user_id: int
    status: str
    duration_seconds: int = 0

    class Config:
        from_attributes = True


# --- DASHBOARD SCHEMA ---
class DashboardMeta(BaseModel):
    show_overload_warning: bool


class DashboardOut(BaseModel):
    habits: list[HabitOut]
    cessations: list[CessationOut]
    meta: DashboardMeta
