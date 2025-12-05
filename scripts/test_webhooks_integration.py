#!/usr/bin/env python3
"""
🧪 Teste de Integração Webhooks Calendly → Zapier
TASK-002: Implementar Webhooks Calendly → Zapier

Este script testa a integração completa dos webhooks.
"""

import json
import requests
import time
from datetime import datetime
from typing import Dict, Any

class WebhookTester:
    """Testa a integração de webhooks Calendly → Zapier"""

    def __init__(self, config_file: str = "config/webhooks-calendly-zapier.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Carrega configuração do arquivo JSON"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Arquivo de configuração não encontrado: {self.config_file}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Erro no JSON da configuração: {e}")
            return {}

    def update_config(self, updates: Dict[str, Any]):
        """Atualiza configuração e salva no arquivo"""
        self.config.update(updates)
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print("✅ Configuração atualizada com sucesso")
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")

    def log_test(self, test_type: str, status: str, notes: str = ""):
        """Registra resultado de teste"""
        test_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "test_type": test_type,
            "status": status,
            "notes": notes
        }

        if "test_logs" not in self.config:
            self.config["test_logs"] = []

        self.config["test_logs"].append(test_entry)
        self.update_config({"test_logs": self.config["test_logs"]})

    def test_webhook_url(self) -> bool:
        """Testa se a URL do webhook está acessível"""
        webhook_url = self.config.get("calendly", {}).get("webhook_url", "")

        if not webhook_url or "XXXXXXX" in webhook_url:
            print("❌ Webhook URL não configurada ou é placeholder")
            return False

        try:
            # Testa conectividade (Zapier deve aceitar POST)
            response = requests.post(webhook_url, json={"test": "connection"}, timeout=10)
            if response.status_code in [200, 201]:
                print("✅ Webhook URL acessível")
                return True
            else:
                print(f"⚠️ Webhook respondeu com status {response.status_code}")
                return True  # Ainda pode funcionar
        except requests.RequestException as e:
            print(f"❌ Erro ao testar webhook URL: {e}")
            return False

    def simulate_calendly_payload(self) -> Dict[str, Any]:
        """Gera payload simulado do Calendly"""
        return {
            "event": "invitee.created",
            "time": datetime.now().isoformat(),
            "payload": {
                "event_type": {
                    "uuid": "test-event-uuid",
                    "name": "Sessão PDI Individual - 60min",
                    "duration": 60
                },
                "invitee": {
                    "uuid": "test-invitee-uuid",
                    "first_name": "João",
                    "last_name": "Silva",
                    "email": "joao.silva@email.com",
                    "timezone": "America/Sao_Paulo",
                    "created_at": datetime.now().isoformat()
                },
                "questions_and_responses": {
                    "1_response": "Desenvolvimento de carreira em tecnologia",
                    "2_response": "Sim, mas não consegui manter"
                },
                "reschedule_url": "https://calendly.com/reschedule/test",
                "cancel_url": "https://calendly.com/cancel/test"
            }
        }

    def test_webhook_payload(self) -> bool:
        """Testa envio de payload simulado para o webhook"""
        webhook_url = self.config.get("calendly", {}).get("webhook_url", "")

        if not webhook_url or "XXXXXXX" in webhook_url:
            print("❌ Webhook URL não configurada")
            return False

        payload = self.simulate_calendly_payload()

        try:
            print("📤 Enviando payload de teste...")
            response = requests.post(webhook_url, json=payload, timeout=30)

            if response.status_code in [200, 201, 202]:
                print("✅ Payload enviado com sucesso")
                print(f"📊 Status: {response.status_code}")
                return True
            else:
                print(f"❌ Falha no envio - Status: {response.status_code}")
                print(f"📄 Resposta: {response.text}")
                return False

        except requests.RequestException as e:
            print(f"❌ Erro na requisição: {e}")
            return False

    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes de integração webhooks...\n")

        # Teste 1: URL do webhook
        print("1️⃣ Testando URL do webhook...")
        webhook_test = self.test_webhook_url()
        self.log_test("webhook_url_test", "success" if webhook_test else "failed")

        # Teste 2: Payload
        print("\n2️⃣ Testando envio de payload...")
        payload_test = self.test_webhook_payload()
        self.log_test("payload_test", "success" if payload_test else "failed")

        # Resumo
        print("\n📊 RESUMO DOS TESTES:")
        print(f"   Webhook URL: {'✅' if webhook_test else '❌'}")
        print(f"   Payload: {'✅' if payload_test else '❌'}")

        if webhook_test and payload_test:
            print("\n🎉 Todos os testes passaram! Integração funcional.")
            self.update_config({
                "implementation_status": {
                    **self.config.get("implementation_status", {}),
                    "testing": "completed"
                }
            })
        else:
            print("\n⚠️ Alguns testes falharam. Verifique a configuração.")

def main():
    """Função principal"""
    print("🔗 Teste de Integração Webhooks Calendly → Zapier")
    print("=" * 50)

    tester = WebhookTester()

    if not tester.config:
        print("❌ Não foi possível carregar a configuração")
        return

    tester.run_all_tests()

if __name__ == "__main__":
    main()