from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.autenticacao import router as autenticacao_router
from routers.categorias import router as categorias_router
from routers.questionario import router as questionario_router

app = FastAPI(
    docs_url='/meu-checklist-tarefas-doc',
    title='Meu CheckList de Tarefas',
    description=(
        'Simplifique sua vida, '
        'compartilhe responsabilidades e '
        'ganhe tempo para o que mais importa'
    ),
    version='1.0.0',
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8005'],  # Ou "*" para permitir todas
    allow_credentials=True,
    allow_methods=['*'],  # Ou ["GET", "POST", ...]
    allow_headers=['*'],
)

# Registrar rotas
app.include_router(autenticacao_router, prefix='/api')
app.include_router(questionario_router, prefix='/api')
app.include_router(categorias_router, prefix='/api')


@app.get('/')
def root():

    mensagem = (
        "Bem-vindo à API 'Meu CheckList de Tarefas': "
        'Simplifique sua vida, '
        'compartilhe responsabilidades ',
        'e ganhe tempo para o que mais importa.',
    )

    return {'message': mensagem}
