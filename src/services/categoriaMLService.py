from __future__ import annotations

import gc

import joblib
import pandas as pd
from fastapi import HTTPException
from fastapi import status
from models.categoria import CategoriaModel
from models.categoria import TarefaModel
from schemas.conjunto_treinamento import ConjuntoTreinamento
from schemas.datasetTarefas import DatasetTarefas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sqlalchemy.orm import Session

from database.database import engine


class CategoriaMLService:
    def __init__(self):
        self._db = None
        self.dataframe = None
        self.modelo = None
        self.conjuntoTreinamento = None
        self.stop_words_custom = None
        self._initialize_service()

    def _initialize_service(self):
        """Inicializa todos os componentes do serviço"""
        try:
            self._liberar_memoria()

            # Lista customizada de stop words em português
            self.stop_words_custom = [
                'a',
                'o',
                'e',
                'é',
                'de',
                'do',
                'da',
                'em',
                'um',
                'uma',
                'os',
                'as',
                'ao',
                'à',
                'para',
                'por',
                'com',
                'não',
                'se',
                'que',
                'como',
                'mas',
                'meu',
                'minha',
                'em',
                'num',
                'dum',
            ]

            print('Obtendo dados do banco...')
            self.dataframe = self._set_dataFrame()
            print(f"Dados obtidos com sucesso. Shape: {self.dataframe.shape}")

            print('Preparando conjunto de treinamento...')
            self.conjuntoTreinamento = self._set_conjunto_treinamento()
            print('Conjunto de treinamento preparado')

            print('Treinando modelo...')
            self.modelo = self._set_modelo()
            print('Modelo treinado com sucesso')

            # Verificação final mais robusta
            if not isinstance(self.dataframe, pd.DataFrame):
                raise ValueError('DataFrame não foi criado corretamente')

            if not isinstance(self.conjuntoTreinamento, ConjuntoTreinamento):
                raise ValueError('Conjunto de treinamento não foi criado corretamente')

            # VERIFICAÇÃO CORRIGIDA AQUI
            if not hasattr(self.modelo.steps[-1][1], 'predict'):
                raise ValueError('O modelo final não tem método predict')

            # Verificação adicional do pipeline
            if not isinstance(self.modelo, Pipeline):
                raise ValueError('O modelo não é um Pipeline válido')

            print('Verificações de modelo concluídas com sucesso')
        except Exception as e:
            if self._db:
                self._db.rollback()
            print(f"ERRO durante inicialização: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Falha ao inicializar serviço de ML: {str(e)}",
            ) from e
        finally:
            if self._db:
                self._db.close()
            print('Conexão com o banco fechada')

    def _liberar_memoria(self):
        gc.collect()

    def _set_dataFrame(self) -> pd.DataFrame:
        """Cria o DataFrame a partir do banco de dados"""
        try:
            self._db = Session(engine)
            resultados = (
                self._db.query(TarefaModel.descricao, CategoriaModel.nome)
                .join(CategoriaModel, TarefaModel.categoria_id == CategoriaModel.id)
                .all()
            )

            if not resultados:
                raise ValueError('Nenhum dado encontrado no banco de dados')

            dataset = DatasetTarefas()
            dataset.tarefa = [r.descricao for r in resultados]
            dataset.categoria = [r.nome for r in resultados]

            df = pd.DataFrame(dataset.to_dict())

            # Verificação adicional
            if df.empty:
                raise ValueError('DataFrame criado está vazio')
            if 'categoria' not in df.columns or 'tarefa' not in df.columns:
                raise ValueError('DataFrame não contém as colunas esperadas')

            return df
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Não foi possível gerar o dataset: {str(e)}",
            ) from e

    def get_relatorio_classificacao(self) -> dict:
        """Gera relatório de classificação do modelo"""
        if not self.modelo or not self.conjuntoTreinamento:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Modelo não foi treinado corretamente',
            )

        y_pred = self.modelo.predict(self.conjuntoTreinamento.X_test)
        all_classes = self.conjuntoTreinamento.label_encoder.transform(
            self.conjuntoTreinamento.label_encoder.classes_,
        )

        return classification_report(
            self.conjuntoTreinamento.y_test,
            y_pred,
            zero_division=0,
            labels=all_classes,
            target_names=self.conjuntoTreinamento.label_encoder.classes_,
            output_dict=True,
        )

    def _set_conjunto_treinamento(self) -> ConjuntoTreinamento:
        """Prepara os dados para treinamento"""
        if self.dataframe is None:
            raise ValueError('DataFrame não foi carregado corretamente')

        le = LabelEncoder()
        self.dataframe['categoria_encoded'] = le.fit_transform(
            self.dataframe['categoria'],
        )

        X_train, X_test, y_train, y_test = train_test_split(
            self.dataframe['tarefa'],
            self.dataframe['categoria_encoded'],
            test_size=0.2,
            random_state=42,
            stratify=self.dataframe['categoria_encoded'],
        )

        return ConjuntoTreinamento(
            label_encoder=le,
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
        )

    def _set_modelo(self):
        """Configura e treina o modelo de machine learning"""
        try:

            print('Criando pipeline TF-IDF + Naive Bayes...')
            # Criação do pipeline
            pipeline = make_pipeline(
                TfidfVectorizer(stop_words=self.stop_words_custom),
                MultinomialNB(alpha=0.1),
            )

            # Verificação imediata
            if not hasattr(pipeline, 'predict'):
                raise ValueError('Pipeline não foi criado corretamente')

            print('Iniciando treinamento do modelo...')
            # Treinamento
            pipeline.fit(
                self.conjuntoTreinamento.X_train,
                self.conjuntoTreinamento.y_train,
            )

            # Verificação do treinamento
            if not hasattr(pipeline, 'classes_'):
                raise ValueError('Modelo não foi treinado corretamente classes_')

            print(f"Modelo treinado com {len(pipeline.classes_)} classes")

            if self.conjuntoTreinamento is None:
                raise ValueError(
                    'Conjunto de treinamento não foi carregado corretamente',
                )

                # Teste predição simples
            try:
                sample_pred = pipeline.predict(
                    [self.conjuntoTreinamento.X_train.iloc[0]],
                )
                if not sample_pred.size:
                    raise ValueError('Predição teste falhou')
            except Exception as e:
                raise ValueError(f"Teste de predição falhou: {str(e)}")

            return pipeline

        except Exception as e:
            print(f"Erro durante criação do modelo: {str(e)}")
            raise

    def prever_categoria(self, tarefa: str, threshold: float = 0.05) -> str:
        """Faz a predição da categoria para uma nova tarefa"""
        try:
            if not hasattr(self, 'modelo') or self.modelo is None:
                print('Modelo não está inicializado')  # Debug
                raise ValueError('Modelo não está inicializado')

            if (
                not hasattr(self, 'conjuntoTreinamento')
                or self.conjuntoTreinamento is None
            ):
                print('Conjunto de treinamento não está inicializado')  # Debug
                raise ValueError('Conjunto de treinamento não está inicializado')

            probas = self.modelo.predict_proba([tarefa])[0]
            max_proba = max(probas)

            if max_proba < threshold:
                return 'Outros'

            encoded = self.modelo.predict([tarefa])[0]
            return self.conjuntoTreinamento.label_encoder.inverse_transform([encoded])[
                0
            ]

        except Exception as e:
            print(f"Erro durante predição: {str(e)}")  # Log adicional
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao prever categoria: {str(e)}",
            )

    def salvar_modelo(self, caminho: str = 'joblib/modelo_tarefas.joblib'):
        """Salva o modelo treinado em um arquivo"""
        if not all([self.dataframe, self.modelo, self.conjuntoTreinamento]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Componentes necessários não estão disponíveis',
            )

        to_persist = {
            'dataframe': self.dataframe,
            'model': self.modelo,
            'label_encoder': self.conjuntoTreinamento.label_encoder,
            'metadata': {
                'created_at': pd.Timestamp.now(),
                'version': '1.0',
                'description': 'Modelo de classificação meu checklist tarefas',
            }            
        }
        joblib.dump(to_persist, caminho)
