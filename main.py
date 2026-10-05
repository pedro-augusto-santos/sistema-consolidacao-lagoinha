from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from auth import hash_senha, verificar_senha, criar_token, verificar_token
from utils import calcular_cortes


app = FastAPI()


def get_db():
    try:
        sessao_db = SessionLocal()
        yield sessao_db
    finally:
        sessao_db.close()


@app.post("/login", response_model=schemas.TokenResponse)
def login(usuario: schemas.LoginRequest, db: Session = Depends(get_db)):
    usuario_encontrado = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()

    if not usuario_encontrado or not verificar_senha(usuario.senha, usuario_encontrado.senha_hash):
        raise HTTPException(status_code=401, detail="Login inválido")

    token = criar_token({"sub": str(usuario_encontrado.id)})
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


@app.post("/cadastrar", response_model=schemas.NovoComecoResponse)
def cadastrar(novo_comeco: schemas.NovoComecoCreate, db: Session = Depends(get_db), usuario_atual  = Depends(verificar_token)):
    novo_comeco_db = models.NovoComeco(
        nome_pessoa=novo_comeco.nome,
        telefone=novo_comeco.telefone,
        data_decisao=datetime.utcnow(),
        usuario_id=usuario_atual.id
    )

    db.add(novo_comeco_db)
    db.commit()
    db.refresh(novo_comeco_db)

    return novo_comeco_db


@app.get("/cadastros", response_model=list[schemas.NovoComecoResponse])
def listar_cadastros(db: Session = Depends(get_db), usuario_atual = Depends(verificar_token)):

    return db.query(models.NovoComeco).all()


@app.get("/cadastros/hoje", response_model=list[schemas.NovoComecoResponse])
def listar_cadastros(db: Session = Depends(get_db), usuario_atual = Depends(verificar_token)):
    inicio_dia = calcular_cortes()[0]

    return db.query(models.NovoComeco).filter(
        models.NovoComeco.data_decisao >= inicio_dia
    ).all()


@app.get("/cadastros/semana", response_model=list[schemas.NovoComecoResponse])
def cadastros_semana(db: Session = Depends(get_db), usuario_atual = Depends(verificar_token)):
    inicio_semana = calcular_cortes()[1]

    return db.query(models.NovoComeco).filter(
        models.NovoComeco.data_decisao >= inicio_semana
    ).all()


@app.get("/cadastros/mes", response_model=list[schemas.NovoComecoResponse])
def cadastros_mes(db: Session = Depends(get_db), usuario_atual = Depends(verificar_token)):
    inicio_mes = calcular_cortes()[2]

    return db.query(models.NovoComeco).filter(
        models.NovoComeco.data_decisao >= inicio_mes
    ).all()

@app.get("/contagem", response_model=schemas.ContagemResponse)
def contagem(db: Session = Depends(get_db), usuario_atual = Depends(verificar_token)):

    inicio_dia, inicio_semana, inicio_mes = calcular_cortes()

    return schemas.ContagemResponse(
        hoje=db.query(models.NovoComeco).filter(models.NovoComeco.data_decisao >= inicio_dia).count(),
        semana=db.query(models.NovoComeco).filter(models.NovoComeco.data_decisao >= inicio_semana).count(),
        mes=db.query(models.NovoComeco).filter(models.NovoComeco.data_decisao >= inicio_mes).count(),
        total=db.query(models.NovoComeco).count()
    )
