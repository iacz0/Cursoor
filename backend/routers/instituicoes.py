from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database.database import get_db
from models.models import Instituicao

router = APIRouter()

class InstituicaoCreate(BaseModel):
    nome: str
    localizacao: Optional[str] = None
    tipo: Optional[str] = None

class InstituicaoOut(InstituicaoCreate):
    id_instituicao: int
    class Config:
        from_attributes = True

@router.get("/", response_model=List[InstituicaoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Instituicao).all()

@router.get("/{id}", response_model=InstituicaoOut)
def obter(id: int, db: Session = Depends(get_db)):
    i = db.query(Instituicao).filter(Instituicao.id_instituicao == id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Instituição não encontrada")
    return i

@router.post("/", response_model=InstituicaoOut)
def criar(data: InstituicaoCreate, db: Session = Depends(get_db)):
    i = Instituicao(**data.dict())
    db.add(i); db.commit(); db.refresh(i)
    return i

@router.put("/{id}", response_model=InstituicaoOut)
def atualizar(id: int, data: InstituicaoCreate, db: Session = Depends(get_db)):
    i = db.query(Instituicao).filter(Instituicao.id_instituicao == id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Instituição não encontrada")
    for k, v in data.dict().items():
        setattr(i, k, v)
    db.commit(); db.refresh(i)
    return i

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    i = db.query(Instituicao).filter(Instituicao.id_instituicao == id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Instituição não encontrada")
    db.delete(i); db.commit()
    return {"ok": True}
