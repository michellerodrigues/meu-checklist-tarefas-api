from __future__ import annotations

import joblib


def prever_categoriaEnsemble(tarefa, threshold=0.45):
    """Versão otimizada como função"""
    try:
        componente_modelo = joblib.load('modelo_completo.joblib')

        modelo = componente_modelo['ensemble']

        probas = modelo.predict_proba([tarefa])[0]
        max_proba = max(probas)

        if max_proba < threshold:
            return 'Outros'

        label_encoder_modelo = componente_modelo['label_encoder']

        encoded = modelo.predict([tarefa])[0]
        return label_encoder_modelo.inverse_transform([encoded])[0]

    except Exception as e:
        print(f"Erro: {str(e)}")
        return 'Erro mica'


def prever_categoriaNB(tarefa, threshold=0.45):
    """Versão otimizada como função"""
    try:
        componente_modelo = joblib.load('modelo_completo.joblib')

        modelo = componente_modelo['melhor_modelo_individual']

        probas = modelo.predict_proba([tarefa])[0]
        max_proba = max(probas)

        if max_proba < threshold:
            return 'Outros'

        label_encoderNB = componente_modelo['label_encoder']

        encoded = modelo.predict([tarefa])[0]
        return label_encoderNB.inverse_transform([encoded])[0]

    except Exception as e:
        print(f"Erro: {str(e)}")
        return 'Erro mica'


test_cases = [
    'substituir escovas de dente',
    'instalar sistema de irrigação das plantas',
    'organizar calendário de provas',
    'Comprar protetor de colchão para idosos',
    'recarregar o bilhete do metrô',
]

print('\nTestando o modelo carregado:')
for task in test_cases:
    categoriaNB = prever_categoriaNB(task)
    categoriaEnsemble = prever_categoriaEnsemble(task)
    print(
        f"Tarefa: '{task[:30]}...' → Categoria NB: {categoriaNB} ;  → Categoria Ensemble: {categoriaEnsemble} ",
    )
