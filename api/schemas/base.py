from pydantic import BaseModel, field_validator
from typing import List, Literal

# Neste esquema, temos a validação das tags que devem começar com '#'
# As tags são armazenadas como ["#tag1","#tag2"] no banco de dados
class OpcaoBase(BaseModel):
    id:int
    texto: str
    tags: List[str]
    
    @field_validator('tags')
    def validar_tags(cls, v):
        if not all(tag.startswith('#') for tag in v):
            raise ValueError("Tags devem começar com '#'")
        return v


class PerguntaBase(BaseModel):
    texto: str
    tipo: Literal['radio', 'checkbox']