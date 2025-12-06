from .Base import Base
from sqlalchemy import Column, Integer, String

def start_habit():
    return "start"
def end_habit():
    return "end"
def frozen_habit():
    return "frozen"
def delete_habit():
    return "delete"


class Habit(Base):
    
    tittle = Column(String)

    id = Column(Integer, primary_key=True, index = True)
    
    status = Column(String)

    