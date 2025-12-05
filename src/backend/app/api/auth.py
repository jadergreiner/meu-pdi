"""
Endpoints de autenticação da API.

Este módulo contém todos os endpoints relacionados à autenticação:
registro, login, refresh token, validação de email, reset de senha.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import usuarios_db, tokens_validacao, tokens_reset_senha
from app.db.session import get_db
from app.models.schemas import (
    EmailValidationRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserBasicInfo,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.models.user import User

# Instâncias globais
security = HTTPBearer()

# JWT Manager (simplificado - será movido para core)
class JWTManager:
    """Gerenciador JWT usando Authlib para recursos avançados"""

    def __init__(self):
        self.private_key = settings.jwt_secret_key
        self.public_key = settings.jwt_secret_key  # Para HS256, mesma chave
        self.algorithm = settings.jwt_algorithm

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Cria token JWT de acesso usando Authlib"""
        from authlib.jose import jwt as authlib_jwt

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)

        to_encode.update({
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access"
        })

        header = {"alg": self.algorithm, "typ": "JWT"}
        token = authlib_jwt.encode(header, to_encode, self.private_key)
        return token.decode('utf-8') if isinstance(token, bytes) else token

    def create_refresh_token(self, data: dict) -> str:
        """Cria token JWT de refresh usando Authlib"""
        from authlib.jose import jwt as authlib_jwt

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_token_expire_days)

        to_encode.update({
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "refresh"
        })

        header = {"alg": self.algorithm, "typ": "JWT"}
        token = authlib_jwt.encode(header, to_encode, self.private_key)
        return token.decode('utf-8') if isinstance(token, bytes) else token

    def decode_token(self, token: str) -> dict:
        """Decodifica e valida token JWT usando Authlib"""
        from authlib.jose import jwt as authlib_jwt
        from jwt import PyJWTError

        try:
            claims = authlib_jwt.decode(token, self.public_key)
            claims.validate()
            return claims
        except Exception as e:
            raise PyJWTError(f"Token inválido: {str(e)}")

    def verify_token_type(self, claims: dict, expected_type: str) -> bool:
        """Verifica se o token é do tipo esperado"""
        return claims.get("type") == expected_type

# Instância global do gerenciador JWT
jwt_manager = JWTManager()

# Funções de autenticação
def hash_password(password: str) -> str:
    """Gera hash seguro da senha usando hashlib (simplificado para desenvolvimento)"""
    import hashlib
    import secrets

    # Para desenvolvimento, usar hash simples com salt
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha plain corresponde ao hash"""
    import hashlib

    try:
        salt, hash_value = hashed_password.split(':', 1)
        expected = hashlib.sha256(f"{salt}{plain_password}".encode()).hexdigest()
        return expected == hash_value
    except:
        return False

def authenticate_user(email: str, password: str):
    """Autentica usuário por email e senha"""
    # Procurar usuário por email
    user = None
    user_id = None
    for uid, u in usuarios_db.items():
        if u["email"] == email:
            user = u
            user_id = uid
            break

    if not user:
        return False

    # Verificar senha
    if not verify_password(password, user["senha_hash"]):
        return False

    # Retornar dados do usuário para login
    return {
        "id": user_id,
        "nome_completo": user["nome_completo"],
        "email": user["email"],
        "email_validado": user["email_validado"],
        "data_cadastro": user["data_cadastro"]
    }

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register_user(user: UserRegister):
    """
    Endpoint para registro de novos usuarios no Portal do Aluno.

    Valida:
    - Email unico
    - Senha forte (feito pelo validator)
    - Confirmacao de senha (feito pelo validator)
    - Aceite dos termos

    Retorna tokens JWT para login automatico apos registro.
    """
    # Validar email unico
    if any(u["email"] == user.email for u in usuarios_db.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ja cadastrado no sistema"
        )

    # Validar aceite dos termos
    if not user.aceitar_termos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aceite dos termos de uso e LGPD e obrigatorio"
        )

    # Gerar ID unico e token de validacao
    user_id = str(uuid.uuid4())
    token_validacao = str(uuid.uuid4())

    # Criar usuario
    novo_usuario = {
        "id": user_id,
        "nome_completo": user.nome_completo,
        "email": user.email,
        "senha_hash": hash_password(user.senha),  # Hash da senha
        "email_validado": False,
        "data_cadastro": datetime.now(timezone.utc),
        "token_validacao": token_validacao,
        "token_expiracao": datetime.now(timezone.utc) + timedelta(hours=24),
        # Campos do perfil (inicialmente vazios)
        "foto_perfil": None,
        "cargo_atual": None,
        "empresa_atual": None,
        "bio": None,
        "linkedin_url": None,
        "github_url": None,
        # Dados iniciais do PDI
        "pdi": {
            "status": "iniciando",
            "objetivos": [],
            "progresso": 0.0,
            "ultima_atualizacao": datetime.now(timezone.utc),
            "proximas_acoes": ["Completar perfil profissional", "Agendar primeira sessao de mentoria"]
        }
    }

    # Salvar no banco (simulado)
    usuarios_db[user_id] = novo_usuario
    tokens_validacao[token_validacao] = {
        "user_id": user_id,
        "expiracao": novo_usuario["token_expiracao"]
    }

    # Criar tokens JWT para login automatico
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = jwt_manager.create_access_token(
        data={"sub": user_id, "email": user.email},
        expires_delta=access_token_expires
    )

    refresh_token = jwt_manager.create_refresh_token(
        data={"sub": user_id, "email": user.email}
    )

    # Retornar resposta com tokens (login automatico)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserBasicInfo(
            id=user_id,
            nome_completo=user.nome_completo,
            email=user.email,
            email_validado=False,
            data_cadastro=novo_usuario["data_cadastro"]
        )
    )


@router.post("/login", response_model=TokenResponse)
async def login_user(user_credentials: UserLogin):
    """
    Endpoint para login de usuários.

    Valida credenciais e retorna token JWT de acesso.
    """
    # Autenticar usuário
    user = authenticate_user(user_credentials.email, user_credentials.senha)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Criar token de acesso
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = jwt_manager.create_access_token(
        data={"sub": user["id"], "email": user["email"]},
        expires_delta=access_token_expires
    )

    # Criar token de refresh
    refresh_token = jwt_manager.create_refresh_token(
        data={"sub": user["id"], "email": user["email"]}
    )

    # Preparar dados do usuário para resposta (sem senha)
    user_response = UserBasicInfo(
        id=user["id"],
        nome_completo=user["nome_completo"],
        email=user["email"],
        email_validado=user["email_validado"],
        data_cadastro=user["data_cadastro"]
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user_response
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(request: RefreshTokenRequest):
    """
    Endpoint para renovar token de acesso usando refresh token.

    Recebe refresh token e retorna novo par access/refresh token.
    """
    from jwt import PyJWTError

    try:
        # Decodificar e validar refresh token
        claims = jwt_manager.decode_token(request.refresh_token)

        # Verificar se é um token de refresh
        if not jwt_manager.verify_token_type(claims, "refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido - tipo incorreto"
            )

        user_id = claims.get("sub")
        user_email = claims.get("email")

        if not user_id or not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido - dados ausentes"
            )

        # Verificar se usuário ainda existe
        if user_id not in usuarios_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        user = usuarios_db[user_id]

        # Criar novos tokens
        access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        new_access_token = jwt_manager.create_access_token(
            data={"sub": user_id, "email": user_email},
            expires_delta=access_token_expires
        )

        new_refresh_token = jwt_manager.create_refresh_token(
            data={"sub": user_id, "email": user_email}
        )

        # Preparar dados do usuário para resposta
        user_response = {
            "id": user_id,
            "nome_completo": user["nome_completo"],
            "email": user["email"],
            "email_validado": user["email_validado"],
            "data_cadastro": user["data_cadastro"]
        }

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            user=user_response
        )

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado"
        )


@router.post("/validate-email")
async def validar_email(request: EmailValidationRequest):
    """
    Endpoint para validar email através de token.

    Recebe o token enviado por email e marca o usuário como validado.
    """
    token = request.token

    # Validar token
    if token not in tokens_validacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido"
        )

    token_info = tokens_validacao[token]

    # Verificar expiração
    if datetime.now(timezone.utc) > token_info["expiracao"]:
        # Token expirado, remover
        del tokens_validacao[token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expirado"
        )

    user_id = token_info["user_id"]

    # Verificar se usuário existe
    if user_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Marcar email como validado
    usuarios_db[user_id]["email_validado"] = True

    # Remover token usado
    del tokens_validacao[token]

    return {
        "message": "Email validado com sucesso",
        "email_validado": True
    }


@router.post("/reset-password", response_model=dict)
async def solicitar_reset_senha(request: PasswordResetRequest):
    """
    Solicita reset de senha para um usuário.
    Gera token único e simula envio por email.
    """
    # Verificar se usuário existe
    user_id = None
    for uid, user_data in usuarios_db.items():
        if user_data["email"] == request.email:
            user_id = uid
            break

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Gerar token único para reset
    reset_token = str(uuid.uuid4())

    # Armazenar token com expiração (1 hora)
    tokens_reset_senha[reset_token] = {
        "user_id": user_id,
        "expiracao": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    # Simular envio de email (em produção seria email real)
    # TODO: Integrar com serviço de email

    return {
        "message": "Email de reset enviado com sucesso",
        "token": reset_token,  # Em produção, isso não seria retornado
        "expiracao": tokens_reset_senha[reset_token]["expiracao"].isoformat()
    }


@router.post("/confirm-reset-password", response_model=dict)
async def confirmar_reset_senha(request: PasswordResetConfirm):
    """
    Confirma reset de senha usando token válido.
    Atualiza senha do usuário.
    """
    # Verificar se token existe
    if request.token not in tokens_reset_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido"
        )

    token_info = tokens_reset_senha[request.token]

    # Verificar expiração
    if datetime.now(timezone.utc) > token_info["expiracao"]:
        # Remover token expirado
        del tokens_reset_senha[request.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expirado"
        )

    user_id = token_info["user_id"]

    # Verificar se usuário ainda existe
    if user_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Atualizar senha do usuário
    usuarios_db[user_id]["senha_hash"] = hash_password(request.nova_senha)

    # Remover token usado
    del tokens_reset_senha[request.token]

    return {
        "message": "Senha alterada com sucesso"
    }