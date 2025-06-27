from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session

from models.categoria import CategoriaModel
from models.categoria import TarefaModel
from schemas.categoria import (
    CarregaPainelUsuarioResponse,
    TarefaCreate,
)

from schemas.converters import CategoriaConverter


def criar_tarefa(nova_tarefa: TarefaCreate, db: Session) -> TarefaModel:
    db_tarefa = TarefaModel(
        descricao = nova_tarefa.descricao,
        categoria_id = nova_tarefa.categoria_id,
        recorrencia_id = nova_tarefa.recorrencia_id,
        tags = "")


    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


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

def buscar_categoria(categoria_nome: str, db: Session) -> CategoriaModel:
    db_categoria = (
        db.query(CategoriaModel).filter(CategoriaModel.nome == categoria_nome).first()
    )
    if db_categoria is None:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return db_categoria