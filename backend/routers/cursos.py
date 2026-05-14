from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database.database import get_db
from models.models import Curso

router = APIRouter()

class CursoCreate(BaseModel):
    id_adotante_instrutor: int
    titulo: str
    descricao: Optional[str] = None
    status_aprovacao: Optional[str] = "Pendente"

class CursoOut(CursoCreate):
    id_curso: int
    class Config:
        from_attributes = True

@router.get("/", response_model=List[CursoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Curso).all()

@router.get("/{id}", response_model=CursoOut)
def obter(id: int, db: Session = Depends(get_db)):
    c = db.query(Curso).filter(Curso.id_curso == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return c

@router.post("/", response_model=CursoOut)
def criar(data: CursoCreate, db: Session = Depends(get_db)):
    c = Curso(**data.dict())
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.put("/{id}", response_model=CursoOut)
def atualizar(id: int, data: CursoCreate, db: Session = Depends(get_db)):
    c = db.query(Curso).filter(Curso.id_curso == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    for k, v in data.dict().items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c

@router.put("/{id}/aprovar")
def aprovar_curso(id: int, db: Session = Depends(get_db)):
    c = db.query(Curso).filter(Curso.id_curso == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    c.status_aprovacao = "Aprovado"
    db.commit(); db.refresh(c)
    return c

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    c = db.query(Curso).filter(Curso.id_curso == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    db.delete(c); db.commit()
    return {"ok": True}
