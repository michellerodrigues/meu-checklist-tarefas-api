from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from src.models.categoria import CategoriaModel

from ..database.database import SessionLocal
from ..schemas.categoria import (
    CarregaPainelUsuarioResponse,
)
from ..schemas.categoria import Categoria as CategoriaSchema
from ..schemas.categoria import CategoriaCreate as CategoriaCreateSchema
from ..services.categorias import criar_categoria
from ..services.categorias import ler_categoria
from ..services.categorias import listar_categorias

router = APIRouter(prefix='/categorias', tags=['Categorias'])


def get_db():
    """Rotas para listagem e controle de Categorias"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    '/',
    response_model=CategoriaSchema,
    summary='Cria uma nova categoria vazia, sem tarefas',
)
def criar_nova_categoria(
    categoria: CategoriaCreateSchema,
    db: Session = Depends(get_db),
):

    return criar_categoria(categoria, db)


@router.get(
    '/',
    response_model=list[CarregaPainelUsuarioResponse],
    summary='Lista a Categoria com Todas as tarefas disponíveis para a aplicação',
    response_description='Lista de categorias com tarefas',
)
def get_all_categorias(db: Session = Depends(get_db)):
    return listar_categorias(db)


@router.get(
    '/{categoria_id}',
    response_model=CategoriaSchema,
    summary='Obtem uma categoria específica de acordo com o id informado',
    response_description='Uma categoria com suas tarefas',
)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)) -> CategoriaModel:
    return ler_categoria(categoria_id, db)
