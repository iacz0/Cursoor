from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.database import get_db
from models.models import Crianca, Adotante, Curso, Matricula, ProcessoAdocao, Relatorio
import json

router = APIRouter()

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total_criancas = db.query(Crianca).count()
    criancas_disponiveis = db.query(Crianca).filter(Crianca.status == "disponível").count()
    total_adotantes = db.query(Adotante).count()
    total_cursos = db.query(Curso).count()
    cursos_aprovados = db.query(Curso).filter(Curso.status_aprovacao == "Aprovado").count()
    total_matriculas = db.query(Matricula).count()
    total_processos = db.query(ProcessoAdocao).count()
    processos_concluidos = db.query(ProcessoAdocao).filter(ProcessoAdocao.status == "concluído").count()

    return {
        "criancas": {"total": total_criancas, "disponiveis": criancas_disponiveis},
        "adotantes": {"total": total_adotantes},
        "cursos": {"total": total_cursos, "aprovados": cursos_aprovados, "pendentes": total_cursos - cursos_aprovados},
        "matriculas": {"total": total_matriculas},
        "processos": {"total": total_processos, "concluidos": processos_concluidos}
    }
