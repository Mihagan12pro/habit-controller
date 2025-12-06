from .Base import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    name = Column(String)
    id = Column(Integer, primary_key=True, index = True)
    hashed_password = Column(String)
    email = Column(String)