# TASK-T012: Test Authentication Endpoints
import pytest
from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)

def test_register_endpoint():
    """Testa endpoint de registro de usuários"""
    user_data = {
        "nome_completo": "Teste Usuario",
        "email": "teste_register@email.com",
        "senha": "Teste123!",
        "confirmar_senha": "Teste123!",
        "aceitar_termos": True
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert "token_validacao" in data
    assert data["email"] == user_data["email"]
    assert data["nome_completo"] == user_data["nome_completo"]
    assert data["email_validado"] == False

def test_register_duplicate_email():
    """Testa erro ao registrar email duplicado"""
    user_data = {
        "nome_completo": "Teste Usuario",
        "email": "teste_duplicate@email.com",
        "senha": "Teste123!",
        "confirmar_senha": "Teste123!",
        "aceitar_termos": True
    }

    # Primeiro registro
    client.post("/auth/register", json=user_data)

    # Segundo registro com mesmo email
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Email já cadastrado" in response.json()["detail"]

def test_login_endpoint():
    """Testa endpoint de login"""
    # Registrar usuário
    user_data = {
        "nome_completo": "Teste Usuario",
        "email": "teste_login@email.com",
        "senha": "Teste123!",
        "confirmar_senha": "Teste123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    # Fazer login
    login_data = {"email": "teste_login@email.com", "senha": "Teste123!"}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert "user" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    """Testa login com credenciais inválidas"""
    login_data = {"email": "naoexiste@email.com", "senha": "SenhaErrada123!"}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Email ou senha inválidos" in response.json()["detail"]

def test_refresh_token_endpoint():
    """Testa endpoint de refresh token"""
    # Registrar e fazer login
    user_data = {
        "nome_completo": "Teste Usuario",
        "email": "teste_refresh@email.com",
        "senha": "Teste123!",
        "confirmar_senha": "Teste123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    login_data = {"email": "teste_refresh@email.com", "senha": "Teste123!"}
    login_response = client.post("/auth/login", json=login_data)
    refresh_token = login_response.json()["refresh_token"]

    # Testar refresh
    refresh_data = {"refresh_token": refresh_token}
    response = client.post("/auth/refresh", json=refresh_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data

def test_validate_email_endpoint():
    """Testa endpoint de validação de email"""
    # Registrar usuário
    user_data = {
        "nome_completo": "Teste Usuario",
        "email": "teste_validate@email.com",
        "senha": "Teste123!",
        "confirmar_senha": "Teste123!",
        "aceitar_termos": True
    }
    register_response = client.post("/auth/register", json=user_data)
    token_validacao = register_response.json()["token_validacao"]

    # Validar email
    validation_data = {"token": token_validacao}
    response = client.post("/auth/validate-email", json=validation_data)
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "Email validado com sucesso" in data["message"]

def test_validate_email_invalid_token():
    """Testa validação com token inválido"""
    validation_data = {"token": "token-invalido-123"}
    response = client.post("/auth/validate-email", json=validation_data)
    assert response.status_code == 400
    assert "Token inválido" in response.json()["detail"]

def test_reset_password_request():
    """Testa solicitação de reset de senha"""
    # Registrar usuário
    user_data = {
        "nome_completo": "Teste Usuario",
        "email": "teste_reset@email.com",
        "senha": "Teste123!",
        "confirmar_senha": "Teste123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    # Solicitar reset
    reset_data = {"email": "teste_reset@email.com"}
    response = client.post("/auth/reset-password", json=reset_data)
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "token" in data
    assert "expiracao" in data
    assert "Email de reset enviado com sucesso" in data["message"]

def test_reset_password_invalid_email():
    """Testa reset com email não cadastrado"""
    reset_data = {"email": "naoexiste@email.com"}
    response = client.post("/auth/reset-password", json=reset_data)
    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]

def test_confirm_reset_password():
    """Testa confirmação de reset de senha"""
    # Registrar usuário
    user_data = {
        "nome_completo": "Teste Usuario",
        "email": "teste_confirm_reset@email.com",
        "senha": "Teste123!",
        "confirmar_senha": "Teste123!",
        "aceitar_termos": True
    }
    client.post("/auth/register", json=user_data)

    # Solicitar reset
    reset_data = {"email": "teste_confirm_reset@email.com"}
    reset_response = client.post("/auth/reset-password", json=reset_data)
    reset_token = reset_response.json()["token"]

    # Confirmar reset
    confirm_data = {
        "token": reset_token,
        "nova_senha": "NovaSenha123!",
        "confirmar_senha": "NovaSenha123!"
    }
    response = client.post("/auth/confirm-reset-password", json=confirm_data)
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "Senha alterada com sucesso" in data["message"]

def test_confirm_reset_invalid_token():
    """Testa confirmação de reset com token inválido"""
    confirm_data = {
        "token": "token-invalido-123",
        "nova_senha": "NovaSenha123!",
        "confirmar_senha": "NovaSenha123!"
    }
    response = client.post("/auth/confirm-reset-password", json=confirm_data)
def test_confirm_reset_invalid_token():
    """Testa confirmação de reset com token inválido"""
    confirm_data = {
        "token": "token-invalido-123",
        "nova_senha": "NovaSenha123!",
        "confirmar_senha": "NovaSenha123!"
    }
    response = client.post("/auth/confirm-reset-password", json=confirm_data)
    assert response.status_code == 400
    assert "Token inválido" in response.json()["detail"]