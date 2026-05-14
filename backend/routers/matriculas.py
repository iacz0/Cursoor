from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database.database import get_db
from models.models import Matricula

router = APIRouter()

class MatriculaCreate(BaseModel):
    id_curso: int
    id_crianca: int
    status: Optional[str] = "Ativo"

class MatriculaOut(MatriculaCreate):
    id_matricula: int
    class Config:
        from_attributes = True

@router.get("/", response_model=List[MatriculaOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Matricula).all()

@router.get("/{id}", response_model=MatriculaOut)
def obter(id: int, db: Session = Depends(get_db)):
    m = db.query(Matricula).filter(Matricula.id_matricula == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return m

@router.post("/", response_model=MatriculaOut)
def criar(data: MatriculaCreate, db: Session = Depends(get_db)):
    m = Matricula(**data.dict())
    db.add(m); db.commit(); db.refresh(m)
    return m

@router.put("/{id}/concluir")
def concluir(id: int, db: Session = Depends(get_db)):
    m = db.query(Matricula).filter(Matricula.id_matricula == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    m.status = "Concluído"
    db.commit(); db.refresh(m)
    return m

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    m = db.query(Matricula).filter(Matricula.id_matricula == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    db.delete(m); db.commit()
    return {"ok": True}
