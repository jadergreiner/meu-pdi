"""
Endpoints de usuários da API.

Este módulo contém todos os endpoints relacionados aos usuários:
perfil, PDI, próximas ações, configurações responsivas.
"""

from datetime import datetime, timezone
from typing import Dict, Optional
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError

from app.core.config import settings
from app.core.database import usuarios_db
from app.models.schemas import (
    NextSteps,
    PDIOverview,
    ResponsiveConfig,
    UserProfile,
    UserStatistics,
)

# Instâncias globais
security = HTTPBearer()

# JWT Manager (simplificado - será movido para core)
class JWTManager:
    """Gerenciador JWT usando Authlib para recursos avançados"""

    def __init__(self):
        self.private_key = settings.jwt_secret_key
        self.public_key = settings.jwt_secret_key  # Para HS256, mesma chave
        self.algorithm = settings.jwt_algorithm

    def decode_token(self, token: str) -> dict:
        """Decodifica e valida token JWT usando Authlib"""
        from authlib.jose import jwt as authlib_jwt

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

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obtém o usuário atual a partir do token JWT usando Authlib"""
    try:
        claims = jwt_manager.decode_token(credentials.credentials)

        # Verificar se é um token de acesso
        if not jwt_manager.verify_token_type(claims, "access"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido - tipo incorreto"
            )

        user_id: str = claims.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido - user_id não encontrado"
            )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )

    # Verificar se usuário existe
    if user_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return usuarios_db[user_id]

router = APIRouter()


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Retorna o perfil completo do usuário autenticado"""
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


@router.get("/pdi/overview", response_model=PDIOverview)
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


@router.get("/next-steps", response_model=NextSteps)
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
            "url": "/profile/edit"
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


@router.get("/dashboard/config")
async def get_responsive_config(current_user: dict = Depends(get_current_user)):
    """
    Endpoint para obter configurações responsivas do dashboard.

    Retorna configurações otimizadas para diferentes dispositivos.
    """
    return ResponsiveConfig(
        breakpoints={
            "mobile": 768,
            "tablet": 1024,
            "desktop": 1440
        },
        layout={
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
        responsive_features={
            "touch_friendly": True,
            "lazy_loading": True,
            "compressed_images": True,
            "minimal_payloads": True,
            "adaptive_images": True,
            "offline_support": False
        }
    )


@router.get("/statistics", response_model=UserStatistics)
async def get_user_statistics(current_user: dict = Depends(get_current_user)):
    """
    Retorna estatísticas e métricas do usuário para o dashboard.

    Inclui métricas de engajamento, progresso e atividade.
    """
    # Calcular dias ativos (simulado - em produção viria do banco)
    data_cadastro = current_user.get("data_cadastro", datetime.now(timezone.utc))
    dias_desde_cadastro = (datetime.now(timezone.utc) - data_cadastro).days
    dias_ativos = min(dias_desde_cadastro, 30)  # Máximo 30 dias para MVP

    # Calcular objetivos completados
    pdi_data = current_user.get("pdi", {})
    objetivos = pdi_data.get("objetivos", [])
    objetivos_completados = sum(1 for obj in objetivos if obj.get("status") == "concluido")

    # Calcular progresso mensal (simulado)
    progresso_mensal = min(objetivos_completados * 25.0, 100.0)  # 25% por objetivo

    # Calcular sessões realizadas
    sessoes_agendadas = current_user.get("sessoes_agendadas", [])
    sessoes_realizadas = sum(1 for sessao in sessoes_agendadas if sessao.get("status") == "realizada")

    # Calcular horas dedicadas (estimativa baseada em sessões)
    horas_dedicadas = sessoes_realizadas * 1.5  # 1.5h por sessão

    # Calcular streak atual (simulado - dias consecutivos)
    streak_atual = min(dias_ativos, 7)  # Máximo 7 dias para MVP

    # Determinar nível de engajamento
    if progresso_mensal >= 75 and sessoes_realizadas >= 2:
        nivel_engajamento = "alto"
    elif progresso_mensal >= 50 or sessoes_realizadas >= 1:
        nivel_engajamento = "medio"
    else:
        nivel_engajamento = "baixo"

    # Última atividade (usar última atualização do PDI ou data de cadastro)
    ultima_atualizacao_pdi = pdi_data.get("ultima_atualizacao")
    ultima_atividade = ultima_atualizacao_pdi if ultima_atualizacao_pdi else data_cadastro

    return UserStatistics(
        dias_ativos=dias_ativos,
        objetivos_completados=objetivos_completados,
        progresso_mensal=round(progresso_mensal, 1),
        sessoes_realizadas=sessoes_realizadas,
        horas_dedicadas=round(horas_dedicadas, 1),
        streak_atual=streak_atual,
        nivel_engajamento=nivel_engajamento,
        ultima_atividade=ultima_atividade
    )