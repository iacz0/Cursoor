# 🌱 Plataforma de Adoção Digital e Convivência

**Autores:** Julya Sally, Iann Cortez e Matheus Henrique  
**Instituição:** Centro Universitário Maurício de Nassau (Recife – PE)

---

## 📁 Estrutura do Projeto

```
adocao/
├── backend/
│   ├── main.py                  ← Entrada da API FastAPI
│   ├── requirements.txt         ← Dependências Python
│   ├── database/
│   │   └── database.py          ← Conexão SQLite/PostgreSQL
│   ├── models/
│   │   └── models.py            ← Tabelas do banco de dados
│   └── routers/
│       ├── criancas.py          ← CRUD Crianças
│       ├── adotantes.py         ← CRUD Adotantes
│       ├── instituicoes.py      ← CRUD Instituições
│       ├── processos.py         ← CRUD Processos de Adoção
│       ├── cursos.py            ← CRUD Cursos
│       ├── matriculas.py        ← CRUD Matrículas
│       ├── compatibilidade.py   ← CRUD Compatibilidade
│       ├── relatorios.py        ← Dashboard / Estatísticas
│       └── usuarios.py          ← Usuários e Login
└── frontend/
    └── index.html               ← Aplicação Vue.js (SPA)
```

---

## 🚀 Como Executar

### 1. Back-end (FastAPI)

```bash
cd backend

# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
uvicorn main:app --reload
```

O servidor estará disponível em: **http://localhost:8000**  
Documentação automática da API: **http://localhost:8000/docs**

---

### 2. Front-end (Vue.js)

Abra o arquivo `frontend/index.html` diretamente no navegador.

> **Dica:** Use a extensão "Live Server" no VS Code para evitar erros de CORS.

---

### 3. Criar primeiro usuário (para fazer login)

Com o servidor rodando, acesse: **http://localhost:8000/docs**

Execute o endpoint `POST /usuarios/` com:
```json
{
  "login": "admin",
  "senha": "1234",
  "perfil": "Governo"
}
```

Depois faça login na interface com `admin` / `1234`.

---

## 🗄️ Banco de Dados

Por padrão, usa **SQLite** (arquivo `adocao.db` criado automaticamente).

Para usar **PostgreSQL**, edite `database/database.py`:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://usuario:senha@localhost/adocao_db"
```

---

## 📊 Funcionalidades

| Módulo | Funcionalidades |
|---|---|
| **Crianças** | Cadastro, edição, exclusão, status |
| **Adotantes** | Perfil completo com preferências |
| **Instituições** | Unidades de acolhimento |
| **Processos** | Acompanhamento da adoção |
| **Cursos** | Proposta e aprovação pelo Governo |
| **Matrículas** | Participação das crianças nos cursos |
| **Compatibilidade** | Índice teórico + prático + geral |
| **Dashboard** | Estatísticas em tempo real |
| **Usuários** | Controle de acesso (Governo / Assistente Social) |

---

## 🛠️ Tecnologias

- **Back-end:** Python 3.10+ · FastAPI · SQLAlchemy · SQLite
- **Front-end:** Vue.js 3 (CDN) · HTML5 · CSS3 puro
- **API:** RESTful com documentação automática (Swagger UI)
