# TASK-T003: Implement JWT Authentication
# TASK-T010: FastAPI modular setup

"""
Aplicação principal FastAPI para Meu PDI - Portal do Aluno.

Esta aplicação integra todos os módulos modulares:
- app/api/auth.py: Endpoints de autenticação (registro, login, refresh, validação email, reset senha)
- app/api/users.py: Endpoints de usuários (perfil, PDI, próximas ações, configurações responsivas)
"""

import sys
import os

# Adicionar o diretório atual ao PYTHONPATH para importações modulares
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

# Importações dos módulos modulares
try:
    from app.api.auth import router as auth_router
    from app.api.users import router as users_router
    from app.api.payments import router as payments_router
    MODULAR_ROUTERS_AVAILABLE = True
except ImportError as e:
    print(f"Aviso: Routers modulares não disponíveis: {e}")
    MODULAR_ROUTERS_AVAILABLE = False
    auth_router = None
    users_router = None
    payments_router = None

app = FastAPI(
    title="Meu PDI - Portal do Aluno",
    version="1.0.0",
    description="Plataforma de mentoria para desenvolvimento profissional individual"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:4200"],  # Frontend Next.js e Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers modulares se disponíveis
if MODULAR_ROUTERS_AVAILABLE:
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(users_router, prefix="/api/users", tags=["Users"])
    app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])
    print("Routers modulares carregados com sucesso")
else:
    print("Executando sem routers modulares")

@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc),
        "version": "1.0.0",
        "modules": ["auth", "users", "payments"]
    }

@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "Bem-vindo ao Meu PDI - Portal do Aluno",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Executar servidor se arquivo for executado diretamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)