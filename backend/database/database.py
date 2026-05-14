from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Onde o banco será salvo
SQLALCHEMY_DATABASE_URL = "sqlite:///./adocao.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# A função que estava faltando! 
# Ela abre a conexão e fecha automaticamente depois de usar.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()