# TASK-T004: Recuperação de Senha Confiável
def test_solicitacao_reset_senha_sucesso(client, sample_user_data):
    """Testa solicitação de reset de senha bem-sucedida"""
    # Arrange - Registrar usuário primeiro
    import uuid
    unique_email = f"reset-{uuid.uuid4()}@email.com"
    user_data = sample_user_data.copy()
    user_data["email"] = unique_email

    # Registrar usuário
    register_response = client.post("/register", json=user_data)
    assert register_response.status_code == 200

    # Act - Solicitar reset de senha
    reset_data = {"email": unique_email}
    response = client.post("/reset-password", json=reset_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "token" in data  # Token para reset
    assert "expiracao" in data

def test_solicitacao_reset_senha_email_invalido(client):
    """Testa solicitação de reset com email não cadastrado"""
    # Arrange
    reset_data = {"email": "naoexiste@email.com"}

    # Act
    response = client.post("/reset-password", json=reset_data)

    # Assert
    assert response.status_code == 404
    assert "Usuario nao encontrado" in response.json()["detail"]

def test_confirmacao_reset_senha_sucesso(client, sample_user_data):
    """Testa confirmação de reset de senha bem-sucedida"""
    # Arrange - Registrar usuário e solicitar reset
    import uuid
    unique_email = f"resetconfirm-{uuid.uuid4()}@email.com"
    user_data = sample_user_data.copy()
    user_data["email"] = unique_email

    # Registrar usuário
    register_response = client.post("/register", json=user_data)
    assert register_response.status_code == 200

    # Solicitar reset
    reset_data = {"email": unique_email}
    reset_response = client.post("/reset-password", json=reset_data)
    assert reset_response.status_code == 200
    reset_token = reset_response.json()["token"]

    # Act - Confirmar reset com nova senha
    confirm_data = {
        "token": reset_token,
        "nova_senha": "NovaSenha456!",
        "confirmar_senha": "NovaSenha456!"
    }
    response = client.post("/confirm-reset-password", json=confirm_data)

    # Assert
    assert response.status_code == 200
    assert "Senha alterada com sucesso" in response.json()["message"]

def test_confirmacao_reset_senha_token_invalido(client):
    """Testa confirmação de reset com token inválido"""
    # Arrange
    confirm_data = {
        "token": "token-invalido-123",
        "nova_senha": "NovaSenha456!",
        "confirmar_senha": "NovaSenha456!"
    }

    # Act
    response = client.post("/confirm-reset-password", json=confirm_data)

    # Assert
    assert response.status_code == 400
    assert "Token invalido" in response.json()["detail"]

def test_confirmacao_reset_senha_token_expirado(client, sample_user_data):
    """Testa confirmação de reset com token expirado"""
    # Arrange - Simular token expirado diretamente no banco
    from src.backend.main import tokens_reset_senha
    import uuid
    from datetime import datetime, timedelta, timezone

    expired_token = str(uuid.uuid4())
    tokens_reset_senha[expired_token] = {
        "user_id": str(uuid.uuid4()),
        "expiracao": datetime.now(timezone.utc) - timedelta(hours=1)  # Expirado
    }

    confirm_data = {
        "token": expired_token,
        "nova_senha": "NovaSenha456!",
        "confirmar_senha": "NovaSenha456!"
    }

    # Act
    response = client.post("/confirm-reset-password", json=confirm_data)

    # Assert
    assert response.status_code == 400
    assert "Token expirado" in response.json()["detail"]