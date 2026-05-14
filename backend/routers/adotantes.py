from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database.database import get_db
from models.models import Adotante

router = APIRouter()

class AdotanteCreate(BaseModel):
    nome: str
    idade: int
    estado_civil: str
    preferencia_idade: Optional[str] = None
    preferencia_sexo: Optional[str] = None

class AdotanteOut(AdotanteCreate):
    id_adotante: int
    class Config:
        from_attributes = True

@router.get("/", response_model=List[AdotanteOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Adotante).all()

@router.get("/{id}", response_model=AdotanteOut)
def obter(id: int, db: Session = Depends(get_db)):
    a = db.query(Adotante).filter(Adotante.id_adotante == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Adotante não encontrado")
    return a

@router.post("/", response_model=AdotanteOut)
def criar(data: AdotanteCreate, db: Session = Depends(get_db)):
    a = Adotante(**data.dict())
    db.add(a); db.commit(); db.refresh(a)
    return a

@router.put("/{id}", response_model=AdotanteOut)
def atualizar(id: int, data: AdotanteCreate, db: Session = Depends(get_db)):
    a = db.query(Adotante).filter(Adotante.id_adotante == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Adotante não encontrado")
    for k, v in data.dict().items():
        setattr(a, k, v)
    db.commit(); db.refresh(a)
    return a

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    a = db.query(Adotante).filter(Adotante.id_adotante == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Adotante não encontrado")
    db.delete(a); db.commit()
    return {"ok": True}
