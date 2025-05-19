import json
from pydantic import BaseModel, field_validator
from typing import List
from .base import OpcaoBase, PerguntaBase

class OpcaoSchema(OpcaoBase):
    selecionada: bool

class PerguntaSchema(PerguntaBase):
    opcoes: List[OpcaoSchema]

    @field_validator('opcoes')
    def validar_opcoes_radio(cls, v, values):
        if values.data.get('tipo') == 'radio':
            selecionadas = sum(1 for opcao in v if opcao.selecionada)
            if selecionadas > 1:
                raise ValueError("Perguntas 'radio' devem ter no máximo uma opção selecionada")
        return v


class QuestionarioResponse(BaseModel):
    id: int
    perguntas: List[PerguntaSchema]

    class Config:
        orm_mode = True

class ResponderQuestionarioRequest(BaseModel):
    id: int
    respostas: List['RespotasSelecionadas'] 

    class Config:
        orm_mode = True

class RespotasSelecionadas(BaseModel):
    opcoes_selecionadas: List[int] 
    
    class Config:
        orm_mode = True

class ResponderQuestionarioResponse(BaseModel):
    mensagem: str
    questionario_id: int
    tags_usuario: List[str]

    @field_validator('tags_usuario')
    def parse_tags(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value

    class Config:
        orm_mode = True


OpcaoSchema.model_rebuild()
QuestionarioResponse.model_rebuild()
RespotasSelecionadas.model_rebuild()
ResponderQuestionarioRequest.model_rebuild()
PerguntaSchema.model_rebuild()