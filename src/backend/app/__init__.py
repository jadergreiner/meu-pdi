"""
Aplicação FastAPI modular para a plataforma Meu PDI.

Este é o ponto de entrada principal da aplicação FastAPI,
configurada de forma modular com routers separados.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.core.config import settings
from app.db.session import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida da aplicação.

    Executado na inicialização e no encerramento da aplicação.
    """
    # Inicialização
    print("🚀 Inicializando aplicação FastAPI...")

    # Criar tabelas do banco de dados
    try:
        await create_tables()
        print("✅ Tabelas do banco de dados criadas/verficadas")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

    yield

    # Encerramento
    print("🛑 Encerrando aplicação FastAPI...")


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API Backend para a plataforma Meu PDI - Desenvolvimento Profissional Individual",
    lifespan=lifespan,
    debug=settings.debug,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health_router)

# Rota raiz
@app.get("/")
async def root():
    """Rota raiz da API."""
    return {
        "message": "Bem-vindo à API Meu PDI",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    )