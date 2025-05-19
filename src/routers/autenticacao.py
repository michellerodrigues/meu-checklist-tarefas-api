from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, insert
from sqlalchemy.orm import Session
from services.autenticacao import criar_usuario, efetuar_login
from database.database import SessionLocal
from schemas.usuario import CadastrarUsuarioRequest, CadastrarUsuarioResponse, UsuarioLoginRequest, UsuarioLoginResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/cadastro", response_model=CadastrarUsuarioResponse, 
                summary="Efetua o cadastro do usuário na aplicação", 
                status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: CadastrarUsuarioRequest, db: Session = Depends(get_db)): 
    return criar_usuario(usuario,db)



@router.post("/login", response_model=UsuarioLoginResponse,
            summary="Efetua login no sistema",
            response_description="Devolve as tags do usuário (para filtro das tarefas), se tem questionário")
def login(dados_login: UsuarioLoginRequest,  db: Session = Depends(get_db)):    
    return efetuar_login(dados_login, db)

        