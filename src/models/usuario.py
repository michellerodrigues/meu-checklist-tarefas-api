from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from models.base import BaseModel


class UsuarioModel(BaseModel):
    """
    Nesta tabela temos os dados do usuário
    e uma encriptação simples da sua senha 'hash_senha'
    A 'data_ultimo_acesso' é atualizada sempre
    que o usuário faz login. Ela guiará as futuras notificações
    Nas proximas entregas, implementarei o token do usuário

    """

    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hash_senha = Column(String(255), nullable=False)
    data_ultimo_acesso = Column(DateTime)
    questionarios = relationship('QuestionarioModel', backref='usuario', lazy=True)
