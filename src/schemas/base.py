from __future__ import annotations

from typing import Literal

from pydantic import BaseModel
from pydantic import field_validator


class OpcaoBase(BaseModel):
    """
    Neste esquema, temos a validação das tags que devem começar com '#'
    As tags são armazenadas como ["#tag1","#tag2"] no banco de dados

    """

    id: int
    texto: str
    tags: list[str]

    @field_validator('tags')
    def validar_tags(self, v):
        if not all(tag.startswith('#') for tag in v):
            raise ValueError("Tags devem começar com '#'")
        return v


class PerguntaBase(BaseModel):
    texto: str
    tipo: Literal['radio', 'checkbox']
