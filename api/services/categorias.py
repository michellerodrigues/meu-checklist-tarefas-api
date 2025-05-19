from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload
from schemas.converters import CategoriaConverter
from models.categoria import CategoriaModel, TarefaModel
from schemas.categoria import CategoriaCreate  as CategoriaCreateSchema
from schemas.categoria import Categoria as CategoriaSchema



def criar_categoria(categoria: CategoriaCreateSchema, db: Session):
    db_categoria = CategoriaModel(nome=categoria.nome)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def listar_categorias(db: Session):
    db_categoria = db.query(CategoriaModel).options(
        selectinload(CategoriaModel.tarefas).selectinload(TarefaModel.recorrencia)    
        ).all()
    
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    return CategoriaConverter.to_schema(db_categoria)


def ler_categoria(categoria_id: int, db: Session):
    db_categoria = db.query(CategoriaModel).filter(CategoriaModel.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return db_categoria