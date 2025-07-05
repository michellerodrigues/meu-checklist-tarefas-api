from __future__ import annotations

import json

from models.categoria import CategoriaModel
from models.questionario import OpcaoModel
from models.questionario import PerguntaModel
from .categoria import CarregaCategoriaComboResponse, CarregaPainelUsuarioResponse, CategoriaCombo
from .categoria import TarefaUsuario


class OpcaoConverter:
    """
    Neste módulo, temos os conversoes do modelo para o retorno da api
    par que o modelo consiga conversar com o frontend sem causar acoplamento

    """

    @staticmethod
    def to_schema(opcao: OpcaoModel, questionario_id: int) -> dict:
        return {
            'id': opcao.id,
            'texto': opcao.texto,
            'tags': json.loads(opcao.tags),
            'selecionada': any(
                r.questionario_id == questionario_id for r in opcao.respostas
            ),
        }


class PerguntaConverter:
    @staticmethod
    def to_schema(pergunta: PerguntaModel, questionario_id: int) -> dict:
        return {
            'texto': pergunta.texto,
            'tipo': pergunta.tipo,
            'opcoes': [
                OpcaoConverter.to_schema(opcao, questionario_id)
                for opcao in pergunta.opcoes
            ],
        }


class QuestionarioConverter:
    @staticmethod
    def to_schema(perguntas: object, questionario_id: int) -> dict:

        perguntas = perguntas.scalars().all()

        return {
            'id': questionario_id,
            'perguntas': [
                PerguntaConverter.to_schema(pergunta, questionario_id)
                for pergunta in perguntas
            ],
        }


class CategoriaConverter:
    @staticmethod
    def to_schema(
        categoria_model: list[CategoriaModel],
    ) -> list[CarregaPainelUsuarioResponse]:

        painel_tarefas_response = []

        for categoria in categoria_model:
            categoria_response = CarregaPainelUsuarioResponse(
                categoria=categoria.nome,
                tarefas=[],
            )
            for tarefa in categoria.tarefas:
                tarefa_usuario = TarefaUsuario(
                    id=tarefa.id,
                    descricao=tarefa.descricao,
                    recorrencia=tarefa.recorrencia.descricao,
                    tags=CategoriaConverter.ajustar_tags(tarefa.tags),
                )
                categoria_response.tarefas.append(tarefa_usuario)
            painel_tarefas_response.append(categoria_response)
        return painel_tarefas_response

    @staticmethod
    def ajustar_tags(tags: str) -> list[str]:
        try:
            return json.loads(tags) if tags else []  # noqa: W0718
        except Exception:
            return []
    
    @staticmethod
    def to_categoria_combo(
        categoria_model: list[CategoriaModel], categoria_ia:CategoriaModel,
    ) -> CarregaCategoriaComboResponse:
        
        comboCategoria = CarregaCategoriaComboResponse()

        for categoria in categoria_model:
            cat = CategoriaCombo(id=categoria.id, descricao=categoria.nome, selecionado=False)
            
            if categoria_ia.nome==categoria.nome:
                cat.selecionado = True
                
            comboCategoria.categorias.append(cat)
        
        return comboCategoria
