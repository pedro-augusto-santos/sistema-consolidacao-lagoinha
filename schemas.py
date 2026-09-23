from datetime import datetime
from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class NovoComecoCreate(BaseModel):
    nome: str
    telefone: str
    

class NovoComecoResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    usuario_id: int
    data_decisao: datetime

    class Config:
        from_attributes = True