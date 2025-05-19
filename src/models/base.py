from sqlalchemy import Column, Integer
from database.database import Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)

class CompositeKeyBase(Base):
    __abstract__ = True