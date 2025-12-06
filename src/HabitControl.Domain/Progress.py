from .Base import Base
from sqlalchemy import Column, Integer, String

class Progress(Base):
    start_date = Column(String)

    def dayes_passes(self):
        pass