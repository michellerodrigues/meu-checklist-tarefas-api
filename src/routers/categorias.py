from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.categorias import criar_categoria, ler_categoria, listar_categorias
from schemas.categoria import CarregaPainelUsuarioResponse, CategoriaCreate  as CategoriaCreateSchema
from schemas.categoria import Categoria as CategoriaSchema
from database.database import SessionLocal
from typing import List


router = APIRouter()

router = APIRouter(prefix="/categorias", tags=["Categorias"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", 
             response_model=CategoriaSchema,
             summary="Cria uma nova categoria vazia, sem tarefas")
def criar_nova_categoria(categoria: CategoriaCreateSchema, db: Session = Depends(get_db)):
    
    return criar_categoria(categoria,db)

@router.get("/", 
             response_model=List[CarregaPainelUsuarioResponse],
             summary="Lista a Categoria com Todas as tarefas disponíveis para a aplicação", 
             response_description="Lista de categorias com tarefas")
def get_all_categorias(db: Session = Depends(get_db)):
    return listar_categorias(db)


@router.get("/{categoria_id}", response_model=CategoriaSchema,
             summary="Obtem uma categoria específica de acordo com o id informado", 
             response_description="Uma categoria com suas tarefas")
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    return ler_categoria(categoria_id,db)