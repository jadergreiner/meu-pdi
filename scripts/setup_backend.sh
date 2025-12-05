#!/bin/bash

# Script de inicialização do backend FastAPI - Meu PDI
# Este script configura o ambiente de desenvolvimento completo

set -e  # Parar execução em caso de erro

echo "🚀 Inicializando setup do backend FastAPI - Meu PDI"
echo "=================================================="

# Verificar se estamos no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: Execute este script da raiz do projeto (onde está requirements.txt)"
    exit 1
fi

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está disponível
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não está disponível."
    exit 1
fi

echo "📦 Instalando dependências Python..."
pip install -r requirements.txt

echo "🐳 Iniciando serviços Docker (PostgreSQL + Redis)..."
if command -v docker-compose &> /dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo "⏳ Aguardando PostgreSQL ficar pronto..."
sleep 10

# Verificar se PostgreSQL está respondendo
echo "🔍 Verificando conexão com PostgreSQL..."
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        dbname='meu_pdi_dev',
        user='meu_pdi_user',
        password='meu_pdi_password',
        host='localhost',
        port='5432'
    )
    conn.close()
    print('✅ PostgreSQL conectado com sucesso!')
except Exception as e:
    print(f'❌ Erro ao conectar com PostgreSQL: {e}')
    exit(1)
"

echo "🗄️ Executando migrations do banco de dados..."
cd src/backend
python -m alembic upgrade head

echo "✅ Setup concluído com sucesso!"
echo ""
echo "🎯 Para iniciar o servidor FastAPI:"
echo "   cd src/backend"
echo "   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "📖 Documentação da API: http://localhost:8000/docs"
echo "🔍 Health check: http://localhost:8000/health"
echo ""
echo "🐳 Serviços Docker em execução:"
echo "   PostgreSQL: localhost:5432"
echo "   Redis: localhost:6379"
echo ""
echo "🛑 Para parar os serviços Docker:"
if command -v docker-compose &> /dev/null; then
    echo "   docker-compose down"
else
    echo "   docker compose down"
fi