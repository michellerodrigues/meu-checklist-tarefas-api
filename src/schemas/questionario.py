from __future__ import annotations

import json

from pydantic import BaseModel
from pydantic import field_validator

from .base import OpcaoBase
from .base import PerguntaBase


class OpcaoSchema(OpcaoBase):
    """
    Neste módulo, temos o schema questionário que irá guiar tags
    Cada pergunta tem suas opções e cada opção carrega uma lsita de #hashTags
    """

    selecionada: bool


class PerguntaSchema(PerguntaBase):  # noqa: C0115
    opcoes: list[OpcaoSchema]

    @field_validator('opcoes')
    @classmethod
    def validar_opcoes_radio(cls, v: list[str], values):
        if values.data.get('tipo') == 'radio':
            selecionadas = sum(1 for opcao in v if opcao.selecionada)
            if selecionadas > 1:
                raise ValueError(
                    "Perguntas 'radio' devem ter no máximo uma opção selecionada",
                )
        return v


class QuestionarioResponse(BaseModel):  # noqa: C0115
    id: int
    perguntas: list[PerguntaSchema]

    class Config:  # noqa: C0115
        orm_mode = True


class ResponderQuestionarioRequest(BaseModel):
    """
    Contrato de Requisição para Resposta de Questionário do Usuário
    """

    id: int
    respostas: list[RespotasSelecionadas]

    class Config:  # noqa: C0115
        orm_mode = True


class RespotasSelecionadas(BaseModel):  # noqa: C0115
    opcoes_selecionadas: list[int]

    class Config:  # noqa: C0115
        orm_mode = True


class ResponderQuestionarioResponse(BaseModel):
    """
    Contrato de Retorno para Resposta de Questionário do Usuário
    """

    mensagem: str
    questionario_id: int
    tags_usuario: list[str]

    @field_validator('tags_usuario')
    @classmethod
    def parse_tags(cls, value: list[str]):
        if isinstance(value, str):
            return json.loads(value)
        return value

    class Config:  # noqa: C0115
        orm_mode = True


OpcaoSchema.model_rebuild()
QuestionarioResponse.model_rebuild()
RespotasSelecionadas.model_rebuild()
ResponderQuestionarioRequest.model_rebuild()
PerguntaSchema.model_rebuild()
