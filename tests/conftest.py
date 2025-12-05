import pytest
from fastapi.testclient import TestClient

# TASK-T001: Configuração de testes
@pytest.fixture
def client():
    """Cliente de teste para FastAPI"""
    from src.backend.main import app
    return TestClient(app)

@pytest.fixture
def sample_user_data():
    """Dados de usuário de exemplo para testes"""
    return {
        "nome_completo": "João Silva",
        "email": "joao@email.com",
        "senha": "Senha123!",
        "confirmar_senha": "Senha123!",
        "aceitar_termos": True
    }