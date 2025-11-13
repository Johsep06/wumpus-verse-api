from sqlalchemy import Column, Integer, String, Boolean, DateTime

from models import Base

class Enviroments(Base):
    __tablename__ = 'ambiente'

    id = Column('id', Integer, primary_key=True)
    width = Column('largura', Integer)
    height = Column('altura', Integer)

    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height