# meu-pdi

## 🎯 Plataforma de Desenvolvimento Individual

**Status:** ✅ Portal do Aluno MVP Completo - Fase de Testes de Usuário

### 📋 Sobre o Projeto

Plataforma e serviço de mentoria para Plano de Desenvolvimento Individual (PDI) personalizado para profissionais de tecnologia. Foco em crescimento de carreira através de PDI estratégico + acompanhamento sênior.

**Metodologia:** PDI Centralizado + Diário de Sessão + Diário de Bordo
**Modelo:** Service-First (mentoria) → Platform (automatizada)

### 🏗️ Arquitetura Atual

- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS
- **Backend:** FastAPI + PostgreSQL (✅ implementado)
- **Padrões:** App Router, TypeScript strict, utility-first CSS

### 🏗️ Arquitetura Futura (Migrações Planejadas)

- **Frontend:** Angular + TypeScript + Tailwind CSS (ADR-003 aprovado)
- **Backend:** FastAPI + PostgreSQL + PyJWT/Authlib (ADR-004 aprovado)
- **Segurança:** Migração crítica por CVEs ativas (CVE-2024-33664, CVE-2024-33663)
- **Status:** Épico 2 criado com 8 tasks técnicas SMART




### 📊 Progresso Atual

- ✅ **Backlog Reorganizado:** 4 épicos com prioridades claras (Segurança → Validação → Arquitetura → Evolução)
- ✅ **Épico 0 (Segurança):** CVEs críticas identificadas - migração python-jose → PyJWT/Authlib
- ✅ **Épico 1 (Validação):** MVP validado com sucesso - pronto para Fase 2 (TASK-TU005 ✅)
- ✅ **Épico 2 (Arquitetura):** Setup Angular enterprise concluído (TASK-ARCH001 ✅) + Componentes Auth migrados (TASK-ARCH002 ✅) + Dashboard PDI migrado (TASK-ARCH003 ✅) + Testes E2E Dashboard implementados (TASK-ARCH005 ✅) + Estatísticas do Usuário integradas (TASK-DASH001 ✅)
- ✅ **Backend FastAPI:** Setup completo (TASK-010 ✅) + Imports modulares corrigidos (TASK-011 ✅) + Sistema de autenticação JWT funcional (TASK-012 ✅) + Integração Frontend Angular (TASK-013 ✅) + Dashboard PDI Funcional (TASK-014 ✅)
- ✅ **Gate de Qualidade:** EPIC/SPIN/SMART/TDD aplicado com sucesso
- ✅ **Lições Aprendidas:** Sistema implementado para aprendizado contínuo
- ✅ **Portal do Aluno:** MVP completo e validado - pronto para testes de usuário
- ✅ **Sistema de Bugs:** BUG-001, BUG-002, BUG-003 resolvidos com rastreamento profissional
- ✅ **Pagamentos:** TASK-004 concluída (preparação técnica completa)
- ✅ **Webhooks de Pagamento:** TASK-005 concluída (processamento automático Stripe/PagSeguro)
- 🔄 **Sprint Atual:** Fase 2 - Preparação para Testes com Público-Alvo Real
- 🎯 **Próximo Épico:** Épico 0 - Segurança Crítica (4 tasks pendentes)




### 🚀 Funcionalidades Implementadas

- ✅ **Sistema de Qualidade:** Gate EPIC/SPIN/SMART/TDD obrigatório
- ✅ **Documentação Técnica:** Padrões rigorosos aplicados
- ✅ **Estrutura Frontend:** Next.js 14 + TypeScript + Tailwind CSS
- ✅ **Estrutura Angular:** Projeto enterprise Angular 18 com módulos modulares
- ✅ **Componentes Auth Angular:** Login/Register com Reactive Forms + validação completa
- ✅ **Testes TDD Backend:** Estrutura pytest criada (testes falhando - esperado)
- ✅ **Portal do Aluno:** Autenticação completa + Dashboard PDI responsivo (TASK-T001 a T008)
- ✅ **Estatísticas do Usuário:** Dashboard com métricas visuais de engajamento (TASK-STATS001 + TASK-DASH001)
- ✅ **Testes de Usuário:** Framework completo SUS + plano de testes estruturado
- ✅ **Webhooks de Pagamento:** Sistema completo para processamento automático de pagamentos + warnings de depreciação resolvidos




### 🎯 Sprint Atual - Testes de Usuário

**Status:** 🔄 FEATURE-F005 Testes de Usuário (TASK-TU001 ✅, TASK-TU002 ✅, TASK-TU003 ✅, TASK-TU004 🔄) - 4/5 tasks concluídas
**Branch:** `main` (ambiente de produção para testes)
**Tasks:** 5/5 concluídas (Épico 1: ✅ CONCLUÍDO)

1. **TASK-TU001:** Plano de Testes Estruturado ✅
2. **TASK-TU002:** Questionário SUS Adaptado ✅
3. **TASK-TU003:** Ambiente de Teste Automatizado ✅
4. **TASK-TU004:** Execução Fase 1 (Interna) ✅
5. **TASK-TU005:** Análise de Resultados ✅

**Metodologia:** Lean UX + SUS (System Usability Scale) + Feedback Qualitativo

### � Guia de Validação Local

Para executar o projeto localmente e validar todas as funcionalidades implementadas, consulte o **[Guia de Validação Local](docs/guia-validacao-local-portal-aluno.md)**.

**O guia inclui:**

- ✅ Instalação passo a passo
- ✅ Configuração de ambiente
- ✅ Execução dos servidores
- ✅ Checklist de validação funcional
- ✅ Solução de problemas comuns
- ✅ Comandos de desenvolvimento


### 🚀 Próximos Passos

1. **TASK-005:** Webhooks de Pagamento ✅ CONCLUÍDA
2. **Sprint Atual:** Épico 3 - Monetização (TASK-006: Templates de Recibo)
3. **Sprint 1-2:** Foundation + Portal Aluno Básico
4. **Sprint 3-4:** Portal Mentor Core
5. **Sprint 5-6:** Portal Gestor + Integração


### 📁 Estrutura do Projeto

```bash
meu-pdi/
├── business/          # 📊 Documentação de negócio
├── planning/          # 📋 Backlog e arquitetura
├── tracking/          # 📈 Acompanhamento progresso
├── docs/              # 📚 Documentação técnica
├── src/               # 🚧 Em desenvolvimento
└── README.md          # 📖 Este arquivo
```

### 🛠️ Desenvolvimento

```bash

# Backend

python -m uvicorn src.backend.main:app --reload  # ✅ CORRETO: executar da raiz do projeto

# Frontend

cd src/frontend && npm install
npm run dev  # http://localhost:3000

# Validação

python validate_markdown.py <arquivo.md>

# Gerenciamento de Bugs

python scripts/gerar_codigo_bug.py  # Gera próximo código sequencial BUG-XXX + template
# Template ultra-rápido (3 linhas): docs/template-bug-rapido.md
# Template detalhado: docs/bugs/bugs.md

# Testes de Usuário

python scripts/start_test_servers.py  # Inicia backend + frontend simultaneamente
```

---

**Última Atualização:** 04 de novembro de 2025
**Contato:** jadergreiner (GitHub)
