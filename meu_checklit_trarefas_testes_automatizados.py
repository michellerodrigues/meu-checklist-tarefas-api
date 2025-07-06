import pytest
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

# Carrega o modelo salvo

componente_modelo = joblib.load('modelo_completo.joblib')
modelo = componente_modelo['melhor_modelo_individual']
le = componente_modelo['label_encoder']

TEST_CASES = [
    # (tarefa, categoria_esperada)
    ('Montar Sistema e Irrigação das Plantas', 'Cuidados com Plantas'),
    ('regar as plantas', 'Cuidados com Plantas'),
    ('trocar fralda de bebê', 'Cuidados com Bebês Recém-Nascidos'),
    ('Limpar a caixa de areia do gato', 'Cuidados com Animais de Estimação'),
    ('Cortar as unhas do gato', 'Cuidados com Animais de Estimação'),
    ('Lavar o chão do box', 'Limpeza do Banheiro')
]

# Requisitos de desempenho
REQUISITOS = {
    'acuracia_minima': 0.85,  # 80% de acurácia
    'f1_score_minimo': 0.80,  # F1-score mínimo
    'threshold_confianca': 0.45  # Limite de confiança para previsão
}

@pytest.fixture
def loaded_model():
    """Fixture para carregar o modelo uma vez para todos os testes"""
    return modelo, le

def test_acuracia_geral(loaded_model):
    """Testa se a acurácia geral está acima do limite mínimo"""
    modelo, le = loaded_model
    
    # Prepara dados de teste
    X_test = [case[0] for case in TEST_CASES]
    y_true = [case[1] for case in TEST_CASES]
    y_true_encoded = le.transform(y_true)
    
    # Faz previsões
    y_pred_encoded = modelo.predict(X_test)
    acuracia = accuracy_score(y_true_encoded, y_pred_encoded)
    
    assert acuracia >= REQUISITOS['acuracia_minima'], \
        f"Acurácia {acuracia:.2f} abaixo do mínimo {REQUISITOS['acuracia_minima']}"

def test_f1_score(loaded_model):
    """Testa se o F1-score está acima do limite mínimo"""
    modelo, le = loaded_model
    
    X_test = [case[0] for case in TEST_CASES]
    y_true = [case[1] for case in TEST_CASES]
    y_true_encoded = le.transform(y_true)
    y_pred_encoded = modelo.predict(X_test)
    
    f1 = f1_score(y_true_encoded, y_pred_encoded, average='weighted')
    
    assert f1 >= REQUISITOS['f1_score_minimo'], \
        f"F1-score {f1:.2f} abaixo do mínimo {REQUISITOS['f1_score_minimo']}"

def test_confianca_previsoes(loaded_model):
    """Testa se as previsões têm confiança mínima"""
    modelo, _ = loaded_model
    
    X_test = [case[0] for case in TEST_CASES]
    probas = modelo.predict_proba(X_test)
    confiancas = np.max(probas, axis=1)
    
    assert all(confiancas >= REQUISITOS['threshold_confianca']), \
        f"Algumas previsões têm confiança abaixo de {REQUISITOS['threshold_confianca']}"

def test_previsoes_especificas(loaded_model):
    """Testa previsões específicas para casos conhecidos"""
    modelo, le = loaded_model
    
    for tarefa, categoria_esperada in TEST_CASES:
        categoria_predita = le.inverse_transform(modelo.predict([tarefa]))[0]
        assert categoria_predita == categoria_esperada, \
            f"Erro na tarefa '{tarefa}': esperado '{categoria_esperada}', obtido '{categoria_predita}'"

def test_metadados_modelo():
    """Verifica se os metadados do modelo estão completos"""
    assert 'metadata' in componente_modelo, "Metadados não encontrados no modelo salvo"
    meta = componente_modelo['metadata']
    
    assert 'melhor_modelo' in meta, "Melhor Modelo não especificado nos metadados"
    assert 'data_treinamento' in meta, "Data de treinamento não especificada"
    
