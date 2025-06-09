from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session

from ..models.categoria import CategoriaModel
from ..models.categoria import TarefaModel
from ..schemas.categoria import (
    CarregaPainelUsuarioResponse,
)
from ..schemas.categoria import CategoriaCreate as CategoriaCreateSchema
from ..schemas.converters import CategoriaConverter


def criar_categoria(categoria: CategoriaCreateSchema, db: Session) -> CategoriaModel:
    db_categoria = CategoriaModel(nome=categoria.nome)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def listar_categorias(db: Session) -> list[CarregaPainelUsuarioResponse]:
    db_categoria = (
        db.query(CategoriaModel)
        .options(
            selectinload(CategoriaModel.tarefas).selectinload(TarefaModel.recorrencia),
        )
        .all()
    )

    if db_categoria is None:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')

    return CategoriaConverter.to_schema(db_categoria)


def ler_categoria(categoria_id: int, db: Session) -> CategoriaModel:
    db_categoria = (
        db.query(CategoriaModel).filter(CategoriaModel.id == categoria_id).first()
    )
    if db_categoria is None:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return db_categoria
