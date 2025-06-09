from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session

from ..database.database import SessionLocal
from ..schemas.usuario import CadastrarUsuarioRequest
from ..schemas.usuario import CadastrarUsuarioResponse
from ..schemas.usuario import UsuarioLoginRequest
from ..schemas.usuario import UsuarioLoginResponse
from ..services.autenticacao import criar_usuario
from ..services.autenticacao import efetuar_login

router = APIRouter(prefix='/auth', tags=['Autenticação'])


def get_db():
    """Rotas para atenticação do usuário"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    '/cadastro',
    response_model=CadastrarUsuarioResponse,
    summary='Efetua o cadastro do usuário na aplicação',
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_usuario(usuario: CadastrarUsuarioRequest, db: Session = Depends(get_db)):
    return criar_usuario(usuario, db)


@router.post(
    '/login',
    response_model=UsuarioLoginResponse,
    summary='Efetua login no sistema',
    response_description='Devolve as tags do usuário '
    '(para filtro das tarefas), se tem questionário',
)
def login(dados_login: UsuarioLoginRequest, db: Session = Depends(get_db)):
    return efetuar_login(dados_login, db)
