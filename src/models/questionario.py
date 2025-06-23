from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.base import CompositeKeyBase


class PerguntaModel(BaseModel):
    """
    Cada pergunta possui o seu texto descritivo e o tipo ('radio'/'checkbox').
    Esse tipo vai guiar o frontend para montar o questionário.
    """

    __tablename__ = 'perguntas'

    texto = Column(Text, nullable=False)
    tipo = Column(String(10), nullable=False)

    # Relações
    opcoes = relationship('OpcaoModel', back_populates='pergunta')


class QuestionarioModel(BaseModel):
    """O questionário do usuário é criado sem
    respostas assim que o usuário faz login
    Uma vez preenchido o questionário possuirá
    uma lista de respstas"""

    __tablename__ = 'questionario'

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now)
    respostas = relationship('RespostaModel', back_populates='questionario')


class OpcaoModel(BaseModel):
    """Aqui temos o núcleo do questionário.
    Cada opção é uma resposta possível
    e cada opção endereça uma ou mais tags
    Uma vez marcada determinada opção (respondida)
    essas tags vão para as tags do usuário
    As tags do usuário filtrarão
    as tarefas no painel do usuário (frontend)"""

    __tablename__ = 'opcoes'

    texto = Column(Text, nullable=False)
    tags = Column(Text, nullable=False)
    pergunta_id = Column(Integer, ForeignKey('perguntas.id'))

    @property
    def tags_list(self) -> Any | list:
        return json.loads(self.tags) if self.tags else []

    # Relações
    pergunta = relationship('PerguntaModel', back_populates='opcoes')
    respostas = relationship('RespostaModel', back_populates='opcao')


class RespostaModel(CompositeKeyBase):
    """As respostas são uma relação entre questionarioId e OpcaoId
    Esta tabela determina se após o login
    o usuário vai para o painel de tarefas
    (questionarário respondido) ou responderá o questionário"""

    __tablename__ = 'respostas'

    questionario_id = Column(Integer, ForeignKey('questionario.id'), primary_key=True)
    opcao_id = Column(Integer, ForeignKey('opcoes.id'), primary_key=True)

    # Relações
    questionario = relationship('QuestionarioModel', back_populates='respostas')
    opcao = relationship('OpcaoModel', back_populates='respostas')
