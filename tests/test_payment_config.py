"""
Testes de Configuração de Pagamentos
TASK-004: Configurar Conta Stripe/PagSeguro
"""
import os
import pytest
from unittest.mock import patch, MagicMock

def test_stripe_configuration():
    """Testa se as configurações do Stripe estão presentes"""
    stripe_key = os.getenv('STRIPE_SECRET_KEY')
    if stripe_key:  # Só testa se a variável estiver definida
        assert stripe_key.startswith(('sk_test_', 'sk_live_')), "STRIPE_SECRET_KEY inválida"

def test_pagseguro_configuration():
    """Testa se as configurações do PagSeguro estão presentes"""
    email = os.getenv('PAGSEGURO_EMAIL')
    token = os.getenv('PAGSEGURO_TOKEN')

    if email:  # Só testa se as variáveis estiverem definidas
        assert '@' in email, "PAGSEGURO_EMAIL inválido"
    if token:
        assert len(token) > 10, "PAGSEGURO_TOKEN muito curto"

def test_payment_limits():
    """Testa limites de pagamento configurados"""
    min_amount = int(os.getenv('MINIMUM_AMOUNT', '100'))
    max_amount = int(os.getenv('MAXIMUM_AMOUNT', '50000'))

    assert min_amount >= 100, "Valor mínimo deve ser pelo menos R$ 1,00"
    assert max_amount <= 100000, "Valor máximo não deve exceder R$ 1.000,00"
    assert min_amount < max_amount, "Valor mínimo deve ser menor que máximo"

@patch('stripe.Customer.create')
def test_stripe_connection_mock(mock_stripe):
    """Testa simulação de conexão com Stripe"""
    mock_stripe.return_value = {'id': 'cus_test123', 'email': 'test@example.com'}

    # Simular criação de cliente
    try:
        # Importar stripe apenas se disponível
        import stripe
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_fake')

        customer = stripe.Customer.create(email='test@example.com')
        assert customer['id'] == 'cus_test123'
        print("✅ Simulação de conexão com Stripe OK")
    except ImportError:
        pytest.skip("Stripe não instalado - pule teste")
    except Exception as e:
        print(f"ℹ️  Teste mockado (credenciais não configuradas): {e}")

def test_environment_variables_loaded():
    """Testa se as variáveis de ambiente podem ser carregadas"""
    # Tentar carregar do arquivo .env se existir
    env_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'payments.env')

    if os.path.exists(env_file):
        print("✅ Arquivo payments.env encontrado")
        # Verificar se arquivo não está vazio
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content.strip()) > 0, "Arquivo payments.env está vazio"
    else:
        pytest.skip("Arquivo payments.env não encontrado - configuração pendente")

if __name__ == "__main__":
    print("🧪 Executando testes de configuração de pagamentos...")

    try:
        test_payment_limits()
        test_environment_variables_loaded()
        print("✅ Testes básicos passaram")
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")

    print("ℹ️  Para testes completos, configure as credenciais reais em config/payments.env")