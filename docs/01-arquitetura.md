# 🏗️ Arquitetura da Plataforma Meu PDI

## 📋 Visão Geral da Arquitetura

Documento unificado consolidando todas as decisões arquiteturais da plataforma Meu PDI, incluindo ADRs aprovados e decisões técnicas tomadas.

## 🎯 Princípios Arquiteturais

### **1. Service-First → Platform**
- **Fase Atual:** Foco em serviço de mentoria (Calendly + Zapier + Notion)
- **Fase Futura:** Plataforma própria com automação completa
- **Transição:** Migração gradual mantendo valor para usuários

### **2. Segurança como Prioridade**
- **Autenticação:** Migração para bibliotecas seguras (PyJWT/Authlib)
- **Dados:** Criptografia end-to-end, compliance LGPD
- **Monitoramento:** Logs de segurança e alertas automáticos

### **3. Escalabilidade Enterprise**
- **Frontend:** Framework estruturado (Angular) para consistência
- **Backend:** FastAPI com padrões RESTful e GraphQL
- **Infraestrutura:** Cloud-native com containers e orquestração

### **4. Experiência do Desenvolvedor**
- **Qualidade:** TDD obrigatório, testes automatizados
- **Documentação:** Padrões rigorosos, ADRs para decisões
- **Ferramentas:** CLI integradas, automação de processos

---

## 📚 Architecture Decision Records (ADRs)

### **ADR-001: Arquitetura No-Code First** ✅ Aprovado
**Data:** 02/11/2025
**Decisão:** Priorizar no-code/MVP para validação rápida de hipóteses
**Justificativa:** Reduz riscos, acelera time-to-market, foco em produto
**Status:** Implementado (Calendly + Zapier + Notion)

### **ADR-002: Plataforma Própria** ✅ Aprovado
**Data:** 02/11/2025
**Decisão:** Desenvolver plataforma própria após validação MVP
**Justificativa:** Controle total, escalabilidade, diferenciação competitiva
**Status:** Planejado (Épico 2 em desenvolvimento)

### **ADR-003: Migração Next.js → Angular** ✅ Aprovado
**Data:** 03/11/2025
**Decisão:** Migrar frontend para Angular framework
**Justificativa:** Estrutura enterprise, TypeScript obrigatório, ferramentas integradas
**Status:** Planejado (TASK-010 a TASK-013 pendentes)

### **ADR-004: Migração python-jose → PyJWT/Authlib** ✅ Aprovado
**Data:** 03/11/2025
**Decisão:** Migrar autenticação para bibliotecas seguras
**Justificativa:** CVEs críticas (CVE-2024-33664, CVE-2024-33663), manutenção ativa
**Status:** Planejado (TASK-014 a TASK-017 pendentes)

---

## 🏛️ Arquitetura Técnica Atual

### **Frontend (MVP)**
```
Next.js 14 + TypeScript + Tailwind CSS
├── App Router (File-based routing)
├── Server Components + Client Components
├── API Routes (Next.js API)
├── Responsive Design (Mobile-first)
└── Componentes: Auth (Login/Register) + Dashboard
```

### **Backend (Planejado)**
```
FastAPI + Python 3.11+
├── RESTful APIs com OpenAPI/Swagger
├── PostgreSQL (Dados relacionais)
├── Redis (Cache/Sessões)
├── JWT Authentication (PyJWT/Authlib)
└── Background Jobs (Celery)
```

### **Infraestrutura (MVP)**
```
No-Code Stack
├── Calendly (Agendamento)
├── Zapier (Automação)
├── Notion (Banco de dados temporário)
├── Gmail/Outlook (Templates de email)
└── Google Workspace (Documentos)
```

---

## 🏛️ Arquitetura Técnica Futura

### **Frontend (Angular)**
```
Angular 17+ + TypeScript + Tailwind CSS
├── Standalone Components + Signals
├── RxJS para reatividade
├── Angular CLI + Schematics
├── Module-based architecture
└── Playwright E2E testing
```

### **Backend (FastAPI)**
```
FastAPI + Python 3.11+
├── RESTful APIs + GraphQL
├── PostgreSQL + SQLAlchemy
├── Redis Cluster
├── PyJWT/Authlib (JWT/JWS/JWE)
└── Docker + Kubernetes
```

### **Infraestrutura (Cloud)**
```
Azure/AWS Cloud Stack
├── Container Apps (Frontend)
├── AKS (Backend APIs)
├── PostgreSQL Flexible Server
├── Redis Cache
├── Azure Front Door (CDN)
└── GitHub Actions CI/CD
```

---

## 🔄 Plano de Migração Arquitetural

### **Épico 2: Migrações Críticas** 🎯 Em Planejamento

#### **Feature 2.1: Frontend Angular** 🔥 Prioridade Crítica
- **TASK-010:** Setup projeto Angular enterprise (8h)
- **TASK-011:** Migrar componentes auth (12h)
- **TASK-012:** Migrar dashboard PDI (16h)
- **TASK-013:** Configurar testes E2E (10h)

#### **Feature 2.2: Autenticação Segura** 🔥 Prioridade Crítica
- **TASK-014:** Análise segurança python-jose (6h)
- **TASK-015:** Migrar para PyJWT core (8h)
- **TASK-016:** Implementar Authlib avançado (12h)
- **TASK-017:** Testes segurança abrangentes (10h)

### **Timeline Estimada**
- **Fase 1:** Setup e planejamento (2 semanas)
- **Fase 2:** Migração core (3 semanas)
- **Fase 3:** Funcionalidades avançadas (2 semanas)
- **Fase 4:** Testes e otimização (2 semanas)
- **Total:** 9 semanas (63 horas desenvolvimento)

---

## 📊 Métricas de Qualidade Arquitetural

### **Segurança**
- ✅ Zero CVEs em bibliotecas críticas
- ✅ Autenticação JWT/JWS segura
- ✅ Criptografia end-to-end
- 🔄 OWASP Top 10 compliance (planejado)

### **Performance**
- ✅ Frontend: < 3s first contentful paint
- ✅ Backend: < 200ms response time APIs
- ✅ Mobile: 100% responsive
- 🔄 Core Web Vitals (planejado)

### **Manutenibilidade**
- ✅ TypeScript obrigatório (100%)
- ✅ Testes automatizados (> 80% cobertura)
- ✅ Documentação técnica completa
- ✅ ADRs para decisões arquiteturais

### **Escalabilidade**
- ✅ Arquitetura modular
- ✅ Stateless APIs
- ✅ Cache distribuído
- 🔄 Horizontal scaling (planejado)

---

## 🔗 Dependências e Integrações

### **APIs Externas**
- **Calendly API:** Agendamento de sessões
- **Stripe/PagSeguro:** Processamento de pagamentos
- **Google Workspace:** Documentos e planilhas
- **Zoom API:** Videoconferências (planejado)

### **Serviços Internos**
- **PostgreSQL:** Dados relacionais
- **Redis:** Cache e sessões
- **SendGrid:** Emails transacionais
- **Azure Blob Storage:** Arquivos (planejado)

### **Ferramentas de Desenvolvimento**
- **GitHub Actions:** CI/CD pipelines
- **Playwright:** Testes E2E
- **pytest:** Testes backend
- **ESLint/Prettier:** Qualidade código

---

## 🚨 Riscos e Mitigações

### **Riscos Técnicos**
| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Curva aprendizado Angular | Alta | Médio | Treinamento + mentoria |
| Quebra compatibilidade APIs | Média | Alto | Testes integração + rollback |
| Performance degradation | Baixa | Médio | Benchmarks + otimização |
| Dependências vulneráveis | Alta | Crítico | Atualização automática + scanning |

### **Riscos de Negócio**
| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Tempo migração longo | Média | Médio | Abordagem incremental |
| Custos desenvolvimento | Alta | Baixo | MVP validado + ROI claro |
| Adoção equipe | Média | Alto | Comunicação + envolvimento |
| Concorrência | Baixa | Médio | Diferenciação PDI estratégico |

---

## 📈 Roadmap Tecnológico

### **Q4 2025: MVP Validation**
- ✅ Portal aluno funcional
- ✅ Sistema agendamento no-code
- ✅ Testes usuário em andamento
- 🔄 Métricas validação (SUS, NPS)

### **Q1 2026: Enterprise Architecture**
- 🔄 Migração Angular frontend
- 🔄 Migração PyJWT/Authlib backend
- 🔄 Infraestrutura cloud Azure
- 🔄 APIs GraphQL implementadas

### **Q2 2026: Advanced Features**
- 🔄 Dashboard analytics mentor
- 🔄 Sistema notificações push
- 🔄 Integração Zoom nativa
- 🔄 Mobile app híbrida

### **Q3 2026: Scale & Optimize**
- 🔄 Multi-tenant architecture
- 🔄 Microserviços backend
- 🔄 Global CDN deployment
- 🔄 Advanced AI features

---

## 📚 Referências e Documentação

### **ADRs Aprovados**
- [ADR-001: Arquitetura No-Code First](adrs/ADR-001-arquitetura-no-code-first.md)
- [ADR-002: Plataforma Própria](adrs/ADR-002-plataforma-propria.md)
- [ADR-003: Migração Angular](adrs/ADR-003-migracao-angular.md)
- [ADR-004: Migração Autenticação](adrs/ADR-004-migracao-autenticacao.md)

### **Documentação Técnica**
- [Backlog Priorizado](planning/backlog.md)
- [Diário de Projeto](diario-projeto.md)
- [Guia de Configuração](guia-configuracao-pagamentos-stripe-pagseguro.md)
- [Plano de Testes](plano-testes-usuario-portal-aluno.md)

### **Qualidade e Processo**
- [Gate de Qualidade](gate-qualidade-portal-aluno.md)
- [Lições Aprendidas](licoes-aprendidas.md)
- [Template Bug Rápido](template-bug-rapido.md)

---

**Versão:** 2.0 - Arquitetura Unificada
**Data:** 03/11/2025
**Responsável:** Equipe de Arquitetura
**Próxima Revisão:** Após conclusão Épico 2