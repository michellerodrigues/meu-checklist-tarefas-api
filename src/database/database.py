from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists

# url de acesso ao banco (essa é uma url de acesso ao sqlite local
DB_PATH = 'src/database'


# Verifica se o diretorio não existe
if not os.path.exists(DB_PATH):
    # então cria o diretorio
    os.makedirs(DB_PATH)


# Configuração do SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}/banco_tarefas.sqlite3"  # SQLite local

# cria a engine de conexão com o banco
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    echo=True,
)

# Instancia um criador de seção com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
