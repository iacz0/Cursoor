from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database.database import get_db
from models.models import ProcessoAdocao

router = APIRouter()

class ProcessoCreate(BaseModel):
    id_crianca: int
    id_adotante: int
    status: Optional[str] = "em andamento"

class ProcessoOut(ProcessoCreate):
    id_processo: int
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProcessoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(ProcessoAdocao).all()

@router.get("/{id}", response_model=ProcessoOut)
def obter(id: int, db: Session = Depends(get_db)):
    p = db.query(ProcessoAdocao).filter(ProcessoAdocao.id_processo == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Processo não encontrado")
    return p

@router.post("/", response_model=ProcessoOut)
def criar(data: ProcessoCreate, db: Session = Depends(get_db)):
    p = ProcessoAdocao(**data.dict())
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.put("/{id}", response_model=ProcessoOut)
def atualizar(id: int, data: ProcessoCreate, db: Session = Depends(get_db)):
    p = db.query(ProcessoAdocao).filter(ProcessoAdocao.id_processo == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Processo não encontrado")
    for k, v in data.dict().items():
        setattr(p, k, v)
    db.commit(); db.refresh(p)
    return p

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    p = db.query(ProcessoAdocao).filter(ProcessoAdocao.id_processo == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Processo não encontrado")
    db.delete(p); db.commit()
    return {"ok": True}
