from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr


class UsuarioBase(BaseModel):
    """
    Classe Base do Usuário
    """

    nome: str
    email: EmailStr


class CadastrarUsuarioRequest(UsuarioBase):
    """
    Contrato de Requisição para Cadastrar Usuário
    """

    senha: str


class CadastrarUsuarioResponse(UsuarioBase):
    """
    Contrato de Resposta para Cadastrar Usuário
    """

    data_ultimo_acesso: datetime | None

    class Config:  # noqa: C0115
        orm_mode = True


class UsuarioLoginRequest(BaseModel):
    """
    Contrato de Requisição para Login Usuário
    """

    email: EmailStr
    senha: str


class UsuarioLoginResponse(BaseModel):
    """Contrato de Resposta para Login Usuário

    Atributos:
        email: identifiador de login do usuário
        temQuestionario: indica se o usuário
            tem questionário preenchido
            email: Endereço eletrônico (opcional)
            data_ultimo_acesso: registra o último acesso
            do usuário para controlar notificações de atrasos de tarefas
        tags: as tags do usuário são responsávels por listar as tarefas relacionadas
    """

    email: EmailStr
    temQuestionario: bool
    questionario_id: int
    data_ultimo_acesso: datetime
    tags: list[str] = []
