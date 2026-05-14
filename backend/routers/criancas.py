from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database.database import get_db
from models.models import Crianca

router = APIRouter()

class CriancaCreate(BaseModel):
    nome: str
    idade: int
    sexo: str
    status: Optional[str] = "disponível"
    id_instituicao: Optional[int] = None

class CriancaOut(CriancaCreate):
    id_crianca: int
    class Config:
        from_attributes = True

@router.get("/", response_model=List[CriancaOut])
def listar_criancas(db: Session = Depends(get_db)):
    return db.query(Crianca).all()

@router.get("/{id}", response_model=CriancaOut)
def obter_crianca(id: int, db: Session = Depends(get_db)):
    c = db.query(Crianca).filter(Crianca.id_crianca == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Criança não encontrada")
    return c

@router.post("/", response_model=CriancaOut)
def criar_crianca(data: CriancaCreate, db: Session = Depends(get_db)):
    c = Crianca(**data.dict())
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.put("/{id}", response_model=CriancaOut)
def atualizar_crianca(id: int, data: CriancaCreate, db: Session = Depends(get_db)):
    c = db.query(Crianca).filter(Crianca.id_crianca == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Criança não encontrada")
    for k, v in data.dict().items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c

@router.delete("/{id}")
def deletar_crianca(id: int, db: Session = Depends(get_db)):
    c = db.query(Crianca).filter(Crianca.id_crianca == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Criança não encontrada")
    db.delete(c); db.commit()
    return {"ok": True}
