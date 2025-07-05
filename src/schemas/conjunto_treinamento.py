from __future__ import annotations

from dataclasses import dataclass

from pandas import Series
from sklearn.preprocessing import LabelEncoder


@dataclass
class ConjuntoTreinamento:
    """Armazena os dados de treinamento e o label encoder"""

    label_encoder: LabelEncoder
    X_train: Series
    X_test: Series
    y_train: Series
    y_test: Series
