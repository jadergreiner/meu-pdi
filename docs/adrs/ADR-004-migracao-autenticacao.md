# ADR-004: Migração de python-jose para PyJWT/Authlib

## Status

**Proposto** → Aprovado → Concluído

## Contexto e Problema

A aplicação utiliza atualmente `python-jose` para manipulação de JWT/JWS. Esta biblioteca apresenta vulnerabilidades críticas de segurança:

- **CVE-2024-33664**: Algoritmo de assinatura ECDSA vulnerável
- **CVE-2024-33663**: Algoritmo de assinatura RSA vulnerável
- **Suporte limitado**: Biblioteca não é mais mantida ativamente
- **Dependências desatualizadas**: Impacta segurança geral da aplicação

## Decisão

Migrar a autenticação de **python-jose** para **PyJWT/Authlib** como bibliotecas principais para JWT/JWS.

## Fundamentos Técnicos

### 1. Comparação de Bibliotecas

| Característica | python-jose | PyJWT/Authlib |
|---|---|---|
| **Status de Segurança** | Vulnerabilidades críticas (CVEs) | Ativamente mantido, seguro |
| **Algoritmos Suportados** | Limitado | Completo (RSA, ECDSA, HMAC, etc.) |
| **Performance** | Adequada | Otimizada para produção |
| **Manutenção** | Abandonada | Ativa e frequente |
| **Documentação** | Básica | Completa e atualizada |

### 2. Benefícios da Migração

- **Segurança**: Eliminação de vulnerabilidades críticas
- **Confiabilidade**: Biblioteca mantida por comunidade ativa
- **Performance**: Melhor otimização para operações JWT
- **Compatibilidade**: Suporte completo a algoritmos modernos
- **Futuro**: Garantia de atualizações de segurança

### 3. Estratégia de Migração

#### PyJWT para Operações Básicas
- **Uso**: Verificação e decodificação de tokens JWT simples
- **Vantagens**: API simples, performance otimizada
- **Casos de Uso**: Autenticação básica, validação de tokens

#### Authlib para Operações Avançadas
- **Uso**: JWS, JOSE, OAuth2, OpenID Connect
- **Vantagens**: Framework completo para autenticação moderna
- **Casos de Uso**: Integração com provedores OAuth, validação avançada

## Consequências

### Positivas

- ✅ **Segurança crítica** resolvida (CVEs eliminadas)
- ✅ **Manutenibilidade** garantida com biblioteca ativa
- ✅ **Performance** melhorada em operações JWT
- ✅ **Escalabilidade** para recursos avançados de autenticação
- ✅ **Conformidade** com padrões de segurança atuais

### Negativas

- ❌ **Refatoração** do código de autenticação existente
- ❌ **Testes extensivos** necessários para validação
- ❌ **Curva de aprendizado** das novas APIs
- ❌ **Dependências** adicionais (Authlib para recursos avançados)

## Alternativas Consideradas

### Opção 1: Manter python-jose
- **Vantagens**: Sem refatoração imediata
- **Desvantagens**: Riscos de segurança críticos, sem suporte

### Opção 2: jose (JavaScript)
- **Vantagens**: Ecossistema maduro
- **Desvantagens**: Incompatível com backend Python

### Opção 3: cryptography + custom
- **Vantagens**: Controle total
- **Desvantagens**: Desenvolvimento complexo, alto risco de bugs

## Plano de Migração

### Fase 1: Análise e Planejamento (3-5 dias)
- [ ] Mapeamento completo do uso atual de python-jose
- [ ] Identificação de algoritmos e operações utilizadas
- [ ] Definição da estratégia PyJWT vs Authlib por módulo

### Fase 2: Migração Core (1-2 semanas)
- [ ] Instalação das novas bibliotecas
- [ ] Migração de funções básicas (verificação/decodificação)
- [ ] Atualização de imports e dependências

### Fase 3: Migração Avançada (1 semana)
- [ ] Migração de operações JWS complexas
- [ ] Implementação de novos padrões de segurança
- [ ] Refatoração de middleware de autenticação

### Fase 4: Testes e Validação (1 semana)
- [ ] Testes unitários completos
- [ ] Testes de integração de autenticação
- [ ] Validação de performance e segurança

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Quebra de autenticação | Alta | Crítico | Testes abrangentes + rollback plan |
| Performance degradation | Média | Médio | Benchmarks antes/depois da migração |
| Incompatibilidade de tokens | Baixa | Alto | Estratégia de transição gradual |
| Curva de aprendizado | Média | Baixo | Documentação + exemplos de migração |

## Métricas de Sucesso

- [ ] Zero vulnerabilidades de segurança (CVEs resolvidas)
- [ ] Cobertura de testes: ≥ 95% para autenticação
- [ ] Performance: Sem degradação > 5%
- [ ] Tempo de migração: ≤ 4 semanas
- [ ] Zero incidentes de autenticação em produção

## Código de Exemplo

### Antes (python-jose)
```python
from jose import jwt, jws

# Verificação básica
payload = jwt.decode(token, key, algorithms=['RS256'])

# JWS avançado
signed = jws.sign(payload, key, algorithm='RS256')
```

### Depois (PyJWT/Authlib)
```python
from jwt import decode as jwt_decode
from authlib.jose import jwt as authlib_jwt

# Verificação básica com PyJWT
payload = jwt_decode(token, key, algorithms=['RS256'])

# JWS avançado com Authlib
header = {'alg': 'RS256'}
token = authlib_jwt.encode(header, payload, key)
```

---

**Data:** 03/11/2025
**Decisor:** Equipe de Segurança
**Aprovadores:** [Lista de aprovadores]
