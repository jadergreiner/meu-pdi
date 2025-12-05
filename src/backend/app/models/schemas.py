"""
Schemas Pydantic para validação de dados da API.

Este módulo contém todos os modelos Pydantic utilizados na aplicação
para validação de entrada e saída de dados.
"""

import re
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ConfigDict


# Validação de senha forte
def validar_senha_forte(senha: str) -> bool:
    """
    Valida se a senha atende critérios de segurança:
    - Pelo menos 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    - Pelo menos um caractere especial
    """
    if len(senha) < 8:
        return False

    # Verificar critérios usando regex
    criterios = [
        r'[A-Z]',  # Maiúscula
        r'[a-z]',  # Minúscula
        r'[0-9]',  # Número
        r'[!@#$%^&*(),.?":{}|<>]'  # Caractere especial
    ]

    return all(re.search(criterio, senha) for criterio in criterios)


# Schemas de Autenticação
class UserRegister(BaseModel):
    """Schema para registro de novos usuários."""
    nome_completo: str = Field(..., min_length=2, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email profissional válido")
    senha: str = Field(..., min_length=8, max_length=128, description="Senha forte (8+ caracteres)")
    confirmar_senha: str = Field(..., description="Confirmação da senha")
    aceitar_termos: bool = Field(..., description="Aceite dos termos de uso e LGPD")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "nome_completo": "João Silva",
                "email": "joao.silva@email.com",
                "senha": "MinhaSenhaForte123!",
                "confirmar_senha": "MinhaSenhaForte123!",
                "aceitar_termos": True
            }
        }
    }

    @field_validator('senha')
    @classmethod
    def senha_deve_ser_forte(cls, v):
        if not validar_senha_forte(v):
            raise ValueError('Senha deve ter pelo menos 8 caracteres, com maiúscula, minúscula, número e caractere especial')
        return v

    @model_validator(mode='after')
    def senhas_devem_ser_iguais(self):
        if self.senha != self.confirmar_senha:
            raise ValueError('Confirmação de senha não coincide')
        return self


class UserLogin(BaseModel):
    """Schema para login de usuários."""
    email: EmailStr = Field(..., description="Email do usuário")
    senha: str = Field(..., description="Senha do usuário")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "email": "joao.silva@email.com",
                "senha": "MinhaSenhaForte123!"
            }
        }
    }


class UserBasicInfo(BaseModel):
    """Schema para informações básicas do usuário em respostas de token."""
    id: str
    nome_completo: str
    email: str
    email_validado: bool
    data_cadastro: datetime


class TokenResponse(BaseModel):
    """Schema para resposta de autenticação com tokens."""
    access_token: str
    refresh_token: str
    token_type: str
    user: UserBasicInfo

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "nome_completo": "João Silva",
                    "email": "joao.silva@email.com",
                    "email_validado": True,
                    "data_cadastro": "2025-11-03T10:30:00Z"
                }
            }
        }
    }


class RefreshTokenRequest(BaseModel):
    """Schema para requisição de refresh token."""
    refresh_token: str


# Schemas de Usuário
class UserResponse(BaseModel):
    """Schema para resposta de dados do usuário."""
    id: str
    nome_completo: str
    email: str
    email_validado: bool
    data_cadastro: datetime
    token_validacao: str

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nome_completo": "João Silva",
                "email": "joao.silva@email.com",
                "email_validado": False,
                "data_cadastro": "2025-11-03T10:30:00Z",
                "token_validacao": "abc123-def456-ghi789"
            }
        }
    }


class UserProfile(BaseModel):
    """Schema para resposta do perfil completo do usuário."""
    id: str
    nome_completo: str
    email: str
    email_validado: bool
    data_cadastro: datetime
    foto_perfil: Optional[str] = None
    cargo_atual: Optional[str] = None
    empresa_atual: Optional[str] = None
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nome_completo": "João Silva",
                "email": "joao.silva@email.com",
                "email_validado": True,
                "data_cadastro": "2025-11-03T10:30:00Z",
                "foto_perfil": "https://example.com/foto.jpg",
                "cargo_atual": "Desenvolvedor Senior",
                "empresa_atual": "Tech Company Ltda",
                "bio": "Desenvolvedor apaixonado por tecnologia e mentoria",
                "linkedin_url": "https://linkedin.com/in/joaosilva",
                "github_url": "https://github.com/joaosilva"
            }
        }
    }


# Schemas de PDI
class PDIOverview(BaseModel):
    """Schema para visão geral do PDI do usuário."""
    status_geral: str = Field(..., description="Status geral do PDI", examples=["iniciando", "em_andamento", "avancado"])
    objetivos_ativos: int = Field(..., description="Número de objetivos ativos", ge=0)
    progresso_percentual: float = Field(..., description="Progresso geral em percentual", ge=0.0, le=100.0)
    proximas_acoes: List[str] = Field(..., description="Próximas ações recomendadas")
    ultima_atualizacao: datetime = Field(..., description="Última atualização do PDI")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "status_geral": "iniciando",
                "objetivos_ativos": 0,
                "progresso_percentual": 0.0,
                "proximas_acoes": ["Completar perfil profissional", "Agendar primeira sessão de mentoria"],
                "ultima_atualizacao": "2025-11-03T10:30:00Z"
            }
        }
    }


class NextSteps(BaseModel):
    """Schema para próximas ações recomendadas ao usuário."""
    acoes_recomendadas: List[dict] = Field(..., description="Lista de ações recomendadas")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "acoes_recomendadas": [
                    {
                        "titulo": "Completar Perfil Profissional",
                        "descricao": "Adicione informações sobre sua experiência e objetivos",
                        "prioridade": "alta",
                        "url": "/profile/edit"
                    },
                    {
                        "titulo": "Agendar Primeira Sessão",
                        "descricao": "Conecte-se com um mentor para iniciar seu PDI",
                        "prioridade": "alta",
                        "url": "/mentoring/schedule"
                    }
                ]
            }
        }
    }


class UserStatistics(BaseModel):
    """Schema para estatísticas e métricas do usuário."""
    dias_ativos: int = Field(..., description="Número de dias consecutivos com atividade")
    objetivos_completados: int = Field(..., description="Total de objetivos PDI concluídos")
    progresso_mensal: float = Field(..., description="Percentual de progresso no mês atual")
    sessoes_realizadas: int = Field(..., description="Número total de sessões de mentoria realizadas")
    horas_dedicadas: float = Field(..., description="Total de horas dedicadas ao desenvolvimento")
    streak_atual: int = Field(..., description="Sequência atual de dias ativos")
    nivel_engajamento: str = Field(..., description="Nível de engajamento (baixo/médio/alto)")
    ultima_atividade: Optional[datetime] = Field(None, description="Data da última atividade")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "dias_ativos": 15,
                "objetivos_completados": 3,
                "progresso_mensal": 75.5,
                "sessoes_realizadas": 2,
                "horas_dedicadas": 8.5,
                "streak_atual": 5,
                "nivel_engajamento": "alto",
                "ultima_atividade": "2025-11-03T14:30:00Z"
            }
        }
    }


# Schemas de Reset de Senha
class PasswordResetRequest(BaseModel):
    """Schema para solicitação de reset de senha."""
    email: EmailStr = Field(..., description="Email do usuário para reset de senha")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "email": "joao.silva@email.com"
            }
        }
    }


class PasswordResetConfirm(BaseModel):
    """Schema para confirmação de reset de senha."""
    token: str = Field(..., description="Token de reset recebido por email")
    nova_senha: str = Field(..., min_length=8, description="Nova senha forte")
    confirmar_senha: str = Field(..., description="Confirmação da nova senha")

    @model_validator(mode='after')
    def senhas_reset_devem_ser_iguais(self):
        if self.nova_senha != self.confirmar_senha:
            raise ValueError('Confirmação de senha não coincide')
        return self

    @field_validator('nova_senha')
    @classmethod
    def nova_senha_deve_ser_forte(cls, v):
        if not validar_senha_forte(v):
            raise ValueError(
                'Senha deve ter pelo menos 8 caracteres, '
                'uma letra maiúscula, uma minuscula, um número e um caractere especial'
            )
        return v

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "token": "abc123-def456-ghi789",
                "nova_senha": "NovaSenhaForte123!",
                "confirmar_senha": "NovaSenhaForte123!"
            }
        }
    }


# Schemas de Validação de Email
class EmailValidationRequest(BaseModel):
    """Schema para validação de email."""
    token: str = Field(..., description="Token de validação enviado por email")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "token": "abc123-def456-ghi789"
            }
        }
    }


# Schemas de Dashboard
class ResponsiveConfig(BaseModel):
    """Schema para configurações responsivas do dashboard."""
    breakpoints: dict = Field(..., description="Breakpoints para responsividade")
    layout: dict = Field(..., description="Configurações de layout")
    responsive_features: dict = Field(..., description="Features responsivas habilitadas")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "breakpoints": {
                    "mobile": 768,
                    "tablet": 1024,
                    "desktop": 1440
                },
                "layout": {
                    "grid_columns": {"mobile": 1, "tablet": 2, "desktop": 3},
                    "sidebar_collapsible": True,
                    "mobile_navigation": "drawer"
                },
                "responsive_features": {
                    "touch_friendly": True,
                    "lazy_loading": True,
                    "adaptive_images": True
                }
            }
        }
    }


# Schemas de Pagamento
class PaymentCreate(BaseModel):
    """Schema para criação de novo pagamento."""
    amount: float = Field(..., gt=0, description="Valor do pagamento em reais")
    currency: str = Field(default="BRL", min_length=3, max_length=3, description="Moeda (ISO 4217)")
    gateway: str = Field(..., pattern="^(stripe|pagseguro)$", description="Gateway de pagamento")
    description: Optional[str] = Field(None, max_length=255, description="Descrição do pagamento")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "amount": 299.90,
                "currency": "BRL",
                "gateway": "stripe",
                "description": "Mentoria PDI - Pacote Premium"
            }
        }
    }


class PaymentResponse(BaseModel):
    """Schema para resposta de pagamento."""
    id: int
    user_id: int
    gateway: str
    gateway_payment_id: str
    amount: float
    currency: str
    status: str
    payment_method: Optional[str]
    description: Optional[str]
    receipt_url: Optional[str]
    invoice_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 123,
                "gateway": "stripe",
                "gateway_payment_id": "pi_1234567890",
                "amount": 299.90,
                "currency": "BRL",
                "status": "paid",
                "payment_method": "credit_card",
                "description": "Mentoria PDI - Pacote Premium",
                "receipt_url": "https://pay.stripe.com/receipts/...",
                "invoice_url": None,
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-15T10:35:00Z"
            }
        }
    }


class PaymentWebhookLogResponse(BaseModel):
    """Schema para resposta de log de webhook."""
    id: int
    payment_id: Optional[int]
    gateway: str
    event_type: str
    event_id: str
    processed: bool
    processing_error: Optional[str]
    received_at: datetime

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "payment_id": 123,
                "gateway": "stripe",
                "event_type": "payment_intent.succeeded",
                "event_id": "evt_1234567890",
                "processed": True,
                "processing_error": None,
                "received_at": "2025-01-15T10:35:00Z"
            }
        }
    }


class StripeWebhookPayload(BaseModel):
    """Schema para payload de webhook do Stripe."""
    id: str = Field(..., description="ID do evento")
    object: str = Field(..., description="Tipo do objeto")
    api_version: Optional[str]
    created: int
    data: dict = Field(..., description="Dados do evento")
    livemode: bool
    pending_webhooks: int
    request: Optional[dict]
    type: str = Field(..., description="Tipo do evento")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "id": "evt_1234567890",
                "object": "event",
                "api_version": "2020-08-27",
                "created": 1640995200,
                "data": {
                    "object": {
                        "id": "pi_1234567890",
                        "object": "payment_intent",
                        "amount": 29990,
                        "currency": "brl",
                        "status": "succeeded"
                    }
                },
                "livemode": False,
                "pending_webhooks": 1,
                "request": {"id": "req_123", "idempotency_key": None},
                "type": "payment_intent.succeeded"
            }
        }
    }


class PagSeguroWebhookPayload(BaseModel):
    """Schema para payload de webhook do PagSeguro."""
    event: str = Field(..., description="Tipo do evento")
    payment: dict = Field(..., description="Dados do pagamento")
    resource: Optional[dict]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "event": "PAYMENT",
                "payment": {
                    "code": "PAY-1234567890",
                    "status": "PAID",
                    "amount": "299.90",
                    "grossAmount": "299.90"
                },
                "resource": {
                    "title": "Mentoria PDI - Pacote Premium",
                    "description": "Pagamento confirmado"
                }
            }
        }
    }


class WebhookResponse(BaseModel):
    """Schema para resposta de processamento de webhook."""
    success: bool
    message: str
    payment_id: Optional[int]
    event_processed: bool

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Webhook processado com sucesso",
                "payment_id": 123,
                "event_processed": True
            }
        }
    }
