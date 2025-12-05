#!/usr/bin/env python3
"""
Script para renomear funções de teste em lote.
Substitui nomes de funções de teste do inglês para o português em todos os arquivos de teste.

Uso: python scripts/batch_rename_test_functions.py
"""

import os
import re
from pathlib import Path

# Dicionário de traduções: inglês -> português
TRANSLATIONS = {
    'test_user_registration_valid_data': 'test_cadastro_usuario_dados_validos',
    'test_user_registration_invalid_data': 'test_cadastro_usuario_dados_invalidos',
    'test_user_registration_duplicate_email': 'test_cadastro_usuario_email_duplicado',
    'test_user_registration_success': 'test_cadastro_usuario_sucesso',
    'test_email_validation_token_creation': 'test_validacao_email_criacao_token',
    'test_email_validation_token_verification': 'test_validacao_email_verificacao_token',
    'test_email_validation_token_expiry': 'test_validacao_email_expiracao_token',
    'test_email_validation_invalid_token': 'test_validacao_email_token_invalido',
    'test_user_login_success': 'test_login_usuario_sucesso',
    'test_user_login_invalid_credentials': 'test_login_usuario_credenciais_invalidas',
    'test_user_login_unverified_email': 'test_login_usuario_email_nao_verificado',
    'test_user_login_locked_account': 'test_login_usuario_conta_bloqueada',
    'test_password_reset_request_success': 'test_solicitacao_reset_senha_sucesso',
    'test_password_reset_request_invalid_email': 'test_solicitacao_reset_senha_email_invalido',
    'test_password_reset_confirm_success': 'test_confirmacao_reset_senha_sucesso',
    'test_password_reset_confirm_invalid_token': 'test_confirmacao_reset_senha_token_invalido',
    'test_password_reset_confirm_expired_token': 'test_confirmacao_reset_senha_token_expirado',
    'test_get_user_profile_success': 'test_obter_perfil_usuario_sucesso',
    'test_get_user_profile_not_found': 'test_obter_perfil_usuario_nao_encontrado',
    'test_get_user_profile_unauthorized': 'test_obter_perfil_usuario_nao_autorizado',
    'test_update_user_profile_success': 'test_atualizar_perfil_usuario_sucesso',
    'test_update_user_profile_invalid_data': 'test_atualizar_perfil_usuario_dados_invalidos',
    'test_update_user_profile_not_found': 'test_atualizar_perfil_usuario_nao_encontrado',
    'test_update_user_profile_unauthorized': 'test_atualizar_perfil_usuario_nao_autorizado',
    'test_get_pdi_overview_success': 'test_obter_visao_geral_pdi_sucesso',
    'test_get_pdi_overview_not_found': 'test_obter_visao_geral_pdi_nao_encontrado',
    'test_get_pdi_overview_unauthorized': 'test_obter_visao_geral_pdi_nao_autorizado',
    'test_get_next_steps_success': 'test_obter_proximos_passos_sucesso',
    'test_get_next_steps_not_found': 'test_obter_proximos_passos_nao_encontrado',
    'test_get_next_steps_unauthorized': 'test_obter_proximos_passos_nao_autorizado',
    'test_get_responsive_config_success': 'test_obter_config_responsiva_sucesso',
    'test_get_responsive_config_not_found': 'test_obter_config_responsiva_nao_encontrado',
    'test_get_responsive_config_unauthorized': 'test_obter_config_responsiva_nao_autorizado',
    'test_api_responses_mobile_friendly': 'test_respostas_api_amigaveis_mobile',
    'test_api_responses_desktop_optimized': 'test_respostas_api_otimizadas_desktop',
    'test_api_responses_tablet_compatible': 'test_respostas_api_compativeis_tablet',
    'test_api_responses_accessibility_compliant': 'test_respostas_api_conformes_acessibilidade',
    'test_api_responses_performance_optimized': 'test_respostas_api_otimizadas_performance',
    'test_api_responses_error_handling': 'test_respostas_api_tratamento_erros',
    'test_api_responses_caching_strategy': 'test_respostas_api_estrategia_cache',
    'test_api_responses_security_headers': 'test_respostas_api_cabecalhos_seguranca'
}

def rename_functions_in_file(file_path):
    """Renomeia funções de teste em um arquivo específico."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Regex para encontrar definições de função de teste
    pattern = r'(def\s+)(test_[a-zA-Z_]+)(\s*\()'

    def replace_func(match):
        func_name = match.group(2)
        if func_name in TRANSLATIONS:
            return match.group(1) + TRANSLATIONS[func_name] + match.group(3)
        return match.group(0)

    content = re.sub(pattern, replace_func, content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Função principal para processar todos os arquivos de teste."""
    test_dir = Path('tests')
    if not test_dir.exists():
        print("Diretório 'tests' não encontrado.")
        return

    files_modified = 0
    for test_file in test_dir.glob('test_*.py'):
        if rename_functions_in_file(test_file):
            print(f"Modificado: {test_file}")
            files_modified += 1
        else:
            print(f"Sem mudanças: {test_file}")

    print(f"\nTotal de arquivos modificados: {files_modified}")

if __name__ == '__main__':
    main()