from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from schemas.converters import CategoriaConverter
from sqlalchemy.orm import Session

from database.database import SessionLocal
from schemas.categoria import (
    CarregaCategoriaComboResponse,
    CarregaPainelUsuarioResponse,
)
from schemas.categoria import Categoria as CategoriaSchema
from schemas.categoria import CategoriaCreate as CategoriaCreateSchema
from services.categorias import buscar_categoria, criar_categoria
from services.categorias import ler_categoria
from services.categorias import listar_categorias
from models.categoria import CategoriaModel

from services.categoriaMLService import CategoriaMLService

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

@router.get(
    '/ml/{nome_tarefa}',
    response_model=CarregaCategoriaComboResponse,
    summary='Obtem do modelo de aprendizado a categoria de acordo com o nome da tarefa',
    response_description='Predição da categoria de acordo com o Algoritmo de IA',
)
def get_ml_categoria(nome_tarefa:str, db: Session = Depends(get_db)):
    
    ml_service = CategoriaMLService()

   # sugestaoIACategoria = prever_categoriaV0(nome_tarefa, threshold=0.05)
    sugestaoIACategoria = ml_service.prever_categoria(nome_tarefa, threshold=0.05)
    
    categoriaEncontradaIA = buscar_categoria(sugestaoIACategoria,db)

    if categoriaEncontradaIA is None:
        raise HTTPException(status_code=400, detail='Categoria prevista pela IA não está cadastrada na base de dados')

    db_categoria = (
        db.query(CategoriaModel)
        .all()
    )

    return CategoriaConverter.to_categoria_combo(db_categoria, categoriaEncontradaIA)
