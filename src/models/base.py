from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Integer

from ..database.database import Base


class BaseModel(Base):
    """
    Classe base para herança pois todas as tabelas tem Id
    """

    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)


class CompositeKeyBase(Base):
    """
    Chave composta
    """

    __abstract__ = True
