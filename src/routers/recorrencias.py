from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from schemas.categoria import RecorrenciaBase as ListarRecorrenciaResponse
from services.tarefas import listar_recorrencias
from sqlalchemy.orm import Session

from database.database import SessionLocal

router = APIRouter(prefix='/recorrencias', tags=['Recorrencias'])


def get_db():
    """Rotas para listagem e controle de Recorrencias"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    '/',
    response_model=list[ListarRecorrenciaResponse],
    summary='Listar Recorrencias',
)
def get_recorrencias(
    db: Session = Depends(get_db),
) -> list[ListarRecorrenciaResponse]:

    recorrencias = listar_recorrencias(db)

    return [{'id': rec.id, 'descricao': rec.descricao} for rec in recorrencias]
