from sqlalchemy import Column, Integer, String, DateTime
from models.base import BaseModel
from sqlalchemy.orm import relationship


# Nesta tabela temos os dados do usuário e uma encriptação simples da sua senha 'hash_senha'
# A 'data_ultimo_acesso' é atualizada sempre que o usuário faz login. Ela guiará as futuras notificações
# Nas proximas entregas, implementarei o token do usuário


class UsuarioModel(BaseModel):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hash_senha = Column(String(255), nullable=False)
    data_ultimo_acesso = Column(DateTime)
    questionarios = relationship('QuestionarioModel', backref='usuario', lazy=True)