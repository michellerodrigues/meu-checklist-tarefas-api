from __future__ import annotations

import pickle


import time

import joblib
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
from sklearn.ensemble import VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier



# Configurações iniciais
nltk.download('stopwords')
stop_words_pt = stopwords.words('portuguese')


class DatasetTarefas:
    def __init__(self):
        self.tarefa = []
        self.categoria = []

    def to_dict(self):
        return {'tarefa': self.tarefa, 'categoria': self.categoria}


def obter_dataset() -> DatasetTarefas:
    """Obtém o dataset do arquivo PKL. O parâmetro db é mantido para compatibilidade, mas não é usado."""
    dataset = DatasetTarefas()
    
    try:
        with open('dataset_tarefas.pkl', 'rb') as arquivo:
            dados = pickle.load(arquivo)
            
            dataset.tarefa = dados['tarefa']
            dataset.categoria = dados['categoria']
    except FileNotFoundError:
        raise Exception("Arquivo .pkl não encontrado.")
    
    return dataset

dataset = obter_dataset()

# Criação do DataFrame
print('\nCriando DataFrame...')
df = pd.DataFrame(dataset.to_dict())

# Pré-processamento
print('\nPré-processamento dos dados...')
le = LabelEncoder()
df['categoria_encoded'] = le.fit_transform(df['categoria'])

# Divisão treino-teste
X_train, X_test, y_train, y_test = train_test_split(
    df['tarefa'],
    df['categoria_encoded'],
    test_size=0.2,
    random_state=42,
    stratify=df['categoria_encoded'],
)


# Função para avaliar modelos
def evaluate_model(model, X_train, y_train, X_test, y_test, model_name):
    start_time = time.time()

    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"\n{model_name} - Cross-validation scores: {cv_scores}")
    print(f"{model_name} - Média CV accuracy: {np.mean(cv_scores):.4f}")

    # Treino e teste
    model.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))

    print(f"{model_name} - Acurácia no treino: {train_acc:.4f}")
    print(f"{model_name} - Acurácia no teste: {test_acc:.4f}")

    # Relatório de classificação
    y_pred = model.predict(X_test)
    print(f"\nRelatório de classificação para {model_name}:")
    print(
        classification_report(y_test, y_pred, zero_division=0, target_names=le.classes_),
    )

    print(f"Tempo de execução: {time.time() - start_time:.2f} segundos")

    return {
        'model': model,
        'name': model_name,
        'cv_mean': np.mean(cv_scores),
        'train_acc': train_acc,
        'test_acc': test_acc,
        'time': time.time() - start_time,
    }


# Definindo os modelos
models = [
    (
        'Naive Bayes',
        make_pipeline(TfidfVectorizer(stop_words=stop_words_pt), MultinomialNB()),
    ),
    (
        'KNN',
        make_pipeline(
            TfidfVectorizer(stop_words=stop_words_pt),
            StandardScaler(with_mean=False),  # TF-IDF produz matriz esparsa
            KNeighborsClassifier(),
        ),
    ),
    (
        'Árvore de Decisão',
        make_pipeline(
            TfidfVectorizer(stop_words=stop_words_pt),
            DecisionTreeClassifier(random_state=42),
        ),
    ),
    (
        'SVM',
        make_pipeline(
            TfidfVectorizer(stop_words=stop_words_pt),
            StandardScaler(with_mean=False),
            SVC(probability=True, random_state=42),
        ),
    ),
]

# Otimização de hiperparâmetros para cada modelo
param_grids = {
    'Naive Bayes': {'multinomialnb__alpha': [0.1, 0.5, 1.0, 2.0]},
    'KNN': {
        'kneighborsclassifier__n_neighbors': [3, 5, 7],
        'kneighborsclassifier__weights': ['uniform', 'distance'],
    },
    'Árvore de Decisão': {
        'decisiontreeclassifier__max_depth': [None, 10, 20, 30],
        'decisiontreeclassifier__min_samples_split': [2, 5, 10],
    },
    'SVM': {'svc__C': [0.1, 1, 10], 'svc__kernel': ['linear', 'rbf']},
}

# Treinamento e avaliação dos modelos
results = []
best_models = {}

for name, model in models:
    print(f"\n=== Processando modelo: {name} ===")

    # GridSearchCV para otimização de hiperparâmetros
    grid_search = GridSearchCV(model, param_grids[name], cv=5, n_jobs=-1, verbose=1)

    print(f"Otimizando hiperparâmetros para {name}...")
    grid_search.fit(X_train, y_train)

    print(f"Melhores parâmetros para {name}: {grid_search.best_params_}")
    best_model = grid_search.best_estimator_
    best_models[name] = best_model

    # Avaliação do melhor modelo
    result = evaluate_model(
        best_model, X_train, y_train, X_test, y_test, f"{name} (Otimizado)",
    )
    results.append(result)

# Comparação dos modelos
print('\n=== Comparação dos Modelos ===')
comparison = pd.DataFrame(results)
print(comparison[['name', 'cv_mean', 'train_acc', 'test_acc', 'time']])

# Visualização dos resultados
plt.figure(figsize=(10, 6))
sns.barplot(x='name', y='test_acc', data=comparison)
plt.title('Acurácia nos Testes por Modelo')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('comparacao_modelos.png')
plt.close()

# Ensemble com os melhores modelos
print('\nCriando ensemble com os melhores modelos...')
ensemble = VotingClassifier(
    estimators=[(name, model) for name, model in best_models.items()], voting='soft',
)

ensemble_result = evaluate_model(ensemble, X_train, y_train, X_test, y_test, 'Ensemble')
results.append(ensemble_result)


# Função para prever categoria com threshold
def prever_categoria(tarefa, threshold=0.45):
    probas = ensemble.predict_proba([tarefa])[0]
    max_proba = max(probas)

    if max_proba < threshold:
        return 'Outros'

    encoded = ensemble.predict([tarefa])[0]
    return le.inverse_transform([encoded])[0]


# Exemplos de uso
test_cases = [
    'substituir escovas de dente',
    'instalar sistema de irrigação das plantas',
    'organizar calendário de provas',
    'Comprar protetor de colchão para idosos',
    'recarregar o bilhete do metrô',
]

print('\nTestando o modelo ensemble:')
for task in test_cases:
    print(f"A tarefa '{task}' pertence à categoria: {prever_categoria(task)}")

# Salvando o melhor modelo e recursos
to_persist = {
    'model': ensemble,
    'label_encoder': le,
    'vectorizer': best_models['Naive Bayes'].named_steps['tfidfvectorizer'],
    'metadata': {
        'created_at': pd.Timestamp.now(),
        'version': '2.0',
        'description': 'Modelo de classificação de tarefas com ensemble otimizado',
        'performance': comparison.to_dict(),
    },
}

joblib.dump(to_persist, 'melhor_modelo_tarefas.joblib')
print("\nModelo salvo com sucesso em 'melhor_modelo_tarefas.joblib'")
