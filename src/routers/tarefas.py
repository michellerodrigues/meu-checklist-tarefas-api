from __future__ import annotations

from database.database import SessionLocal
from fastapi import APIRouter
from fastapi import Depends
from schemas.categoria import Tarefa
from schemas.categoria import TarefaCreate
from services.categorias import buscar_categoria
from services.tarefas import criar_tarefa
from sqlalchemy.orm import Session

from src.machine_learning import prever_categoria

router = APIRouter(prefix='/tarefas', tags=['Tarefas'])


def get_db():
    """Rotas para listagem e controle de Tarefas"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    '/',
    response_model=Tarefa,
    summary='Cria uma nova tarefa',
)
def criar_nova_tarefa(
    nova_tarefa: TarefaCreate,
    db: Session = Depends(get_db),
):

    categoria_nome = prever_categoria(nova_tarefa.descricao)

    categoria = buscar_categoria(categoria_nome, db)

    nova_tarefa.categoria_id = categoria.id
    nova_tarefa.recorrencia_id = 1

    return criar_tarefa(nova_tarefa, db)
