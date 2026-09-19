from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os

# HASHING DA SENHA 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # FERRAMENTA BCRYPT PARA GERAR HASHES DE SENHAS OU VERIFICAR SE A SENHA CORRESPONDE A UM HASH EXISTENTE

def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha) # PEGA STR SENHA E DEVOLVE UM HASH CORRESPONDENTE QUE SERA ARMAZENADO NO BANCO

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash) # RECEBE A SENHA E O HASH E USA O BCRYPT PARA VERIFICAR SE A SENHA CORRESPONDE AO HASH

SECRET_KEY = os.getenv("SECRET_KEY") # CHAVE USADA PARA ASSINAR JWT
ALGORITHM = os.getenv("ALGORITHM") # PEGA O ALGORITMO DO PAYLOAD
EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # TEMPO DE EXPIRAÇÃO DO TOKEN

def criar_token(dados: dict) -> str:
    payload = dados.copy()
    expira_em = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    payload.update({"exp": expira_em})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

