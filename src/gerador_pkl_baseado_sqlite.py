from __future__ import annotations

import csv
import pickle

from models.categoria import CategoriaModel
from models.categoria import TarefaModel
from sqlalchemy.orm import Session

from database.database import engine


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


def criar_csv_database():
    """Exporta os dados do banco para um arquivo CSV"""
    nome_arquivo: str = 'dataset_tarefas.csv'

    db = Session(engine)

    try:
        # Obter os dados do banco
        dataset = obter_dataset(db)

        # Criar e escrever o arquivo CSV
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv)

            # Escrever cabeçalho
            writer.writerow(['tarefa', 'categoria'])

            # Escrever linhas de dados
            for tarefa, categoria in zip(dataset.tarefa, dataset.categoria):
                writer.writerow([tarefa, categoria])

        print(f"Dados exportados com sucesso para {nome_arquivo}")

    except Exception as e:
        print(f"Erro ao exportar para CSV: {str(e)}")
    finally:
        db.close()


def criar_pkl_database():

    nome_arquivo: str = 'dataset_tarefas.pkl'

    db = Session(engine)

    # Usando sua função existente para obter os dados
    dataset = obter_dataset(db)

    # Criar um dicionário com a estrutura desejada
    dados_para_exportar = {'tarefa': dataset.tarefa, 'categoria': dataset.categoria}

    # Salvar no arquivo PKL
    with open(nome_arquivo, 'wb') as arquivo:
        pickle.dump(dados_para_exportar, arquivo)


# Criando o arquivo para preparação do colab
criar_pkl_database()
criar_csv_database()
