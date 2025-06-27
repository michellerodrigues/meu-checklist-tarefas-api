from typing import Any

from sklearn.calibration import LabelEncoder


class ConjuntoTreinamento:
    def __init__(self):
        self.le = LabelEncoder
        self.X_train = Any
        self.X_test = Any
        self.y_train = Any
        self.y_test = Any
          
