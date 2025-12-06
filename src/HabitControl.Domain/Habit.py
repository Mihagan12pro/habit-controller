from .Base import Base
from sqlalchemy import Column, Integer, String
import enum

class HabitStatus(enum.Enum):
    start = (0, "start")#Пользователь начал вырабатывать привычку
    end = (1, "end")#Привычка выработана
    frozen = (2, "frozen")#Пользователь временно перестал пытаться вырабатывать привычку
    delete = (3, "delete")#Удалить привычку



class Habit(Base):
    tittle = Column(String)

    id = Column(Integer, primary_key=True, index = True)
    
    status = Column(String)

    