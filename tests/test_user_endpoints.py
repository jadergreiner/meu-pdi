"""
Testes para endpoints de usuários.

Testa funcionalidades de perfil, PDI, próximas ações e estatísticas.
"""

import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.backend.main import app
from src.backend.app.core.database import usuarios_db


@pytest.fixture
def client():
    """Cliente de teste para a API."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Headers de autenticação para testes."""
    # Mock do token JWT para testes
    return {"Authorization": "Bearer mock_token"}


@pytest.fixture
def test_user():
    """Usuário de teste com dados completos."""
    user_id = "test_user_123"
    user_data = {
        "id": user_id,
        "nome_completo": "João Silva",
        "email": "joao.silva@email.com",
        "email_validado": True,
        "data_cadastro": datetime.now(timezone.utc),
        "foto_perfil": "https://example.com/foto.jpg",
        "cargo_atual": "Desenvolvedor Pleno",
        "empresa_atual": "Tech Corp",
        "bio": "Desenvolvedor apaixonado por tecnologia",
        "linkedin_url": "https://linkedin.com/in/joaosilva",
        "github_url": "https://github.com/joaosilva",
        "perfil_completo": True,
        "pdi": {
            "status": "em_andamento",
            "objetivos": [
                {"titulo": "Aprender React", "status": "concluido"},
                {"titulo": "Certificação AWS", "status": "em_andamento"},
                {"titulo": "Liderança Técnica", "status": "pendente"}
            ],
            "progresso": 65.0,
            "ultima_atualizacao": datetime.now(timezone.utc) - timedelta(days=2),
            "proximas_acoes": ["Revisar objetivos", "Agendar mentoria"]
        },
        "sessoes_agendadas": [
            {"id": "sessao_1", "status": "realizada", "data": datetime.now(timezone.utc) - timedelta(days=7)},
            {"id": "sessao_2", "status": "realizada", "data": datetime.now(timezone.utc) - timedelta(days=3)},
            {"id": "sessao_3", "status": "agendada", "data": datetime.now(timezone.utc) + timedelta(days=7)}
        ]
    }
    usuarios_db[user_id] = user_data
    return user_data


class TestUserEndpoints:
    """Testes para endpoints de usuários."""

    @patch('src.backend.app.api.users.jwt_manager.decode_token')
    @patch('src.backend.app.api.users.jwt_manager.verify_token_type')
    def test_get_user_profile_success(self, mock_verify_type, mock_decode, client, auth_headers, test_user):
        """Testa obtenção bem-sucedida do perfil do usuário."""
        # Mock do JWT
        mock_decode.return_value = {"sub": test_user["id"], "type": "access"}
        mock_verify_type.return_value = True

        response = client.get("/users/profile", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user["id"]
        assert data["nome_completo"] == test_user["nome_completo"]
        assert data["email"] == test_user["email"]
        assert data["cargo_atual"] == test_user["cargo_atual"]

    @patch('src.backend.app.api.users.jwt_manager.decode_token')
    @patch('src.backend.app.api.users.jwt_manager.verify_token_type')
    def test_get_pdi_overview_success(self, mock_verify_type, mock_decode, client, auth_headers, test_user):
        """Testa obtenção bem-sucedida da visão geral do PDI."""
        mock_decode.return_value = {"sub": test_user["id"], "type": "access"}
        mock_verify_type.return_value = True

        response = client.get("/users/pdi/overview", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status_geral"] == "em_andamento"
        assert data["objetivos_ativos"] == 3
        assert data["progresso_percentual"] == 65.0

    @patch('src.backend.app.api.users.get_current_user')
    def test_get_user_statistics_success(self, mock_get_current_user, client, test_user):
        """Testa obtenção bem-sucedida das estatísticas do usuário."""
        mock_get_current_user.side_effect = lambda: test_user

        response = client.get("/users/statistics")

        assert response.status_code == 200
        data = response.json()

        # Verificar campos obrigatórios
        assert "dias_ativos" in data
        assert "objetivos_completados" in data
        assert "progresso_mensal" in data
        assert "sessoes_realizadas" in data
        assert "horas_dedicadas" in data
        assert "streak_atual" in data
        assert "nivel_engajamento" in data

        # Verificar cálculos
        assert data["objetivos_completados"] == 1  # Apenas "Aprender React" está concluído
        assert data["sessoes_realizadas"] == 2  # Duas sessões com status "realizada"
        assert data["horas_dedicadas"] == 3.0  # 2 sessões * 1.5h
        assert data["nivel_engajamento"] in ["baixo", "medio", "alto"]

    @patch('src.backend.app.api.users.jwt_manager.decode_token')
    @patch('src.backend.app.api.users.jwt_manager.verify_token_type')
    def test_get_user_statistics_new_user(self, mock_verify_type, mock_decode, client, auth_headers):
        """Testa estatísticas para usuário novo sem PDI."""
        # Criar usuário novo
        new_user_id = "new_user_456"
        new_user = {
            "id": new_user_id,
            "nome_completo": "Maria Santos",
            "email": "maria.santos@email.com",
            "email_validado": False,
            "data_cadastro": datetime.now(timezone.utc),
            "perfil_completo": False
        }
        usuarios_db[new_user_id] = new_user

        mock_decode.return_value = {"sub": new_user_id, "type": "access"}
        mock_verify_type.return_value = True

        response = client.get("/users/statistics", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Usuário novo deve ter estatísticas zeradas ou mínimas
        assert data["objetivos_completados"] == 0
        assert data["sessoes_realizadas"] == 0
        assert data["horas_dedicadas"] == 0.0
        assert data["nivel_engajamento"] == "baixo"

        # Limpar dados de teste
        del usuarios_db[new_user_id]

    @patch('src.backend.app.api.users.jwt_manager.decode_token')
    @patch('src.backend.app.api.users.jwt_manager.verify_token_type')
    def test_get_next_steps_success(self, mock_verify_type, mock_decode, client, auth_headers, test_user):
        """Testa obtenção bem-sucedida das próximas ações."""
        mock_decode.return_value = {"sub": test_user["id"], "type": "access"}
        mock_verify_type.return_value = True

        response = client.get("/users/next-steps", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "acoes_recomendadas" in data
        assert isinstance(data["acoes_recomendadas"], list)

    @patch('src.backend.app.api.users.jwt_manager.decode_token')
    @patch('src.backend.app.api.users.jwt_manager.verify_token_type')
    def test_unauthorized_access(self, mock_verify_type, mock_decode, client):
        """Testa acesso não autorizado sem token válido."""
        mock_decode.side_effect = Exception("Token inválido")

        response = client.get("/users/profile")

        assert response.status_code == 401
        assert "Token inválido" in response.json()["detail"]

    @patch('src.backend.app.api.users.jwt_manager.decode_token')
    @patch('src.backend.app.api.users.jwt_manager.verify_token_type')
    def test_user_not_found(self, mock_verify_type, mock_decode, client, auth_headers):
        """Testa erro quando usuário não existe."""
        mock_decode.return_value = {"sub": "nonexistent_user", "type": "access"}
        mock_verify_type.return_value = True

        response = client.get("/users/profile", headers=auth_headers)

        assert response.status_code == 404
        assert "Usuário não encontrado" in response.json()["detail"]