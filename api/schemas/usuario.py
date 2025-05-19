from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class CadastrarUsuarioRequest(UsuarioBase):
    senha: str

class CadastrarUsuarioResponse(UsuarioBase):
    data_ultimo_acesso: datetime | None
    
    class Config:
        orm_mode = True

class UsuarioLoginRequest(BaseModel):
    email: EmailStr
    senha: str

class UsuarioLoginResponse(BaseModel):
    email: EmailStr
    temQuestionario: bool
    questionario_id:int
    data_ultimo_acesso: datetime    
    tags: List[str] = []


