# TASK-T001: Formulario de Cadastro Otimizado
# Implementacao inicial do backend FastAPI para Portal do Aluno

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional, List
import re
import uuid
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import bcrypt
import jwt
from jwt import PyJWTError

app = FastAPI(title="Meu PDI - Portal do Aluno", version="1.0.0")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações de segurança
SECRET_KEY = "your-secret-key-here-change-in-production"  # TODO: Mover para variáveis de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hash de senhas
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__default_rounds=12,
    bcrypt__ident="2b"  # Força versão específica do bcrypt
)

# Bearer token security
security = HTTPBearer()

# Modelos Pydantic para validacao
class UserRegister(BaseModel):
    nome_completo: str = Field(..., min_length=2, max_length=100, description="Nome completo do usuario")
    email: EmailStr = Field(..., description="Email profissional valido")
    senha: str = Field(..., min_length=8, max_length=128, description="Senha forte (8+ caracteres)")
    confirmar_senha: str = Field(..., description="Confirmacao da senha")
    aceitar_termos: bool = Field(..., description="Aceite dos termos de uso e LGPD")

    model_config = {
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
            raise ValueError('Senha deve ter pelo menos 8 caracteres, com maiuscula, minuscula, numero e caractere especial')
        return v

    @model_validator(mode='after')
    def senhas_devem_ser_iguais(self):
        if self.senha != self.confirmar_senha:
            raise ValueError('Confirmacao de senha nao coincide')
        return self

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email do usuario")
    senha: str = Field(..., description="Senha do usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "joao.silva@email.com",
                "senha": "MinhaSenhaForte123!"
            }
        }
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: str
    nome_completo: str
    email: str
    email_validado: bool
    data_cadastro: datetime
    token_validacao: str

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="Email do usuario para reset de senha")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "joao.silva@email.com"
            }
        }
    }

class EmailValidationRequest(BaseModel):
    token: str = Field(..., description="Token de validacao enviado por email")

    model_config = {
        "json_schema_extra": {
            "example": {
                "token": "abc123-def456-ghi789"
            }
        }
    }

class PasswordResetConfirm(BaseModel):
    token: str = Field(..., description="Token de reset recebido por email")
    nova_senha: str = Field(..., min_length=8, description="Nova senha forte")
    confirmar_senha: str = Field(..., description="Confirmacao da nova senha")

    @model_validator(mode='after')
    def senhas_reset_devem_ser_iguais(self):
        if self.nova_senha != self.confirmar_senha:
            raise ValueError('Confirmacao de senha nao coincide')
        return self

    @field_validator('nova_senha')
    @classmethod
    def nova_senha_deve_ser_forte(cls, v):
        if not validar_senha_forte(v):
            raise ValueError(
                'Senha deve ter pelo menos 8 caracteres, '
                'uma letra maiuscula, uma minuscula, um numero e um caractere especial'
            )
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "token": "abc123-def456-ghi789",
                "nova_senha": "NovaSenhaForte123!",
                "confirmar_senha": "NovaSenhaForte123!"
            }
        }
    }

class UserProfile(BaseModel):
    """Modelo para resposta do perfil do usuário"""
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

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nome_completo": "João Silva",
                "email": "joao.silva@email.com",
                "email_validado": True,
                "data_cadastro": "2025-11-02T10:30:00Z",
                "foto_perfil": "https://example.com/foto.jpg",
                "cargo_atual": "Desenvolvedor Senior",
                "empresa_atual": "Tech Company Ltda",
                "bio": "Desenvolvedor apaixonado por tecnologia e mentoria",
                "linkedin_url": "https://linkedin.com/in/joaosilva",
                "github_url": "https://github.com/joaosilva"
            }
        }
    }

class PDIOverview(BaseModel):
    """Modelo para visão geral do PDI do usuário"""
    status_geral: str = Field(..., description="Status geral do PDI", examples=["iniciando", "em_andamento", "avancado"])
    objetivos_ativos: int = Field(..., description="Número de objetivos ativos", ge=0)
    progresso_percentual: float = Field(..., description="Progresso geral em percentual", ge=0.0, le=100.0)
    proximas_acoes: List[str] = Field(..., description="Próximas ações recomendadas")
    ultima_atualizacao: datetime = Field(..., description="Última atualização do PDI")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_geral": "iniciando",
                "objetivos_ativos": 0,
                "progresso_percentual": 0.0,
                "proximas_acoes": ["Completar perfil profissional", "Agendar primeira sessão de mentoria"],
                "ultima_atualizacao": "2025-11-02T10:30:00Z"
            }
        }
    }

class NextSteps(BaseModel):
    """Modelo para próximas ações recomendadas ao usuário"""
    acoes_recomendadas: List[dict] = Field(..., description="Lista de ações recomendadas")

    model_config = {
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

class ResponsiveConfig(BaseModel):
    """Modelo para configurações responsivas do dashboard"""
    breakpoints: dict = Field(..., description="Breakpoints para responsividade")
    layout: dict = Field(..., description="Configurações de layout")
    responsive_features: dict = Field(..., description="Features responsivas habilitadas")

    model_config = {
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

# Validacao de senha forte
def validar_senha_forte(senha: str) -> bool:
    """
    Valida se a senha atende criterios de seguranca:
    - Pelo menos 8 caracteres
    - Pelo menos uma letra maiuscula
    - Pelo menos uma letra minuscula
    - Pelo menos um numero
    - Pelo menos um caractere especial
    """
    if len(senha) < 8:
        return False

    # Verificar criterios usando regex
    criterios = [
        r'[A-Z]',  # Maiuscula
        r'[a-z]',  # Minuscula
        r'[0-9]',  # Numero
        r'[!@#$%^&*(),.?":{}|<>]'  # Caractere especial
    ]

    return all(re.search(criterio, senha) for criterio in criterios)

# Simulacao de banco de dados (temporario - sera substituido por PostgreSQL)
usuarios_db = {
    "test-user-uuid-123": {
        "id": "test-user-uuid-123",
        "nome_completo": "Usuario Teste",
        "email": "teste@meupdi.com",
        "senha_hash": "$2b$12$r1sgqYpI4JEAbrceV0G/Q.5UU0jY/NBS.FUTDHVaJGJKHxyK/.zwW",  # senha: Teste123!
        "telefone": "(11) 99999-9999",
        "cargo_atual": "Desenvolvedor Pleno",
        "empresa_atual": "Empresa Teste",
        "experiencia_anos": 5,
        "area_interesse": "Backend Development",
        "objetivos_carreira": "Tornar-se Senior e lider tecnico",
        "data_cadastro": "2024-01-15T10:00:00Z",
        "status": "ativo",
        "email_validado": True,
        "token_validacao": None,
        "token_expiracao": None,
        "pdi_atual": {
            "titulo": "Plano de Desenvolvimento Individual - 2024",
            "status": "em_andamento",
            "data_criacao": "2024-01-15T10:00:00Z",
            "competencias": [
                {"nome": "Lideranca Tecnica", "nivel_atual": 3, "nivel_desejado": 5, "acoes": ["Mentorar juniors", "Apresentar em conferencias"]},
                {"nome": "Arquitetura de Sistemas", "nivel_atual": 4, "nivel_desejado": 5, "acoes": ["Estudar DDD", "Implementar microservicos"]},
                {"nome": "Comunicacao", "nivel_atual": 2, "nivel_desejado": 4, "acoes": ["Cursos de apresentacao", "Praticar feedback"]}
            ],
            "proximos_passos": [
                {"titulo": "Mentoria com Senior", "data": "2024-02-01", "status": "agendado"},
                {"titulo": "Curso de Arquitetura", "data": "2024-02-15", "status": "planejado"}
            ],
            "status": "iniciando",
            "objetivos": [],
            "progresso": 0.0,
            "ultima_atualizacao": "2024-01-15T10:00:00Z",
            "proximas_acoes": ["Completar perfil profissional", "Agendar primeira sessão de mentoria"]
        }
    }
}
tokens_validacao = {}
tokens_reset_senha = {}

# Funções de autenticação
def hash_password(password: str) -> str:
    """Gera hash seguro da senha usando bcrypt"""
    # bcrypt limita senhas a 72 bytes, truncar se necessário
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha plain corresponde ao hash"""
    # bcrypt limita senhas a 72 bytes, truncar se necessário
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria token JWT de acesso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

@app.post("/register", response_model=UserResponse)
async def register_user(user: UserRegister):
    """
    Endpoint para registro de novos usuarios no Portal do Aluno.

    Valida:
    - Email unico
    - Senha forte (feito pelo validator)
    - Confirmacao de senha (feito pelo validator)
    - Aceite dos termos
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
            "proximas_acoes": ["Completar perfil profissional", "Agendar primeira sessão de mentoria"]
        }
    }

    # Salvar no banco (simulado)
    usuarios_db[user_id] = novo_usuario
    tokens_validacao[token_validacao] = {
        "user_id": user_id,
        "expiracao": novo_usuario["token_expiracao"]
    }

    # Retornar resposta
    return UserResponse(
        id=user_id,
        nome_completo=user.nome_completo,
        email=user.email,
        email_validado=False,
        data_cadastro=novo_usuario["data_cadastro"],
        token_validacao=token_validacao
    )

@app.post("/login", response_model=TokenResponse)
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
            detail="Email ou senha invalidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Criar token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]},
        expires_delta=access_token_expires
    )

    # Preparar dados do usuário para resposta (sem senha)
    user_response = {
        "id": user["id"],
        "nome_completo": user["nome_completo"],
        "email": user["email"],
        "email_validado": user["email_validado"],
        "data_cadastro": user["data_cadastro"]
    }

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@app.get("/health")
async def health_check():
    """Endpoint de verificacao de saude da API"""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

# TASK-T005: Perfil do Usuário Completo
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obtem o usuario atual a partir do token JWT"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido - user_id nao encontrado"
            )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou expirado"
        )

    # Verificar se usuario existe
    if user_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado"
        )

    return usuarios_db[user_id]

@app.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Retorna o perfil completo do usuario autenticado"""
    return UserProfile(
        id=current_user["id"],
        nome_completo=current_user["nome_completo"],
        email=current_user["email"],
        email_validado=current_user["email_validado"],
        data_cadastro=current_user["data_cadastro"],
        foto_perfil=current_user.get("foto_perfil"),
        cargo_atual=current_user.get("cargo_atual"),
        empresa_atual=current_user.get("empresa_atual"),
        bio=current_user.get("bio"),
        linkedin_url=current_user.get("linkedin_url"),
        github_url=current_user.get("github_url")
    )

@app.get("/pdi/overview", response_model=PDIOverview)
async def get_pdi_overview(current_user: dict = Depends(get_current_user)):
    """Retorna visão geral do PDI do usuário autenticado"""
    pdi_data = current_user.get("pdi", {})

    # Garantir valores padrão se PDI não existir
    if not pdi_data:
        pdi_data = {
            "status": "iniciando",
            "objetivos": [],
            "progresso": 0.0,
            "ultima_atualizacao": datetime.now(timezone.utc),
            "proximas_acoes": ["Completar perfil profissional", "Agendar primeira sessão de mentoria"]
        }

    return PDIOverview(
        status_geral=pdi_data.get("status", "iniciando"),
        objetivos_ativos=len(pdi_data.get("objetivos", [])),
        progresso_percentual=pdi_data.get("progresso", 0.0),
        proximas_acoes=pdi_data.get("proximas_acoes", []),
        ultima_atualizacao=pdi_data.get("ultima_atualizacao", datetime.now(timezone.utc))
    )

@app.get("/next-steps", response_model=NextSteps)
async def get_next_steps(current_user: dict = Depends(get_current_user)):
    """Retorna próximas ações recomendadas para o usuário autenticado"""
    acoes_recomendadas = []

    # Verificar perfil incompleto
    perfil_completo = current_user.get("perfil_completo", False)
    if not perfil_completo:
        acoes_recomendadas.append({
            "titulo": "Completar Perfil Profissional",
            "descricao": "Adicione informações sobre sua experiência, habilidades e objetivos para personalizar sua jornada",
            "prioridade": "alta",
            "url": "/profile/complete"
        })

    # Verificar PDI iniciado
    pdi_data = current_user.get("pdi", {})
    if not pdi_data or pdi_data.get("status") == "iniciando":
        acoes_recomendadas.append({
            "titulo": "Criar Primeiro PDI",
            "descricao": "Defina seus objetivos de desenvolvimento profissional com orientação estruturada",
            "prioridade": "alta",
            "url": "/pdi/create"
        })

    # Verificar sessões de mentoria
    sessoes_agendadas = current_user.get("sessoes_agendadas", [])
    if len(sessoes_agendadas) == 0:
        acoes_recomendadas.append({
            "titulo": "Agendar Sessão de Mentoria",
            "descricao": "Conecte-se com um mentor experiente para acelerar seu desenvolvimento",
            "prioridade": "media",
            "url": "/mentoring/schedule"
        })

    # Verificar progresso semanal
    ultima_atualizacao = pdi_data.get("ultima_atualizacao")
    if ultima_atualizacao:
        dias_sem_atualizar = (datetime.now(timezone.utc) - ultima_atualizacao).days
        if dias_sem_atualizar > 7:
            acoes_recomendadas.append({
                "titulo": "Atualizar Progresso Semanal",
                "descricao": "Registre suas conquistas e desafios da semana para manter o PDI atualizado",
                "prioridade": "media",
                "url": "/pdi/update"
            })

    # Ações padrão se nenhuma específica se aplicar
    if not acoes_recomendadas:
        acoes_recomendadas.append({
            "titulo": "Explorar Recursos da Plataforma",
            "descricao": "Conheça ferramentas e conteúdos disponíveis para seu desenvolvimento",
            "prioridade": "baixa",
            "url": "/resources"
        })

    return NextSteps(acoes_recomendadas=acoes_recomendadas)

# TODO: Implementar endpoints adicionais:
# - POST /validate-email (TASK-T002)
# - POST /login (TASK-T003)
# - POST /reset-password (TASK-T004)

# TASK-T002: Sistema de Validação Email Robusto
def criar_token_validacao():
    """Cria um token único para validação de email"""
    return str(uuid.uuid4())

def validar_token_email(token: str) -> bool:
    """
    Valida se um token de email é válido e não expirou.

    Returns:
        bool: True se o token é válido, False caso contrário
    """
    if token not in tokens_validacao:
        return False

    token_info = tokens_validacao[token]
    if datetime.now(timezone.utc) > token_info["expiracao"]:
        # Token expirado, remover
        del tokens_validacao[token]
        return False

    return True

@app.post("/validate-email")
async def validar_email(request: EmailValidationRequest):
    """
    Endpoint para validar email através de token.

    Recebe o token enviado por email e marca o usuário como validado.
    """
    token = request.token
    # Validar token
    if not validar_token_email(token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token invalido ou expirado"
        )

    # Obter informações do token
    token_info = tokens_validacao[token]
    user_id = token_info["user_id"]

    # Verificar se usuário existe
    if user_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado"
        )

    # Marcar email como validado
    usuarios_db[user_id]["email_validado"] = True

    # Remover token usado
    del tokens_validacao[token]

    return {
        "message": "Email validado com sucesso",
        "email_validado": True
    }

# TASK-T004: Recuperação de Senha Confiável
@app.post("/reset-password", response_model=dict)
async def solicitar_reset_senha(request: PasswordResetRequest):
    """
    Solicita reset de senha para um usuario.
    Gera token unico e envia por email (simulado).
    """
    # Verificar se usuario existe
    user_id = None
    for uid, user_data in usuarios_db.items():
        if user_data["email"] == request.email:
            user_id = uid
            break

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado"
        )

    # Gerar token unico para reset
    import uuid
    reset_token = str(uuid.uuid4())

    # Armazenar token com expiracao (1 hora)
    tokens_reset_senha[reset_token] = {
        "user_id": user_id,
        "expiracao": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    # Simular envio de email (em producao seria email real)
    # TODO: Integrar com servico de email

    return {
        "message": "Email de reset enviado com sucesso",
        "token": reset_token,  # Em producao, isso nao seria retornado
        "expiracao": tokens_reset_senha[reset_token]["expiracao"].isoformat()
    }

@app.post("/confirm-reset-password", response_model=dict)
async def confirmar_reset_senha(request: PasswordResetConfirm):
    """
    Confirma reset de senha usando token valido.
    Atualiza senha do usuario.
    """
    # Verificar se token existe
    if request.token not in tokens_reset_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token invalido"
        )

    token_info = tokens_reset_senha[request.token]

    # Verificar expiracao
    if datetime.now(timezone.utc) > token_info["expiracao"]:
        # Remover token expirado
        del tokens_reset_senha[request.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expirado"
        )

    user_id = token_info["user_id"]

    # Verificar se usuario ainda existe
    if user_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado"
        )

    # Atualizar senha do usuario
    usuarios_db[user_id]["senha_hash"] = hash_password(request.nova_senha)

    # Remover token usado
    del tokens_reset_senha[request.token]

    return {
        "message": "Senha alterada com sucesso"
    }

# TASK-T008: Layout Responsivo
@app.get("/dashboard/config")
async def get_responsive_config(current_user: dict = Depends(get_current_user)):
    """
    Endpoint para obter configurações responsivas do dashboard.

    Retorna configurações otimizadas para diferentes dispositivos.
    """
    return {
        "breakpoints": {
            "mobile": 768,
            "tablet": 1024,
            "desktop": 1440
        },
        "layout": {
            "grid_columns": {
                "mobile": 1,
                "tablet": 2,
                "desktop": 3
            },
            "card_spacing": {
                "mobile": "8px",
                "tablet": "12px",
                "desktop": "16px"
            },
            "font_sizes": {
                "mobile": "14px",
                "tablet": "16px",
                "desktop": "18px"
            },
            "sidebar_collapsible": True,
            "mobile_navigation": "drawer"
        },
        "responsive_features": {
            "touch_friendly": True,
            "lazy_loading": True,
            "compressed_images": True,
            "minimal_payloads": True,
            "adaptive_images": True,
            "offline_support": False
        }
    }