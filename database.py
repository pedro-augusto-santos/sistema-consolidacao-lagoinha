from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Pega a URL de conexão que está no .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a "engine" - o objeto que sabe se conectar ao banco
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões - cada sessão é uma "conversa" com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que nossas tabelas (models) vão herdar
Base = declarative_base()