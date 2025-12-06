from .Base import Base

class Habit(Base):
    def __init__(self, id, tittle, is_done = False):
        self.tittle = tittle
        self.__id = id
        self.is_done = is_done

    @property
    def id(self, id):
        return self.__id

    