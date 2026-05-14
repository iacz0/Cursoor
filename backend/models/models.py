from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    login = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    perfil = Column(String(50), nullable=False)  # Governo / Assistente Social

class Instituicao(Base):
    __tablename__ = "instituicoes"
    id_instituicao = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    localizacao = Column(String(300))
    tipo = Column(String(100))
    criancas = relationship("Crianca", back_populates="instituicao")

class Crianca(Base):
    __tablename__ = "criancas"
    id_crianca = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    idade = Column(Integer)
    sexo = Column(String(20))
    status = Column(String(50), default="disponível")  # disponível / em processo
    id_instituicao = Column(Integer, ForeignKey("instituicoes.id_instituicao"))
    instituicao = relationship("Instituicao", back_populates="criancas")
    matriculas = relationship("Matricula", back_populates="crianca")
    compatibilidades = relationship("Compatibilidade", back_populates="crianca")

class Adotante(Base):
    __tablename__ = "adotantes"
    id_adotante = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    idade = Column(Integer)
    estado_civil = Column(String(50))
    preferencia_idade = Column(String(50))
    preferencia_sexo = Column(String(20))
    processos = relationship("ProcessoAdocao", back_populates="adotante")
    cursos = relationship("Curso", back_populates="instrutor")
    compatibilidades = relationship("Compatibilidade", back_populates="adotante")

class ProcessoAdocao(Base):
    __tablename__ = "processos_adocao"
    id_processo = Column(Integer, primary_key=True, index=True)
    id_crianca = Column(Integer, ForeignKey("criancas.id_crianca"))
    id_adotante = Column(Integer, ForeignKey("adotantes.id_adotante"))
    status = Column(String(50), default="em andamento")
    data_inicio = Column(DateTime, server_default=func.now())
    crianca = relationship("Crianca")
    adotante = relationship("Adotante", back_populates="processos")

class Curso(Base):
    __tablename__ = "cursos"
    id_curso = Column(Integer, primary_key=True, index=True)
    id_adotante_instrutor = Column(Integer, ForeignKey("adotantes.id_adotante"))
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text)
    status_aprovacao = Column(String(50), default="Pendente")  # Pendente / Aprovado
    instrutor = relationship("Adotante", back_populates="cursos")
    matriculas = relationship("Matricula", back_populates="curso")

class Matricula(Base):
    __tablename__ = "matriculas"
    id_matricula = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"))
    id_crianca = Column(Integer, ForeignKey("criancas.id_crianca"))
    data_inscricao = Column(DateTime, server_default=func.now())
    status = Column(String(50), default="Ativo")  # Ativo / Concluído
    curso = relationship("Curso", back_populates="matriculas")
    crianca = relationship("Crianca", back_populates="matriculas")

class Compatibilidade(Base):
    __tablename__ = "compatibilidade"
    id = Column(Integer, primary_key=True, index=True)
    id_crianca = Column(Integer, ForeignKey("criancas.id_crianca"))
    id_adotante = Column(Integer, ForeignKey("adotantes.id_adotante"))
    nivel_teorico = Column(Float, default=0.0)
    nivel_pratico = Column(Float, default=0.0)
    nivel_geral = Column(Float, default=0.0)
    crianca = relationship("Crianca", back_populates="compatibilidades")
    adotante = relationship("Adotante", back_populates="compatibilidades")

class Relatorio(Base):
    __tablename__ = "relatorios"
    id_relatorio = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(100))
    dados_json = Column(Text)
    data_geracao = Column(DateTime, server_default=func.now())
