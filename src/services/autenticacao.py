from datetime import datetime
import json
from typing import List
from fastapi import HTTPException
from services.questionario import obter_questionario_usuario, get_tags_do_usuario
from schemas.usuario import CadastrarUsuarioRequest, UsuarioLoginRequest, UsuarioLoginResponse
from security.security import criar_hash_senha, verificar_senha
from models.questionario import QuestionarioModel
from models.usuario import UsuarioModel
from sqlalchemy.future import select
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def __usuario_valido(email: str, senha: str, db: Session):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    
    if not usuario or not verificar_senha(senha, usuario.hash_senha):
       return False
    
    return usuario

def efetuar_login(dados_login: UsuarioLoginRequest, db: Session):
    
    usuario = __usuario_valido(dados_login.email, dados_login.senha, db)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
   
    dataUltimoAcessoLogin = usuario.data_ultimo_acesso
    dataUltimoAcesso = datetime.now()
    usuario.data_ultimo_acesso = dataUltimoAcesso   
   
    
    if dataUltimoAcessoLogin is None:    
        novo_questionario = QuestionarioModel(
            usuario_id=usuario.id,
            data_criacao=datetime.now()
         )
        
        db.add(novo_questionario)
        db.commit()
        db.refresh(novo_questionario)
        return UsuarioLoginResponse(email=usuario.email, temQuestionario=False, questionario_id = 0, data_ultimo_acesso=dataUltimoAcesso,tags=[])

    questionarioUsuario = obter_questionario_usuario(usuario.email, db)

    if questionarioUsuario is None and dataUltimoAcessoLogin is None:
        return UsuarioLoginResponse(email=usuario.email, temQuestionario=False, questionario_id = 0, data_ultimo_acesso=dataUltimoAcesso,tags=[])
    
    tags = get_tags_do_usuario(questionarioUsuario["perguntas"])
    
    if tags is None or tags==[]:
        return UsuarioLoginResponse(email=usuario.email, temQuestionario=False, questionario_id = 0, data_ultimo_acesso=dataUltimoAcesso,tags=[])
    
    return  UsuarioLoginResponse(email=usuario.email, temQuestionario=True, questionario_id = questionarioUsuario["id"], data_ultimo_acesso=dataUltimoAcesso,tags=tags)  


def criar_usuario(usuario: CadastrarUsuarioRequest, db: Session):
    if db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    hash_senha = criar_hash_senha(usuario.senha)
    
    db_usuario = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        hash_senha=hash_senha
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario
