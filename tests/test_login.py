# TASK-T003: Login Seguro e Intuitivo
def test_login_usuario_sucesso(client, sample_user_data):
    """Testa login bem-sucedido com credenciais válidas"""
    # Arrange - Registrar usuário primeiro
    import uuid
    unique_email = f"login-{uuid.uuid4()}@email.com"
    user_data = sample_user_data.copy()
    user_data["email"] = unique_email

    # Registrar usuário
    register_response = client.post("/register", json=user_data)
    assert register_response.status_code == 200

    # Act - Fazer login
    login_data = {
        "email": unique_email,
        "senha": "Senha123!"
    }
    response = client.post("/login", json=login_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == unique_email

def test_login_usuario_email_invalido(client):
    """Testa login com email não cadastrado"""
    # Arrange
    login_data = {
        "email": "naoexiste@email.com",
        "senha": "Senha123!"
    }

    # Act
    response = client.post("/login", json=login_data)

    # Assert
    assert response.status_code == 401
    assert "Email ou senha invalidos" in response.json()["detail"]

def test_login_usuario_senha_incorreta(client, sample_user_data):
    """Testa login com senha incorreta"""
    # Arrange - Registrar usuário primeiro
    import uuid
    unique_email = f"wrongpass-{uuid.uuid4()}@email.com"
    user_data = sample_user_data.copy()
    user_data["email"] = unique_email

    # Registrar usuário
    register_response = client.post("/register", json=user_data)
    assert register_response.status_code == 200

    # Act - Tentar login com senha errada
    login_data = {
        "email": unique_email,
        "senha": "SenhaErrada456!"
    }
    response = client.post("/login", json=login_data)

    # Assert
    assert response.status_code == 401
    assert "Email ou senha invalidos" in response.json()["detail"]

def test_login_usuario_email_nao_validado(client, sample_user_data):
    """Testa login com email não validado (deve permitir login mas indicar status)"""
    # Arrange - Registrar usuário mas não validar email
    import uuid
    unique_email = f"unverified-{uuid.uuid4()}@email.com"
    user_data = sample_user_data.copy()
    user_data["email"] = unique_email

    # Registrar usuário
    register_response = client.post("/register", json=user_data)
    assert register_response.status_code == 200

    # Act - Fazer login
    login_data = {
        "email": unique_email,
        "senha": "Senha123!"
    }
    response = client.post("/login", json=login_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email_validado"] == False
    # Deve permitir login mesmo com email não validado