import json
from typing import List

from schemas.categoria import CarregaPainelUsuarioResponse, TarefaUsuario
from models.categoria import CategoriaModel
from models import OpcaoModel, PerguntaModel

class OpcaoConverter:
    @staticmethod
    def to_schema(opcao: OpcaoModel, questionario_id: int) -> dict:
        return {
            "id": opcao.id,
            "texto": opcao.texto,
            "tags": json.loads(opcao.tags),
            "selecionada": any(
                r.questionario_id == questionario_id
                for r in opcao.respostas
            )
        }

class PerguntaConverter:
    @staticmethod
    def to_schema(pergunta: PerguntaModel, questionario_id: int) -> dict:
        return {
            "texto": pergunta.texto,
            "tipo": pergunta.tipo,
            "opcoes": [
                OpcaoConverter.to_schema(opcao, questionario_id)
                for opcao in pergunta.opcoes
            ]
        }
    
class QuestionarioConverter:
    @staticmethod
    def to_schema(perguntas: object, questionario_id: int) -> dict:      
        
        perguntas = perguntas.scalars().all()    

        return {
            "id": questionario_id,
            "perguntas": [
                PerguntaConverter.to_schema(pergunta,questionario_id)
                for pergunta in perguntas
            ]
        }
    
class CategoriaConverter:
    @staticmethod
    def to_schema(categoriaModel: List[CategoriaModel]) ->List[CarregaPainelUsuarioResponse]:      
        
        painelTarefasResponse = []

        for categoria in categoriaModel:
            categoriaResponse = CarregaPainelUsuarioResponse(categoria = categoria.nome, tarefas=[])
            for tarefaUser in categoria.tarefas:                
                tarefaUsuario = TarefaUsuario(id = tarefaUser.id, descricao=tarefaUser.descricao, recorrencia = tarefaUser.recorrencia.descricao, tags = CategoriaConverter.ajustarTags(tarefaUser.tags))
                categoriaResponse.tarefas.append(tarefaUsuario)
            painelTarefasResponse.append(categoriaResponse)
        return painelTarefasResponse
    

    @staticmethod
    def ajustarTags(tags:str) -> List[str]:      
        try:
            return json.loads(tags) if tags else []
        except Exception:
            return []
        
        