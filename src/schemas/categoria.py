from __future__ import annotations

from pydantic import BaseModel


class CategoriaBase(BaseModel):
    """
    Neste módulo, temos todos os schemas que definem
    Categorias - agrupamento de tarefas
    Tarefas - menor unidade que pode ser executada
    Recorrência: de quanto em quanto tempo a tarefa se repete
    Painel do Usuário - configuração para o painel do usuário.
    Se for a primeira vez (sem questionário respondido)
    nenhuma tarefa será listada
    Se ele responder o questionário,
    teremos as '#hashtags', com elas as categorias,
    que agrupam tarefas...etc

    """

    nome: str

    class Config:  # noqa: C0115
        orm_mode = True


class CategoriaCreate(CategoriaBase):
    pass


class Categoria(CategoriaBase):
    tarefas: list[Tarefa] = []

    class Config:  # noqa: C0115
        orm_mode = True


class TarefaBase(BaseModel):
    descricao: str
    categoria_id: int
    recorrencia_id: int
    tags: str

    class Config:  # noqa: C0115
        orm_mode = True


class TarefaCreate(TarefaBase):
    pass


class Tarefa(TarefaBase):
    recorrencia: Recorrencia

    class Config:  # noqa: C0115
        orm_mode = True


class RecorrenciaBase(BaseModel):
    id: int
    descricao: str


class RecorrenciaCreate(RecorrenciaBase):
    pass


class Recorrencia(RecorrenciaBase):

    class Config:  # noqa: C0115
        orm_mode = True


class TarefaUsuario(BaseModel):
    id: int
    descricao: str
    recorrencia: str
    tags: list[str]


class CarregaPainelUsuarioResponse(BaseModel):
    categoria: str
    tarefas: list[TarefaUsuario] = []


class CategoriaCombo(BaseModel):
    descricao: str
    id: int
    selecionado: bool


class CarregaCategoriaComboResponse(BaseModel):
    categorias: list[CategoriaCombo] = []
