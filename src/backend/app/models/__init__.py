"""
Modelos SQLAlchemy da aplicação.

Este módulo contém todos os modelos de dados da aplicação,
baseados no SQLAlchemy ORM.
"""

from sqlalchemy.orm import declarative_base, relationship

# Base declarativa para todos os modelos
Base = declarative_base()

# Importar modelos para registro
from .user import User
from .payment import Payment, PaymentWebhookLog

__all__ = ["Base", "User", "Payment", "PaymentWebhookLog"]