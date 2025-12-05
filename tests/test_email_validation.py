import pytest
from datetime import datetime, timedelta, timezone

# TASK-T002: Validação de Email
def test_validacao_email_criacao_token():
    """Testa criação de token de validação"""
    # Arrange & Act
    from src.backend.main import criar_token_validacao
    token = criar_token_validacao()

    # Assert
    assert token is not None
    assert len(token) == 36  # UUID v4 tem 36 caracteres
    assert token.count('-') == 4  # UUID tem 4 hífens

def test_validacao_email_expiracao_token():
    """Testa expiração do token após 24h"""
    # Arrange
    from src.backend.main import validar_token_email, tokens_validacao, usuarios_db
    import uuid
    from datetime import datetime, timedelta, timezone

    # Criar um token que expira imediatamente
    token = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # Simular token expirado (expirou há 1 hora)
    tokens_validacao[token] = {
        "user_id": user_id,
        "expiracao": datetime.now(timezone.utc) - timedelta(hours=1)
    }

    # Act
    result = validar_token_email(token)

    # Assert
    assert result == False
    # Token deve ter sido removido após validação
    assert token not in tokens_validacao

def test_validacao_email_sucesso(client):
    """Testa validação bem-sucedida de email"""
    # Arrange - Registrar usuário com email único
    import uuid
    unique_email = f"test-{uuid.uuid4()}@email.com"
    user_data = {
        "nome_completo": "João Silva",
        "email": unique_email,
        "senha": "Senha123!",
        "confirmar_senha": "Senha123!",
        "aceitar_termos": True
    }

    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    user_data_response = response.json()
    token = user_data_response["token_validacao"]

    # Act - Validar email
    response = client.post("/validate-email", json={"token": token})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Email validado com sucesso"
    assert data["email_validado"] == True

def test_validacao_email_token_invalido(client):
    """Testa validação com token inválido"""
    # Arrange
    invalid_token = "token-invalido-123"

    # Act
    response = client.post("/validate-email", json={"token": invalid_token})

    # Assert
    assert response.status_code == 400
    assert "Token invalido ou expirado" in response.json()["detail"]