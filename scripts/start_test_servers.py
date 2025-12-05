#!/usr/bin/env python3
"""
Script para iniciar servidores de teste do Portal do Aluno MVP

Este script configura e inicia tanto o backend (FastAPI) quanto o frontend (Next.js)
para testes de usuário do Portal do Aluno.

Uso:
    python scripts/start_test_servers.py

Requisitos:
    - Python 3.8+
    - Node.js 18+
    - Dependências instaladas (pip install -r requirements.txt && npm install)
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

# Configurações
BACKEND_PORT = 8000
FRONTEND_PORT = 3000
PROJECT_ROOT = Path(__file__).parent.parent

class TestServerManager:
    """Gerenciador dos servidores de teste"""

    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = False

    def start_backend(self):
        """Inicia o servidor FastAPI"""
        print("🚀 Iniciando servidor backend (FastAPI)...")

        # Mudar para diretório do backend
        backend_dir = PROJECT_ROOT / "src" / "backend"
        os.chdir(backend_dir)

        # Comando para iniciar o servidor
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "127.0.0.1",
            "--port", str(BACKEND_PORT),
            "--reload"
        ]

        try:
            self.backend_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ Backend iniciado em http://localhost:{BACKEND_PORT}")
            print(f"📚 Documentação API: http://localhost:{BACKEND_PORT}/docs")
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar backend: {e}")
            return False

    def start_frontend(self):
        """Inicia o servidor Next.js"""
        print("🎨 Iniciando servidor frontend (Next.js)...")

        # Mudar para diretório do frontend
        frontend_dir = PROJECT_ROOT / "src" / "frontend"
        os.chdir(frontend_dir)

        # Verificar se node_modules existe
        if not (frontend_dir / "node_modules").exists():
            print("📦 Instalando dependências do frontend...")
            install_result = subprocess.run(
                ["npm", "install"],
                capture_output=True,
                text=True
            )
            if install_result.returncode != 0:
                print(f"❌ Erro ao instalar dependências: {install_result.stderr}")
                return False

        # Comando para iniciar o servidor
        cmd = ["npm", "run", "dev"]

        try:
            self.frontend_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env={**os.environ, "PORT": str(FRONTEND_PORT)}
            )
            print(f"✅ Frontend iniciado em http://localhost:{FRONTEND_PORT}")
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar frontend: {e}")
            return False

    def wait_for_servers(self):
        """Aguarda os servidores ficarem prontos"""
        print("⏳ Aguardando servidores ficarem prontos...")

        # Aguardar um pouco para os servidores inicializarem
        time.sleep(5)

        # Verificar se os processos ainda estão rodando
        if self.backend_process and self.backend_process.poll() is None:
            print("✅ Backend está rodando")
        else:
            print("❌ Backend não está respondendo")

        if self.frontend_process and self.frontend_process.poll() is None:
            print("✅ Frontend está rodando")
        else:
            print("❌ Frontend não está respondendo")

    def stop_servers(self):
        """Para os servidores"""
        print("🛑 Parando servidores...")

        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
                print("✅ Backend parado")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("⚠️ Backend forçado a parar")

        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend parado")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("⚠️ Frontend forçado a parar")

    def run_tests(self):
        """Executa testes automatizados"""
        print("🧪 Executando testes automatizados...")

        os.chdir(PROJECT_ROOT)

        # Executar testes do backend
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/test_profile.py",
            "-v",
            "--tb=short"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Todos os testes passaram!")
            return True
        else:
            print("❌ Alguns testes falharam:")
            print(result.stdout)
            print(result.stderr)
            return False

    def show_info(self):
        """Exibe informações sobre o ambiente de teste"""
        print("\n" + "="*60)
        print("🎯 AMBIENTE DE TESTE PRONTO!")
        print("="*60)
        print(f"🌐 Frontend: http://localhost:{FRONTEND_PORT}")
        print(f"🔧 Backend:  http://localhost:{BACKEND_PORT}")
        print(f"📚 API Docs: http://localhost:{BACKEND_PORT}/docs")
        print("\n📋 Funcionalidades disponíveis para teste:")
        print("   • Cadastro de usuário")
        print("   • Login seguro")
        print("   • Dashboard PDI responsivo")
        print("   • Perfil do usuário")
        print("   • Próximos passos interativos")
        print("\n🔑 Usuários de teste:")
        print("   Email: aluno@teste.com")
        print("   Senha: MinhaSenhaForte123!")
        print("\n⚠️  Pressione Ctrl+C para parar os servidores")
        print("="*60 + "\n")

def main():
    """Função principal"""
    print("🧪 Iniciando ambiente de teste do Portal do Aluno MVP")
    print("="*60)

    manager = TestServerManager()

    def signal_handler(signum, frame):
        """Tratador de sinal para parada graceful"""
        print("\n🛑 Recebido sinal de interrupção...")
        manager.stop_servers()
        sys.exit(0)

    # Registrar tratador de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Executar testes automatizados primeiro
        if not manager.run_tests():
            print("❌ Testes automatizados falharam. Abortando inicialização.")
            sys.exit(1)

        # Iniciar servidores
        backend_ok = manager.start_backend()
        if not backend_ok:
            print("❌ Falha ao iniciar backend. Abortando.")
            sys.exit(1)

        frontend_ok = manager.start_frontend()
        if not frontend_ok:
            print("❌ Falha ao iniciar frontend. Abortando.")
            manager.stop_servers()
            sys.exit(1)

        # Aguardar inicialização
        manager.wait_for_servers()

        # Mostrar informações
        manager.show_info()

        # Manter rodando
        print("🔄 Servidores rodando... Pressione Ctrl+C para parar.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Interrupção recebida pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        manager.stop_servers()
        print("👋 Ambiente de teste finalizado.")

if __name__ == "__main__":
    main()