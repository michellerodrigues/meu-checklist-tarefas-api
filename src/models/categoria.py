from __future__ import annotations

from datetime import date

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class CategoriaModel(BaseModel):
    """Definição de agrupamento das tarefas. Uma Categoria agrupa N Tarefas"""

    __tablename__ = 'categorias'
    nome = Column(String, unique=True, index=True)
    tarefas = relationship('TarefaModel', back_populates='categoria')


class TarefaModel(BaseModel):
    """A Tarefa possui uma recorência (frequencia de execução),
    # ela também pertence a uma Categoria
    # e endereça as tags que se relacionarão com as respostas do questionário"""

    __tablename__ = 'tarefas'
    descricao = Column(String, index=True)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    recorrencia_id = Column(Integer, ForeignKey('recorrencias.id'))
    categoria = relationship('CategoriaModel', back_populates='tarefas')
    recorrencia = relationship('RecorrenciaModel', back_populates='tarefas')
    tags = Column(Text, nullable=False)


class RecorrenciaModel(BaseModel):
    """A Recorrência classifica em 'Diária','Semanal','Mensal' cada tarefa que se relaciona com ela
    A recorrencia da tarefa endeceçará os eventos de verificação de tarefas em atraso, etc.
    """

    __tablename__ = 'recorrencias'
    descricao = Column(String, unique=True, index=True)
    tarefas = relationship('TarefaModel', back_populates='recorrencia')


class Execucao(BaseModel):
    """A Execucao marca quando a tarefa foi executada pelo usuário"""

    __tablename__ = 'execucoes'
    tarefa_id = Column(Integer, ForeignKey('tarefas.id'))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    data_execucao = Column(DateTime, nullable=False, default=date.today)
    observacoes = Column(Text)
