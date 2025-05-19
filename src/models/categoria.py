from datetime import date
import json
from pydantic import field_validator
from sqlalchemy import JSON, Column, DateTime, String, Text
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel


# Definição de agrupamento das tarefas. Uma Categoria agrupa N Tarefas
class CategoriaModel(BaseModel):
    __tablename__ = "categorias"
    nome = Column(String, unique=True, index=True)
    tarefas = relationship("TarefaModel", back_populates="categoria")


# A Tarefa possui uma recorência (frequencia de execução), 
# ela também pertence a uma Categoria 
# e endereça as tags que se relacionarão com as respostas do questionário
class TarefaModel(BaseModel):
    __tablename__ = "tarefas"
    descricao = Column(String, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    recorrencia_id = Column(Integer, ForeignKey("recorrencias.id")) 
    categoria = relationship("CategoriaModel", back_populates="tarefas")
    recorrencia = relationship("RecorrenciaModel", back_populates="tarefas")
    tags =  Column(Text,nullable=False)
   

# A Recorrência classifica em 'Diária','Semanal','Mensal' cada tarefa que se relaciona com ela
# A recorrencia da tarefa endeceçará os eventos de verificação de tarefas em atraso, etc.

class RecorrenciaModel(BaseModel):
    __tablename__ = "recorrencias"
    descricao = Column(String, unique=True, index=True)
    tarefas = relationship("TarefaModel", back_populates="recorrencia")


# A Execucao marca quando a tarefa foi executada pelo usuário
class Execucao(BaseModel):
    __tablename__ = "execucoes"
    tarefa_id = Column(Integer, ForeignKey("tarefas.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    data_execucao = Column(DateTime, nullable=False, default = date.today)
    observacoes  = Column(Text)