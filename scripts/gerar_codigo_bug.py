#!/usr/bin/env python3
"""
Gerador de Códigos Sequenciais para Bugs - Meu PDI

Este script gera códigos sequenciais para novos bugs no formato BUG-XXX.
Lê o arquivo bugs.md e determina o próximo número disponível.

Uso:
    python gerar_codigo_bug.py

Exemplo de saída:
    Próximo código disponível: BUG-003
"""

import os
import re
from datetime import datetime

def gerar_codigo_bug():
    """
    Gera o próximo código sequencial para bug baseado nos registros existentes.

    Returns:
        str: Código no formato BUG-XXX
    """
    # Caminho absoluto para o arquivo bugs.md
    arquivo_bugs = os.path.join(os.path.dirname(__file__), "..", "docs", "bugs", "bugs.md")

    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_bugs):
        print(f"❌ Arquivo {arquivo_bugs} não encontrado!")
        return "BUG-001"

    # Lê o conteúdo do arquivo
    with open(arquivo_bugs, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Busca todos os códigos BUG-XXX no arquivo
    padrao_bug = r'## BUG-(\d{3})'
    matches = re.findall(padrao_bug, conteudo)

    if not matches:
        # Nenhum bug encontrado, começa com 001
        proximo_numero = 1
    else:
        # Encontra o maior número e adiciona 1
        maior_numero = max(int(match) for match in matches)
        proximo_numero = maior_numero + 1

    # Formata com 3 dígitos
    codigo = "03d"

    return codigo

def obter_data_hora_atual():
    """
    Retorna a data e hora atual no formato DD/MM/YYYY HH:MM

    Returns:
        str: Data/hora formatada
    """
    agora = datetime.now()
    return agora.strftime("%d/%m/%Y %H:%M")

def main():
    """Função principal"""
    print("🔢 Gerador de Códigos para Bugs - Meu PDI")
    print("=" * 50)

    # Gera código
    codigo = gerar_codigo_bug()
    print(f"📋 Próximo código disponível: {codigo}")

    # Mostra data/hora atual
    data_hora = obter_data_hora_atual()
    print(f"📅 Data/Hora atual: {data_hora}")

    # Template para novo bug
    print("\n📝 Template para novo bug:")
    print("-" * 30)
    print(f"""## {codigo} - [Título Breve]

**Data/Hora Registro:** {data_hora}
**Status:** 🆕 Aberto
**Severidade:** [Baixa|Média|Alta|Crítica]
**Prioridade:** [Baixa|Média|Alta|Urgente]

### 📋 Detalhes do Bug

**Página/Funcionalidade:** [URL ou descrição]
**Browser/OS:** [Informações do ambiente]
**Usuário:** [Email ou identificação]

### 🔍 Reprodução

**Passos para Reproduzir:**

1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

**Comportamento Esperado:** [Descrição do que deveria acontecer]
**Comportamento Atual:** [Descrição do que está acontecendo]

### 🔧 Investigação

**Causa Identificada:** [Análise técnica do problema]
**Arquivos Afetados:** [Lista de arquivos relacionados]

### ✅ Resolução

**Solução Implementada:** [Descrição da correção]
**Arquivos Modificados:** [Lista de arquivos alterados]
**Testes Realizados:** [Validação da correção]
**Data/Hora Resolução:** DD/MM/YYYY HH:MM

### 📝 Observações

[Informações adicionais relevantes]
""")

if __name__ == "__main__":
    main()