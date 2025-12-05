"""
Modelo de Usuário da aplicação.

Este módulo define o modelo User usando SQLAlchemy ORM,
representando um usuário da plataforma Meu PDI.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models import Base


class User(Base):
    """Modelo de usuário da plataforma."""

    __tablename__ = "users"

    # Campos obrigatórios
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_completo = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)

    # Campos de validação
    email_validado = Column(Boolean, default=False, nullable=False)
    token_validacao = Column(String(255), nullable=True)
    token_expiracao = Column(DateTime(timezone=True), nullable=True)

    # Campos de perfil (opcionais)
    foto_perfil = Column(String(500), nullable=True)
    cargo_atual = Column(String(100), nullable=True)
    empresa_atual = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)

    # Campos de PDI
    pdi_status = Column(String(50), default="iniciando", nullable=False)
    pdi_objetivos = Column(Text, nullable=True)  # JSON string
    pdi_progresso = Column(Integer, default=0, nullable=False)
    pdi_ultima_atualizacao = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Campos de auditoria
    data_cadastro = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    payments = relationship("Payment", back_populates="user")

    def __repr__(self):
        """Representação string do usuário."""
        return f"<User(id={self.id}, email='{self.email}', nome='{self.nome_completo}')>"