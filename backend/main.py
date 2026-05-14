from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa o motor do banco e a Base do arquivo que configuramos acima
from database.database import engine, Base
# IMPORTANTE: Importar os models para o SQLAlchemy saber o que criar
from models import models 

from routers import (
    criancas, adotantes, instituicoes, processos, 
    cursos, matriculas, compatibilidade, relatorios, usuarios
)

# Cria as tabelas no banco de dados automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plataforma de Adoção Digital e Convivência",
    description="API para gestão de adoção e módulo de convivência educacional",
    version="1.0.0"
)

# Configuração de CORS (Liberado para o seu frontend acessar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(criancas.router, prefix="/criancas", tags=["Crianças"])
app.include_router(adotantes.router, prefix="/adotantes", tags=["Adotantes"])
app.include_router(instituicoes.router, prefix="/instituicoes", tags=["Instituições"])
app.include_router(processos.router, prefix="/processos", tags=["Processos de Adoção"])
app.include_router(cursos.router, prefix="/cursos", tags=["Cursos"])
app.include_router(matriculas.router, prefix="/matriculas", tags=["Matrículas"])
app.include_router(compatibilidade.router, prefix="/compatibilidade", tags=["Compatibilidade"])
app.include_router(relatorios.router, prefix="/relatorios", tags=["Relatórios"])

@app.get("/")
def root():
    return {"message": "Plataforma de Adoção Digital e Convivência - API v1.0"}