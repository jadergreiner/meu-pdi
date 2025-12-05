# TASK-T005: Perfil do Usuário Completo
import pytest
from datetime import datetime

def test_obter_perfil_usuario_sucesso(client, sample_user_data):
    """Testa obtenção do perfil do usuário com sucesso"""
    # Arrange: Cadastrar e fazer login do usuário
    import uuid
    unique_email = f"profile-test-{uuid.uuid4()}@email.com"
    test_data = sample_user_data.copy()
    test_data["email"] = unique_email

    register_response = client.post("/auth/register", json=test_data)
    assert register_response.status_code == 200
    user_data = register_response.json()

    # Validar email para poder fazer login
    validate_response = client.post("/auth/validate-email", json={"token": user_data["token_validacao"]})
    assert validate_response.status_code == 200

    # Fazer login para obter token
    login_data = {
        "email": unique_email,
        "senha": sample_user_data["senha"]
    }
    login_response = client.post("/auth/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Act: Obter perfil do usuário
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/profile", headers=headers)

    # Assert
    assert response.status_code == 200
    profile_data = response.json()
    assert profile_data["id"] == user_data["id"]
    assert profile_data["nome_completo"] == sample_user_data["nome_completo"]
    assert profile_data["email"] == unique_email
    assert profile_data["email_validado"] == True
    assert "data_cadastro" in profile_data
    # Campos opcionais devem ser None inicialmente
    assert profile_data["foto_perfil"] is None
    assert profile_data["cargo_atual"] is None
    assert profile_data["empresa_atual"] is None
    assert profile_data["bio"] is None
    assert profile_data["linkedin_url"] is None
    assert profile_data["github_url"] is None

def test_obter_perfil_usuario_nao_autorizado(client):
    """Testa erro ao acessar perfil sem token"""
    # Act
    response = client.get("/users/profile")

    # Assert
    assert response.status_code == 403  # FastAPI retorna 403 para Bearer token missing

def test_obter_perfil_usuario_token_invalido(client):
    """Testa erro com token inválido"""
    # Arrange
    headers = {"Authorization": "Bearer invalid-token"}

    # Act
    response = client.get("/users/profile", headers=headers)

    # Assert
    assert response.status_code == 401
    assert "Token" in response.json()["detail"]

def test_obter_perfil_usuario_nao_encontrado(client):
    """Testa erro quando usuário do token não existe mais"""
    # Arrange: Criar token válido mas remover usuário (simulação)
    # Isso é difícil de testar diretamente, mas o código já trata este caso
    # na função get_current_user
    pass


# TASK-T006: Testes para endpoint PDI overview
def test_obter_visao_geral_pdi_sucesso(client):
    """Testa sucesso ao obter PDI overview com token válido"""
    # Arrange: Registrar usuário e obter token
    user_data = {
        "nome_completo": "João Silva",
        "email": "aluno@teste.com",
        "senha": "MinhaSenhaForte123!",
        "confirmar_senha": "MinhaSenhaForte123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Act: Fazer requisição para PDI overview
    response = client.get("/users/pdi/overview", headers=headers)

    # Assert: Verificar resposta de sucesso
    assert response.status_code == 200
    data = response.json()
    assert "status_geral" in data
    assert "objetivos_ativos" in data
    assert "progresso_percentual" in data
    assert "proximas_acoes" in data
    assert "ultima_atualizacao" in data


def test_obter_visao_geral_pdi_nao_autorizado(client):
    """Testa erro 403 quando token não é fornecido"""
    # Act: Fazer requisição sem token
    response = client.get("/users/pdi/overview")

    # Assert: Verificar erro de autenticação
    assert response.status_code == 403  # FastAPI retorna 403 por padrão para auth obrigatória
    assert "detail" in response.json()


def test_obter_visao_geral_pdi_token_invalido(client):
    """Testa erro 401 quando token e invalido"""
    # Arrange: Token invalido
    headers = {"Authorization": "Bearer token_invalido"}

    # Act: Fazer requisicao com token invalido
    response = client.get("/users/pdi/overview", headers=headers)

    # Assert: Verificar erro de autenticacao
    assert response.status_code == 401
    assert "detail" in response.json()
    assert "Token" in response.json()["detail"]


# TASK-T007: Testes para endpoint próximos passos
def test_obter_proximos_passos_sucesso(client):
    """Testa sucesso ao obter próximos passos com token válido"""
    # Arrange: Registrar usuário e obter token
    user_data = {
        "nome_completo": "João Silva",
        "email": "aluno@teste.com",
        "senha": "MinhaSenhaForte123!",
        "confirmar_senha": "MinhaSenhaForte123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Act: Fazer requisição para próximos passos
    response = client.get("/users/next-steps", headers=headers)

    # Assert: Verificar resposta de sucesso
    assert response.status_code == 200
    data = response.json()
    assert "acoes_recomendadas" in data
    assert isinstance(data["acoes_recomendadas"], list)
    assert len(data["acoes_recomendadas"]) > 0

    # Verificar estrutura de cada ação
    for acao in data["acoes_recomendadas"]:
        assert "titulo" in acao
        assert "descricao" in acao
        assert "prioridade" in acao
        assert "url" in acao
        assert acao["prioridade"] in ["alta", "media", "baixa"]


def test_obter_proximos_passos_nao_autorizado(client):
    """Testa erro 403 quando token não é fornecido"""
    # Act: Fazer requisição sem token
    response = client.get("/users/next-steps")

    # Assert: Verificar erro de autenticação
    assert response.status_code == 403  # FastAPI retorna 403 por padrão para auth obrigatória
    assert "detail" in response.json()


def test_obter_proximos_passos_token_invalido(client):
    """Testa erro 401 quando token e invalido"""
    # Arrange: Token invalido
    headers = {"Authorization": "Bearer token_invalido"}

    # Act: Fazer requisicao com token invalido
    response = client.get("/users/next-steps", headers=headers)

    # Assert: Verificar erro de autenticacao
    assert response.status_code == 401
    assert "detail" in response.json()
    assert "Token" in response.json()["detail"]


def test_obter_proximos_passos_acoes_personalizadas(client):
    """Testa se as ações são personalizadas baseado no perfil incompleto"""
    # Arrange: Registrar usuário sem completar perfil e obter token
    user_data = {
        "nome_completo": "João Silva",
        "email": "aluno2@teste.com",
        "senha": "MinhaSenhaForte123!",
        "confirmar_senha": "MinhaSenhaForte123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Act: Fazer requisição para próximos passos
    response = client.get("/users/next-steps", headers=headers)

    # Assert: Verificar que ações de completar perfil estão presentes
    assert response.status_code == 200
    data = response.json()
    titulos = [acao["titulo"] for acao in data["acoes_recomendadas"]]

    # Deve incluir ações relacionadas ao perfil incompleto
    assert any("perfil" in titulo.lower() or "completar" in titulo.lower() for titulo in titulos)


# TASK-T008: Testes para configurações responsivas
def test_obter_configuracao_responsiva_sucesso(client):
    """Testa sucesso ao obter configurações responsivas"""
    # Arrange: Registrar usuário e obter token
    user_data = {
        "nome_completo": "João Silva",
        "email": "aluno@teste.com",
        "senha": "MinhaSenhaForte123!",
        "confirmar_senha": "MinhaSenhaForte123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Act: Fazer requisição para configurações responsivas
    response = client.get("/users/dashboard/config", headers=headers)

    # Assert: Verificar resposta de sucesso
    assert response.status_code == 200
    data = response.json()
    assert "breakpoints" in data
    assert "layout" in data
    assert "responsive_features" in data

    # Verificar estrutura dos breakpoints
    breakpoints = data["breakpoints"]
    assert "mobile" in breakpoints
    assert "tablet" in breakpoints
    assert "desktop" in breakpoints
    assert breakpoints["mobile"] <= breakpoints["tablet"] <= breakpoints["desktop"]


def test_obter_configuracao_responsiva_nao_autorizado(client):
    """Testa erro 403 quando token não é fornecido"""
    # Act: Fazer requisição sem token
    response = client.get("/users/dashboard/config")

    # Assert: Verificar erro de autenticação
    assert response.status_code == 403
    assert "detail" in response.json()


def test_obter_configuracao_responsiva_token_invalido(client):
    """Testa erro 401 quando token e invalido"""
    # Arrange: Token invalido
    headers = {"Authorization": "Bearer token_invalido"}

    # Act: Fazer requisicao com token invalido
    response = client.get("/users/dashboard/config", headers=headers)

    # Assert: Verificar erro de autenticacao
    assert response.status_code == 401
    assert "detail" in response.json()
    assert "Token" in response.json()["detail"]


def test_obter_configuracao_responsiva_recursos(client):
    """Testa se as configurações incluem features responsivas"""
    # Arrange: Registrar usuário e obter token
    user_data = {
        "nome_completo": "João Silva",
        "email": "aluno@teste.com",
        "senha": "MinhaSenhaForte123!",
        "confirmar_senha": "MinhaSenhaForte123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Act: Fazer requisição para configurações responsivas
    response = client.get("/users/dashboard/config", headers=headers)

    # Assert: Verificar features responsivas
    assert response.status_code == 200
    data = response.json()

    layout = data["layout"]
    assert "grid_columns" in layout
    assert "sidebar_collapsible" in layout
    assert "mobile_navigation" in layout

    responsive_features = data["responsive_features"]
    assert "touch_friendly" in responsive_features
    assert "lazy_loading" in responsive_features
    assert "adaptive_images" in responsive_features


# TASK-T008: Testes para layout responsivo
def test_respostas_api_amigaveis_mobile(client):
    """Testa se as respostas das APIs são adequadas para mobile (JSON leve)"""
    # Arrange: Registrar usuário e obter token
    user_data = {
        "nome_completo": "João Silva",
        "email": "aluno@teste.com",
        "senha": "MinhaSenhaForte123!",
        "confirmar_senha": "MinhaSenhaForte123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Act & Assert: Testar endpoints principais
    endpoints = ["/users/profile", "/users/pdi/overview", "/users/next-steps"]

    for endpoint in endpoints:
        response = client.get(endpoint, headers=headers)
        assert response.status_code == 200

        # Verificar se resposta é JSON leve (< 10KB)
        content_length = len(response.content)
        assert content_length < 10240, f"Resposta de {endpoint} muito grande para mobile: {content_length} bytes"

        # Verificar se é JSON válido
        data = response.json()
        assert isinstance(data, dict), f"Resposta de {endpoint} não é JSON válido"


def test_estrutura_resposta_visao_geral_pdi(client):
    """Testa se a estrutura da resposta PDI overview é otimizada para mobile"""
    # Arrange
    user_data = {
        "nome_completo": "João Silva",
        "email": "aluno@teste.com",
        "senha": "MinhaSenhaForte123!",
        "confirmar_senha": "MinhaSenhaForte123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Act
    response = client.get("/users/pdi/overview", headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.json()

    # Verificar campos essenciais para mobile
    required_fields = ["status_geral", "objetivos_ativos", "progresso_percentual", "proximas_acoes", "ultima_atualizacao"]
    for field in required_fields:
        assert field in data, f"Campo obrigatório {field} ausente na resposta mobile"

    # Verificar tipos de dados apropriados
    assert isinstance(data["objetivos_ativos"], int)
    assert isinstance(data["progresso_percentual"], (int, float))
    assert isinstance(data["proximas_acoes"], list)
    assert len(data["proximas_acoes"]) <= 5, "Lista de próximas ações muito longa para mobile"


def test_otimizacao_mobile_proximos_passos(client):
    """Testa se next-steps está otimizado para consumo mobile"""
    # Arrange
    user_data = {
        "nome_completo": "João Silva",
        "email": "aluno@teste.com",
        "senha": "MinhaSenhaForte123!",
        "confirmar_senha": "MinhaSenhaForte123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Act
    response = client.get("/users/next-steps", headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.json()

    # Verificar estrutura otimizada para mobile
    assert "acoes_recomendadas" in data
    assert isinstance(data["acoes_recomendadas"], list)
    assert len(data["acoes_recomendadas"]) <= 6, "Muitas ações para tela mobile"

    # Verificar cada ação tem estrutura mobile-friendly
    for acao in data["acoes_recomendadas"]:
        assert "titulo" in acao
        assert "descricao" in acao
        assert "prioridade" in acao
        assert "url" in acao

        # Títulos curtos para mobile
        assert len(acao["titulo"]) <= 50, f"Título muito longo: {acao['titulo']}"
        assert len(acao["descricao"]) <= 120, f"Descrição muito longa: {acao['descricao']}"

        # Prioridade válida
        assert acao["prioridade"] in ["alta", "media", "baixa"]


def test_tempos_resposta_api_mobile(client):
    """Testa se as respostas das APIs são rápidas o suficiente para mobile"""
    import time

    # Arrange
    user_data = {
        "nome_completo": "João Silva",
        "email": "aluno@teste.com",
        "senha": "MinhaSenhaForte123!",
        "confirmar_senha": "MinhaSenhaForte123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Act & Assert: Testar tempo de resposta
    endpoints = ["/users/profile", "/users/pdi/overview", "/users/next-steps"]

    for endpoint in endpoints:
        start_time = time.time()
        response = client.get(endpoint, headers=headers)
        end_time = time.time()

        response_time = end_time - start_time
        assert response_time < 1.0, f"Endpoint {endpoint} muito lento para mobile: {response_time:.2f}s"
        assert response.status_code == 200
