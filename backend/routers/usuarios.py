from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database.database import get_db
from models.models import Usuario
from utils.security import gerar_hash, verificar_senha

router = APIRouter()

# Schema para criação (pede perfil)
class UsuarioCreate(BaseModel):
    login: str
    senha: str
    perfil: str

# Schema para login (não pede perfil)
class UsuarioLogin(BaseModel):
    login: str
    senha: str

# Schema para saída (não mostra a senha)
class UsuarioOut(BaseModel):
    id_usuario: int
    login: str
    perfil: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[UsuarioOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.post("/", response_model=UsuarioOut)
def criar(data: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Transforma a senha pura em Hash
    senha_hash = gerar_hash(data.senha)
    
    # 2. Cria o usuário com a senha protegida
    u = Usuario(
        login=data.login,
        perfil=data.perfil,
        senha=senha_hash
    )
    
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@router.post("/login")
def login(data: UsuarioLogin, db: Session = Depends(get_db)):
    # 1. Busca o usuário apenas pelo login
    u = db.query(Usuario).filter(Usuario.login == data.login).first()
    
    # 2. Verifica se o usuário existe E se a senha bate com o hash salvo
    if not u or not verificar_senha(data.senha, u.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    return {"id_usuario": u.id_usuario, "login": u.login, "perfil": u.perfil}

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    u = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(u)
    db.commit()
    return {"ok": True}