from __future__ import annotations

import gc

import joblib
import pandas as pd
from fastapi import HTTPException
from fastapi import status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sqlalchemy.orm import Session

from src.database.database import engine
from src.models.categoria import CategoriaModel
from src.models.categoria import TarefaModel
from src.schemas import ConjuntoTreinamento
from src.schemas.datasetTarefas import DatasetTarefas


class CategoriaMLService:

    def __init__(self):
        self.dataframe = self._set_dataFrame()
        self.modelo = self._set_modelo()
        self.conjuntoTreinamento = self._set_conjunto_treinamento()

    def _liberar_memoria():
        gc.collect()

    def _set_dataFrame(self):

        try:

            db = Session(engine)

            resultados = (
                db.query(TarefaModel.descricao, CategoriaModel.nome)
                .join(CategoriaModel, TarefaModel.categoria_id == CategoriaModel.id)
                .all()
            )

            dataset = DatasetTarefas()

            dataset.tarefa = [r.descricao for r in resultados]
            dataset.categoria = [r.nome for r in resultados]

            self.dataFrame = pd.DataFrame(dataset.to_dict())

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Não foi possível gerar o dataset: {str(e)}",
            ) from e

    def get_relatorio_classificacao(self) -> dict:

        y_pred = self.modelo.predict(self.conjuntoTreinamento.X_test)

        all_classes = self.conjuntoTreinamento.le.transform(
            self.conjuntoTreinamento.le.classes_,
        )  # Pega todas as classes do LabelEncoder

        return classification_report(
            self.conjuntoTreinamento.y_test,
            y_pred,
            zero_division=0,  # Define precisão/recall como 0 quando não há amostras
            labels=all_classes,
            target_names=self.conjuntoTreinamento.le.classes_,
        )

    def _set_conjunto_treinamento(self) -> ConjuntoTreinamento:

        le = LabelEncoder()
        self.dataframe['categoria_encoded'] = le.fit_transform(
            self.dataframe['categoria'],
        )

        # Dividir em treino e teste (80% treino, 20% teste)
        X_train, X_test, y_train, y_test = train_test_split(
            self.dataframe['tarefa'],
            self.dataframe['categoria_encoded'],
            test_size=0.2,
            random_state=42,
        )

        conjuntoTreinamento = ConjuntoTreinamento(le, X_train, X_test, y_train, y_test)
        return conjuntoTreinamento

    def _set_modelo(self):

        self.dataset = self._obter_dataset()

        self._liberar_memoria()

        self.conjuntoTreinamento = self._pre_processamento_target(self.dataset)

        self.modelo = make_pipeline(TfidfVectorizer(), MultinomialNB())

        # Treinar o modelo
        self.modelo.fit(
            self.conjuntoTreinamento.X_train,
            self.conjuntoTreinamento.y_train,
        )

    # Função para prever categoria de novas tarefas
    """def prever_categoria(self, tarefa):
        encoded = self.modelo.predict([tarefa])[0]
        return self.conjuntoTreinamento.le.inverse_transform([encoded])[0]"""

    def prever_categoria(self, tarefa, threshold=0.05):
        # Obtém as probabilidades para todas as classes
        probas = self.modelo.predict_proba([tarefa])[0]
        max_proba = max(probas)

        print(f"probabilidade max {max_proba}")
        # Se a probabilidade máxima for menor que o threshold, retorna categoria default
        if max_proba < threshold:
            return 'Outros'  # Ou qualquer nome que você queira para a categoria default

        # Caso contrário, retorna a categoria com maior probabilidade
        encoded = self.modelo.predict([tarefa])[0]
        return self.conjuntoTreinamento.le.inverse_transform([encoded])[0]

    def _criar_joblib(self):
        to_persist = {
            'dataframe': self.dataFrame,
            'model': self.modelo,
            'label_encoder': self.conjuntoTreinamento.le,
            'metadata': {
                'created_at': pd.Timestamp.now(),
                'version': '1.0',
                'description': 'Modelo de classificação meu checklist tarefas',
            },
        }
        joblib.dump(to_persist, 'joblib/modelo_tarefas.joblib')
