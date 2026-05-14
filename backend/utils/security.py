from passlib.context import CryptContext

# Configura o algoritmo Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gerar_hash(senha: str) -> str:
    """Transforma senha pura em hash (embaralhado)"""
    return pwd_context.hash(senha)

def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """Verifica se a senha pura bate com o hash salvo"""
    return pwd_context.verify(senha_pura, senha_hash)