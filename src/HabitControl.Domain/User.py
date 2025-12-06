from .Base import Base

class User(Base):

    
    def __init__(self, name, id, hashed_password, email):
        self.name = name
        self.__id = id
        self.__hashed_password = hashed_password
        self.email = email
    
    @property
    def id(self):
        return self.__id
    
    @property
    def hashed_password(self):
        return self.__hashed_password