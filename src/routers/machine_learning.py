import pandas as pd
import time
from sklearn.preprocessing import LabelEncoder

# Dataset de exemplo com tarefas e categorias
data = {
    'tarefa': [
        'Regar as plantas do jardim',
        'Limpar a caixa de areia do gato',
        'Fazer compras no mercado',
        'Organizar os brinquedos das crianças',
        'Trocar a areia do hamster',
        'Pagar as contas online',
        'Podar as roseiras',
        'Levar o cachorro para passear',
        'Preparar o lanche da escola',
        'Aspirar o tapete da sala', 
        'pintar o cabelo',
        'manicure',
        'pedicure'
    ],
    'categoria': [
        'jardinagem',
        'pets',
        'compras',
        'organizacao',
        'pets',
        'financas',
        'jardinagem',
        'pets',
        'familia',
        'limpeza',
        'cuidados pessoais',
        'cuidados pessoais',
        'cuidados pessoais'
    ]
}

import gc
# ---- LIMPEZA INICIAL ---- #
# 1. Liberar memória
gc.collect()

import os
os.system('cls' if os.name == 'nt' else 'clear')  # Limpa o terminal

# Tempo inicial
tempo_inicial_dataframe = time.time()
print("Criando Dataframe....INICIO:", tempo_inicial_dataframe)

# Criar DataFrame
df = pd.DataFrame(data.copy())  # Usar .copy() para evitar referências

# Tempo final
tempo_final_dataframe = time.time()
print("Criando Dataframe....FIM:", tempo_final_dataframe)

# Diferença de tempo
print("Tempo decorrido para criacao de Dataframe:", tempo_final_dataframe - tempo_inicial_dataframe, "segundos")


tempo_inicial_prepropocessamento = time.time()
print("Criando Pré-processamento....INICIO:", tempo_inicial_prepropocessamento)
# Pré-processamento do target
le = LabelEncoder()
df['categoria_encoded'] = le.fit_transform(df['categoria'])

tempo_final_prepropocessamento = time.time()
print("Criando Pré-processamento....FIM:", tempo_final_prepropocessamento)

# Diferença de tempo
print("Tempo decorrido para Pré-processamento:", tempo_final_prepropocessamento - tempo_inicial_prepropocessamento, "segundos")

tempo_inicio_impressao = time.time()
print("Preparando Impressão....INICIO:", tempo_inicio_impressao)

print(df.head())

tempo_final_impressao = time.time()
print("Impressão....FIM:", tempo_final_impressao)

# Diferença de tempo
print("Tempo decorrido para Impressao:", tempo_final_impressao - tempo_inicio_impressao, "segundos")

# Diferença de tempo
print("Tempo Total Processamento:", tempo_final_impressao - tempo_inicial_dataframe, "segundos")

print("Hash do DataFrame:", hash(pd.util.hash_pandas_object(df).sum()))