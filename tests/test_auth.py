# TASK-T001: Formulário de Cadastro
def test_cadastro_usuario_dados_validos(client, sample_user_data):
    """Testa cadastro com dados válidos"""
    # Arrange
    # Act
    response = client.post("/register", json=sample_user_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == sample_user_data["email"]
    assert data["nome_completo"] == sample_user_data["nome_completo"]
    assert data["email_validado"] == False
    assert "token_validacao" in data
    assert "data_cadastro" in data

def test_cadastro_usuario_email_duplicado(client, sample_user_data):
    """Testa erro ao cadastrar email duplicado"""
    # Arrange
    client.post("/register", json=sample_user_data)  # Primeiro cadastro

    # Act
    response = client.post("/register", json=sample_user_data)  # Segundo cadastro

    # Assert
    assert response.status_code == 400
    assert "Email ja cadastrado" in response.json()["detail"]

def test_cadastro_usuario_email_invalido(client):
    """Testa erro com email inválido"""
    # Arrange
    invalid_data = {
        "nome_completo": "João Silva",
        "email": "email-invalido",
        "senha": "Senha123!",
        "confirmar_senha": "Senha123!",
        "aceitar_termos": True
    }

    # Act
    response = client.post("/register", json=invalid_data)

    # Assert
    assert response.status_code == 422  # Validation error

def test_cadastro_usuario_senha_fraca(client):
    """Testa erro com senha fraca"""
    # Arrange
    weak_password_data = {
        "nome_completo": "João Silva",
        "email": "joao@email.com",
        "senha": "123",  # Senha fraca
        "confirmar_senha": "123",
        "aceitar_termos": True
    }

    # Act
    response = client.post("/register", json=weak_password_data)

    # Assert
    assert response.status_code == 422  # Validation error