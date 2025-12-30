from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


# 1. Создаем список возможных статусов
class HabitStatus(str, Enum):
    START = "start"  # Начал, в процессе
    FROZEN = "frozen"  # Заморожена (отпуск/болезнь)
    ARCHIVED = "archived"  # В архиве (надоела или выполнена)
    DELETED = "deleted"  # Удалена (в корзине)
    ACTIVE = "active"  # На всякий случай, если используется в отвыканиях


# --- Общая схема для обновления статуса ---
class StatusUpdate(BaseModel):
    status: HabitStatus


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
    status: Optional[HabitStatus] = None


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
    status: Optional[HabitStatus] = None


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
