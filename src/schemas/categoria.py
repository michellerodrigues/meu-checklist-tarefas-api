import json
from pydantic import BaseModel, Field, field_validator
from typing import List


class CategoriaBase(BaseModel):
    nome: str

    class Config:
        orm_mode = True

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    tarefas: List['Tarefa'] = []

    class Config:
        orm_mode = True



class TarefaBase(BaseModel):
    descricao: str
    categoria_id: int
    recorrencia_id: int
    tags: str

    class Config:
        orm_mode = True



class TarefaCreate(TarefaBase):
    pass

class Tarefa(TarefaBase):
    recorrencia: 'Recorrencia'

    class Config:
        orm_mode = True


class RecorrenciaBase(BaseModel):
    descricao: str

class RecorrenciaCreate(RecorrenciaBase):
    pass

class Recorrencia(RecorrenciaBase):
    
    class Config:
        orm_mode = True        


class TarefaUsuario(BaseModel):
    id: int
    descricao: str
    recorrencia: str
    tags: List[str]

class CarregaPainelUsuarioResponse(BaseModel):
    categoria: str    
    tarefas: List['TarefaUsuario'] = []
    