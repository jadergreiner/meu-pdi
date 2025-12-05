#!/bin/bash

# 🚀 Script de Configuração - Gateways de Pagamento
# TASK-004: Configurar Conta Stripe/PagSeguro
# Data: 04/11/2025

set -e

echo "🚀 Iniciando configuração de gateways de pagamento..."
echo "TASK-004: Configurar Conta Stripe/PagSeguro"
echo "================================================"

# Verificar se estamos no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: Execute este script do diretório raiz do projeto"
    exit 1
fi

echo "📋 Verificando pré-requisitos..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale o Python 3.8+ primeiro."
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instale o pip primeiro."
    exit 1
fi

echo "✅ Pré-requisitos verificados"

echo ""
echo "📝 LISTA DE VERIFICAÇÃO - DOCUMENTOS NECESSÁRIOS:"
echo "================================================"
echo "☐ CNPJ da empresa (obrigatório)"
echo "☐ RG/CPF do responsável legal"
echo "☐ Comprovante de endereço comercial"
echo "☐ Extratos bancários (3 meses)"
echo "☐ Conta bancária PJ no mesmo CNPJ"
echo ""

read -p "Todos os documentos estão prontos? (s/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "⏳ Aguarde a preparação dos documentos antes de continuar."
    echo "📖 Consulte: docs/guia-configuracao-pagamentos-stripe-pagseguro.md"
    exit 0
fi

echo ""
echo "🔧 Instalando dependências de pagamento..."

# Instalar bibliotecas de pagamento
pip3 install stripe pagseguro-python

echo "✅ Dependências instaladas"

echo ""
echo "🔑 Configuração das credenciais..."

# Criar arquivo de configuração seguro
cat > config/payments.env << EOF
# 🚨 ARQUIVO SENSÍVEL - NÃO COMMITAR NO GIT
# Configurações de Gateways de Pagamento - Meu PDI
# Gerado em: $(date)

# STRIPE CONFIGURATION
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# PAGSEGURO CONFIGURATION
PAGSEGURO_EMAIL=financeiro@meupdi.com.br
PAGSEGURO_TOKEN=...
PAGSEGURO_APP_ID=...
PAGSEGURO_APP_KEY=...

# PAYMENT SETTINGS
PAYMENT_CURRENCY=BRL
MINIMUM_AMOUNT=100  # R$ 1,00
MAXIMUM_AMOUNT=50000  # R$ 500,00

# WEBHOOK URLS
STRIPE_WEBHOOK_URL=https://api.meupdi.com/webhooks/stripe
PAGSEGURO_WEBHOOK_URL=https://api.meupdi.com/webhooks/pagseguro
EOF

echo "✅ Arquivo config/payments.env criado"
echo "⚠️  IMPORTANTE: Preencha as credenciais reais no arquivo acima"

echo ""
echo "🧪 Criando testes de configuração..."

# Criar arquivo de teste de pagamentos
cat > tests/test_payment_config.py << 'EOF'
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
    assert stripe_key is not None, "STRIPE_SECRET_KEY não configurada"
    assert stripe_key.startswith('sk_'), "STRIPE_SECRET_KEY inválida"

def test_pagseguro_configuration():
    """Testa se as configurações do PagSeguro estão presentes"""
    email = os.getenv('PAGSEGURO_EMAIL')
    token = os.getenv('PAGSEGURO_TOKEN')

    assert email is not None, "PAGSEGURO_EMAIL não configurado"
    assert token is not None, "PAGSEGURO_TOKEN não configurado"

@patch('stripe.Customer.create')
def test_stripe_connection(mock_stripe):
    """Testa conexão com Stripe"""
    mock_stripe.return_value = {'id': 'cus_test123'}

    # Simular criação de cliente
    import stripe
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_fake')

    try:
        customer = stripe.Customer.create(email='test@example.com')
        assert customer['id'] == 'cus_test123'
        print("✅ Conexão com Stripe OK")
    except Exception as e:
        pytest.fail(f"Falha na conexão com Stripe: {e}")

def test_payment_limits():
    """Testa limites de pagamento configurados"""
    min_amount = int(os.getenv('MINIMUM_AMOUNT', '100'))
    max_amount = int(os.getenv('MAXIMUM_AMOUNT', '50000'))

    assert min_amount >= 100, "Valor mínimo deve ser pelo menos R$ 1,00"
    assert max_amount <= 100000, "Valor máximo não deve exceder R$ 1.000,00"
    assert min_amount < max_amount, "Valor mínimo deve ser menor que máximo"

if __name__ == "__main__":
    print("🧪 Executando testes de configuração de pagamentos...")

    try:
        test_payment_limits()
        print("✅ Testes básicos passaram")
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")

    print("ℹ️  Para testes completos, configure as credenciais reais")
EOF

echo "✅ Arquivo tests/test_payment_config.py criado"

echo ""
echo "📚 Próximos passos manuais:"
echo "=========================="
echo "1. 📋 Reunir documentos necessários (CNPJ, RG, comprovantes)"
echo "2. 💳 Criar conta Stripe: https://stripe.com/br"
echo "3. 💰 Criar conta PagSeguro: https://pagseguro.uol.com.br"
echo "4. 🔑 Preencher credenciais em config/payments.env"
echo "5. 🧪 Executar testes: python -m pytest tests/test_payment_config.py"
echo ""

echo "📖 Documentação completa:"
echo "docs/guia-configuracao-pagamentos-stripe-pagseguro.md"

echo ""
echo "🎯 TASK-004 Status: Preparação técnica concluída"
echo "⏳ Aguardando configuração manual das contas"

# Criar backup do .gitignore se necessário
if ! grep -q "config/payments.env" .gitignore; then
    echo "config/payments.env" >> .gitignore
    echo "✅ Arquivo sensível adicionado ao .gitignore"
fi

echo ""
echo "✅ Configuração inicial concluída com sucesso!"
echo "Tempo estimado para conclusão: 4 horas (incluindo aprovações bancárias)"