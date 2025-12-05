"""
Endpoint de health check da API.

Este módulo contém o endpoint básico de verificação de saúde da aplicação.
"""

from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de verificação de saúde da API.

    Retorna informações básicas sobre o status da aplicação.

    Returns:
        dict: Status da aplicação com timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc),
        "service": "Meu PDI - Backend API",
        "version": "1.0.0"
    }