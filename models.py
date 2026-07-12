from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamento: um usuário pode ter vários "novos começos" registrados
    novos_comecos = relationship("NovoComeco", back_populates="usuario")

class NovoComeco(Base):
    __tablename__ = "novos_comecos"

    id = Column(Integer, primary_key=True, index=True)
    nome_pessoa = Column(String, nullable=False)
    telefone = Column(String,nullable=False)
    data_decisao = Column(DateTime)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Relacionamento: um novo começo só pode ter um usuário registrado (relacionamento estilo pai pra filho)
    usuario = relationship("Usuario", back_populates="novos_comecos")

