"""
Modelo de Pagamento da aplicação.

Este módulo define os modelos relacionados a pagamentos usando SQLAlchemy ORM,
representando transações, status e integrações com gateways de pagamento.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models import Base


class Payment(Base):
    """Modelo de pagamento/transação."""

    __tablename__ = "payments"

    # Campos obrigatórios
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Informações da transação
    gateway = Column(String(50), nullable=False)  # 'stripe' ou 'pagseguro'
    gateway_payment_id = Column(String(255), unique=True, nullable=False, index=True)
    amount = Column(Float, nullable=False)  # Valor em reais
    currency = Column(String(3), default="BRL", nullable=False)

    # Status e controle
    status = Column(String(50), default="pending", nullable=False)  # pending, paid, failed, refunded
    payment_method = Column(String(50), nullable=True)  # credit_card, pix, boleto
    description = Column(String(255), nullable=True)

    # Dados do gateway (JSON)
    gateway_metadata = Column(Text, nullable=True)  # JSON com dados específicos do gateway

    # URLs e referências
    receipt_url = Column(String(500), nullable=True)
    invoice_url = Column(String(500), nullable=True)

    # Controle de tentativas e notificações
    webhook_attempts = Column(Integer, default=0, nullable=False)
    last_webhook_at = Column(DateTime(timezone=True), nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Campos de auditoria
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    user = relationship("User", back_populates="payments")
    webhook_logs = relationship("PaymentWebhookLog", back_populates="payment")

    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, gateway={self.gateway}, status={self.status}, amount={self.amount})>"


class PaymentWebhookLog(Base):
    """Log de webhooks recebidos dos gateways de pagamento."""

    __tablename__ = "payment_webhook_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True, index=True)

    # Informações do webhook
    gateway = Column(String(50), nullable=False)  # 'stripe' ou 'pagseguro'
    event_type = Column(String(100), nullable=False)  # Tipo do evento (payment.succeeded, etc.)
    event_id = Column(String(255), unique=True, nullable=False, index=True)  # ID único do evento

    # Payload e headers
    payload = Column(Text, nullable=False)  # JSON do payload recebido
    headers = Column(Text, nullable=True)  # Headers HTTP recebidos
    signature = Column(String(500), nullable=True)  # Assinatura para verificação

    # Processamento
    processed = Column(Boolean, default=False, nullable=False)
    processing_error = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Campos de auditoria
    received_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Relacionamentos
    payment = relationship("Payment", back_populates="webhook_logs")

    def __repr__(self):
        return f"<PaymentWebhookLog(id={self.id}, gateway={self.gateway}, event_type={self.event_type}, processed={self.processed})>"