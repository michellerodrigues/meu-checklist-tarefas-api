from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os


# url de acesso ao banco (essa é uma url de acesso ao sqlite local
db_path = "database"


# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)


# Configuração do SQLAlchemy
SQLALCHEMY_DATABASE_URL = 'sqlite:///%s/banco_tarefas.sqlite3' % db_path # SQLite local

# cria a engine de conexão com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},echo=True)

# Instancia um criador de seção com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
