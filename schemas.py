from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel): 
    # O que chega na API quando alguém cria uma conta
    nome: str
    email: EmailStr
    senha: str


class UsuarioOut(BaseModel): 
    # O que a API devolve para o usuário (sem dados sensíveis)
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True  
        # Permite converter um objeto do SQLAlchemy em um schema Pydantic

class LoginRequest(BaseModel): # O que o usuario digita para fazer login
    email : EmailStr
    senha : str

class TokenResponse(BaseModel): # O que a API devolve após um login bem sucedido
    access_token : str
    token_type : str = "bearer"