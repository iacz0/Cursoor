from database.database import SessionLocal
from models.models import Usuario

def create_test_admin():
    db = SessionLocal()
    
    # Verifica se o admin já existe para não duplicar
    admin_existente = db.query(Usuario).filter(Usuario.login == "admin").first()
    
    if not admin_existente:
        admin = Usuario(
            login="admin",
            senha="admin123", # Para teste, em texto puro. No futuro, use hash!
            perfil="Admin"
        )
        db.add(admin)
        db.commit()
        print("✅ Usuário admin criado com sucesso! (admin / admin123)")
    else:
        print("ℹ️ Usuário admin já existe no banco.")
        
    db.close()

if __name__ == "__main__":
    create_test_admin()