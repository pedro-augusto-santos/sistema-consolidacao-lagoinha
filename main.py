from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
import models 
import schemas
from auth import hash_senha, verificar_senha, criar_token
app = FastAPI()

def get_db(): # Função responsavel por criar as sessões no db
    try:
        sessao_db = SessionLocal()

        yield sessao_db
    
    finally:

        sessao_db.close()


@app.post("/login", response_model=schemas.TokenResponse) # ROTA DO LOGIN
def login(usuario: schemas.LoginRequest, db: Session = Depends(get_db)):
    usuario_encontrado = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()

    if not usuario_encontrado or not verificar_senha(usuario.senha,usuario_encontrado.senha_hash): # SE usuario não existe OU senha não bate
        raise HTTPException(status_code=401, detail="Login inválido")
    
    token = criar_token({"sub": str(usuario_encontrado.id) }) # validação da identidade do token

    return {"access_token": token}

@app.post("/registrar", response_model=schemas.UsuarioOut)
def registrar(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    senha_hash = hash_senha(usuario.senha)

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario