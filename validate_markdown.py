#!/usr/bin/env python3
"""
Script simples para validação básica de markdown
Demonstra implementação prática das lições aprendidas sobre qualidade de documentação
"""

import re
import sys
from pathlib import Path

def validate_markdown_basic(file_path):
    """Validação básica de markdown baseada nas regras mais comuns"""
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return [f"Arquivo não encontrado: {file_path}"]

    lines = content.split('\n')

    # MD022: Headings should be surrounded by blank lines
    for i, line in enumerate(lines):
        if line.startswith('#') and not line.startswith('######'):
            # Check previous line
            if i > 0 and lines[i-1].strip() != '':
                errors.append(f"Linha {i+1}: Heading deve ser precedido por linha em branco")
            # Check next line
            if i < len(lines)-1 and lines[i+1].strip() != '' and not lines[i+1].startswith('#'):
                errors.append(f"Linha {i+1}: Heading deve ser seguido por linha em branco")

    # MD032: Lists should be surrounded by blank lines
    in_list = False
    for i, line in enumerate(lines):
        is_list_item = line.strip().startswith(('- ', '* ', '+ ', '1. ', '2. ', '3. '))
        if is_list_item and not in_list:
            # Check if previous line is blank
            if i > 0 and lines[i-1].strip() != '':
                errors.append(f"Linha {i+1}: Item de lista deve ser precedido por linha em branco")
            in_list = True
        elif not is_list_item and in_list:
            # Check if next line is blank (end of list)
            if i < len(lines)-1 and lines[i+1].strip() != '' and not lines[i+1].strip().startswith(('- ', '* ', '+ ', '1. ', '2. ', '3. ')):
                errors.append(f"Linha {i+1}: Lista deve ser seguida por linha em branco")
            in_list = False

    # MD047: Files should end with a single newline
    if content and not content.endswith('\n'):
        errors.append("Arquivo deve terminar com uma nova linha")

    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python validate_markdown.py <arquivo.md>")
        sys.exit(1)

    file_path = sys.argv[1]
    errors = validate_markdown_basic(file_path)

    if errors:
        print(f"❌ Encontrados {len(errors)} erros de formatação em {file_path}:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"✅ {file_path} está formatado corretamente!")
        sys.exit(0)