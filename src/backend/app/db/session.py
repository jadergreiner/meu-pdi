"""
Configuração da sessão do banco de dados SQLAlchemy.

Este módulo configura a engine assíncrona do SQLAlchemy e fornece
a sessão do banco de dados para toda a aplicação.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Engine assíncrona do SQLAlchemy
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log das queries em modo debug
    poolclass=NullPool,  # Pool de conexões desabilitado para desenvolvimento
    future=True,
)

# Session factory assíncrona
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """
    Dependência FastAPI para obter uma sessão de banco de dados.

    Esta função é usada como dependência nas rotas FastAPI para
    fornecer uma sessão de banco assíncrona.

    Yields:
        AsyncSession: Sessão do banco de dados
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    """
    Cria todas as tabelas do banco de dados.

    Esta função deve ser chamada durante a inicialização da aplicação
    para garantir que todas as tabelas existam.
    """
    from app.models import Base  # Import aqui para evitar circular imports

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """
    Remove todas as tabelas do banco de dados.

    ATENÇÃO: Esta função remove TODOS os dados permanentemente.
    Use apenas em desenvolvimento ou testes.
    """
    from app.models import Base  # Import aqui para evitar circular imports

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)