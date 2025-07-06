
from __future__ import annotations

from models.categoria import CategoriaModel
from models.categoria import TarefaModel
from database.database import engine

from sqlalchemy.orm import Session
import pickle



class DatasetTarefas:
    def __init__(self):
        self.tarefa = []
        self.categoria = []

    def to_dict(self):
        return {'tarefa': self.tarefa, 'categoria': self.categoria}


def obter_dataset(db: Session) -> DatasetTarefas:
    resultados = (
        db.query(TarefaModel.descricao, CategoriaModel.nome)
        .join(CategoriaModel, TarefaModel.categoria_id == CategoriaModel.id)
        .all()
    )

    dataset = DatasetTarefas()

    dataset.tarefa = [r.descricao for r in resultados]
    dataset.categoria = [r.nome for r in resultados]

    return dataset


def criar_pkl_database():
    
    nome_arquivo: str = 'dataset_tarefas.pkl'

    db = Session(engine)

    # Usando sua função existente para obter os dados
    dataset = obter_dataset(db)
    
    # Criar um dicionário com a estrutura desejada
    dados_para_exportar = {
        'tarefa': dataset.tarefa,
        'categoria': dataset.categoria
    }
    
    # Salvar no arquivo PKL
    with open(nome_arquivo, 'wb') as arquivo:
        pickle.dump(dados_para_exportar, arquivo)

#Criando o arquivo para preparação do colab

criar_pkl_database()

