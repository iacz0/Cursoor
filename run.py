import sys
import os
import uvicorn

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

if __name__ == "__main__":
    print("🚀 Servidor da Plataforma de Adoção iniciado em http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)