from __future__ import annotations

__all__ = ['OpcaoModel']  # Lista explícita de exportações

# src/models/__init__.py
from .base import BaseModel
from .categoria import CategoriaModel
from .questionario import OpcaoModel, PerguntaModel, QuestionarioModel, RespostaModel
from .usuario import UsuarioModel

__all__ = [
    'BaseModel',
    'CategoriaModel',
    'PerguntaModel',
    'QuestionarioModel',
    'RespostaModel',
    'UsuarioModel',
    'OpcaoModel',
    'OutroModel',
]  # Exportações públicas
