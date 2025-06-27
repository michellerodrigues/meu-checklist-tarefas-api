from __future__ import annotations

import time
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.database import engine
from models.categoria import CategoriaModel
from models.categoria import TarefaModel


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


db = Session(engine)

# Dataset de exemplo com tarefas e categorias
dataset = obter_dataset(db)

import gc

# ---- LIMPEZA INICIAL ---- #
# 1. Liberar memória
gc.collect()

import os

os.system('cls' if os.name == 'nt' else 'clear')  # Limpa o terminal

# Tempo inicial
tempo_inicial_dataframe = time.time()
print('Criando Dataframe....INICIO:', tempo_inicial_dataframe)

# Criar DataFrame
df = pd.DataFrame(dataset.to_dict())


# Tempo final
tempo_final_dataframe = time.time()
print('Criando Dataframe....FIM:', tempo_final_dataframe)

# Diferença de tempo
print(
    'Tempo decorrido para criacao de Dataframe:',
    tempo_final_dataframe - tempo_inicial_dataframe,
    'segundos',
)


tempo_inicial_prepropocessamento = time.time()
print('Criando Pré-processamento....INICIO:', tempo_inicial_prepropocessamento)
# Pré-processamento do target
le = LabelEncoder()
df['categoria_encoded'] = le.fit_transform(df['categoria'])

# Dividir em treino e teste (80% treino, 20% teste)
X_train, X_test, y_train, y_test = train_test_split(
    df['tarefa'], df['categoria_encoded'], test_size=0.2, random_state=42,
)

# Criar pipeline com vetorização TF-IDF e modelo Naive Bayes
#model = make_pipeline(TfidfVectorizer(), MultinomialNB())

import nltk
from nltk.corpus import stopwords
from sklearn.pipeline import make_pipeline

nltk.download('stopwords')

# Carrega stop words
stop_words_pt = stopwords.words('portuguese')

"""ngram_range=(1, 3),  # Captura frases completas
        max_df=0.85,         # Ignora palavras muito frequentes
        min_df=2,            # Ignora palavras muito raras
        stop_words=stop_words_pt"""


model = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB()
)


# Treinar o modelo
model.fit(X_train, y_train)

# Todas as classes que o modelo conhece (mesmo que não apareçam no teste)
all_classes = le.transform(le.classes_)  # Pega todas as classes do LabelEncoder

# Avaliar no conjunto de teste
y_pred = model.predict(X_test)
print('\nRelatório de classificação:')
print(classification_report(
    y_test, 
    y_pred,
    zero_division=0,  # Define precisão/recall como 0 quando não há amostras
    labels=all_classes, 
    target_names=le.classes_))


# Função para prever categoria de novas tarefas
"""def prever_categoria(tarefa):
    encoded = model.predict([tarefa])[0]
    return le.inverse_transform([encoded])[0] """

def prever_categoria(tarefa, threshold=0.50):
    # Obtém as probabilidades para todas as classes
    probas = model.predict_proba([tarefa])[0]
    max_proba = max(probas)
    
    print(f"probabilidade max {max_proba}")
    # Se a probabilidade máxima for menor que o threshold, retorna categoria default
    if max_proba < threshold :
        return "Outros"  # Ou qualquer nome que você queira para a categoria default
    
    # Caso contrário, retorna a categoria com maior probabilidade
    encoded = model.predict([tarefa])[0]
    return le.inverse_transform([encoded])[0]


# Exemplo de uso
nova_tarefa = 'substituir escovas de dente'
print(
    f"\nA tarefa '{nova_tarefa}' pertence à categoria: {prever_categoria(nova_tarefa)}",
)

nova_tarefa = 'instalar sistema de irrigação'
print(f"A tarefa '{nova_tarefa}' pertence à categoria: {prever_categoria(nova_tarefa)}")

nova_tarefa = 'organizar calendário de provas'
print(f"A tarefa '{nova_tarefa}' pertence à categoria: {prever_categoria(nova_tarefa)}")


tempo_final_prepropocessamento = time.time()
print('Criando Pré-processamento....FIM:', tempo_final_prepropocessamento)

# Diferença de tempo
print(
    'Tempo decorrido para Pré-processamento:',
    tempo_final_prepropocessamento - tempo_inicial_prepropocessamento,
    'segundos',
)

tempo_inicio_impressao = time.time()
print('Preparando Impressão....INICIO:', tempo_inicio_impressao)

# print(df.head())
print(df)

tempo_final_impressao = time.time()
print('Impressão....FIM:', tempo_final_impressao)

# Diferença de tempo
print(
    'Tempo decorrido para Impressao:',
    tempo_final_impressao - tempo_inicio_impressao,
    'segundos',
)

# Diferença de tempo
print(
    'Tempo Total Processamento:',
    tempo_final_impressao - tempo_inicial_dataframe,
    'segundos',
)

print('Hash do DataFrame:', hash(pd.util.hash_pandas_object(df).sum()))

# Dados para salvar (crie um dicionário com tudo que você quer persistir)
to_persist = {
    'dataframe': df,
    'model': model,
    'label_encoder': le,
    'metadata': {
        'created_at': pd.Timestamp.now(),
        'version': '1.0',
        'description': 'Modelo de classificação de tarefas domésticas',
    },
}

# Salvar tudo em um único arquivo
joblib.dump(to_persist, 'modelo_tarefas.joblib')

print("DataFrame e modelo salvos com sucesso em 'modelo_tarefas.joblib'")
