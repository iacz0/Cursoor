from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database.database import get_db
from models.models import Compatibilidade

router = APIRouter()

class CompatCreate(BaseModel):
    id_crianca: int
    id_adotante: int
    nivel_teorico: Optional[float] = 0.0
    nivel_pratico: Optional[float] = 0.0
    nivel_geral: Optional[float] = 0.0

class CompatOut(CompatCreate):
    id: int
    class Config:
        from_attributes = True

@router.get("/", response_model=List[CompatOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Compatibilidade).all()

@router.post("/", response_model=CompatOut)
def criar(data: CompatCreate, db: Session = Depends(get_db)):
    geral = (data.nivel_teorico + data.nivel_pratico) / 2
    c = Compatibilidade(**data.dict(), nivel_geral=geral)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.put("/{id}", response_model=CompatOut)
def atualizar(id: int, data: CompatCreate, db: Session = Depends(get_db)):
    c = db.query(Compatibilidade).filter(Compatibilidade.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    for k, v in data.dict().items():
        setattr(c, k, v)
    c.nivel_geral = (data.nivel_teorico + data.nivel_pratico) / 2
    db.commit(); db.refresh(c)
    return c
