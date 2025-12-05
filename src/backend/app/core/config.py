"""
Configurações centrais da aplicação FastAPI.

Este módulo contém todas as configurações da aplicação,
carregadas de variáveis de ambiente com valores padrão seguros.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação usando Pydantic BaseSettings."""

    # Configurações básicas da aplicação
    app_name: str = "Meu PDI - Plataforma de Mentoria"
    app_version: str = "1.0.0"
    debug: bool = False

    # Configurações do servidor
    host: str = "0.0.0.0"
    port: int = 8000

    # Configurações de segurança JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Caminhos das chaves JWT (para RS256)
    jwt_private_key_path: Optional[str] = None
    jwt_public_key_path: Optional[str] = None

    # Configurações do banco de dados
    database_url: str = "postgresql+asyncpg://meu_pdi_user:meu_pdi_password@localhost:5432/meu_pdi_dev"

    # Configurações Redis
    redis_url: str = "redis://localhost:6379/0"

    # Configurações de CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:4200"]

    # Configurações de email (para produção)
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None

    # Configurações de rate limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # segundos

    class Config:
        """Configurações do Pydantic para carregar variáveis de ambiente."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instância global das configurações
settings = Settings()

# Constantes derivadas das configurações
JWT_PRIVATE_KEY = settings.jwt_secret_key
JWT_PUBLIC_KEY = settings.jwt_secret_key  # Para HS256, mesma chave
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.jwt_refresh_token_expire_days