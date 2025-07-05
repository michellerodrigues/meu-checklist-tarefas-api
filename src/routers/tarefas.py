from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from schemas.categoria import Tarefa
from schemas.categoria import TarefaCreate
from services.tarefas import criar_tarefa
from services.tarefas import ler_categoria
from sqlalchemy.orm import Session

from database.database import SessionLocal

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

    categoriaModelRetorno = ler_categoria(nova_tarefa.categoria_id, db)
    nova_tarefa.categoria_id = categoriaModelRetorno.id

    return criar_tarefa(nova_tarefa, db)
