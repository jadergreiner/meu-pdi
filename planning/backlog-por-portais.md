# 📋 Backlog Refinado - Plataforma Própria por Portais

**Data:** 02 de novembro de 2025
**Status:** 🔄 Refinado por Personas
**Baseado em:** Backlog anterior + Análise de Personas

---

## 🎯 **Visão Geral do Refinamento**

### **Estrutura por Portais**

Seguindo análise das 3 personas principais, o backlog foi reorganizado por portais de usuário:

- **🛡️ Portal do Gestor:** Interface administrativa para gestão da plataforma
- **👨‍🏫 Portal do Mentor:** Ferramentas para mentores gerenciarem sessões e mentorados
- **🎓 Portal do Aluno:** Interface para mentorados agendarem e acompanharem PDI


### **Critérios SMART Aplicados**

Todas as tasks seguem rigorosamente os critérios SMART:

- **Specific:** Descrição clara e objetiva
- **Measurable:** Critérios de aceitação mensuráveis
- **Achievable:** Técnicamente viável com recursos disponíveis
- **Relevant:** Alinhado com objetivos de negócio
- **Time-bound:** Estimativa temporal realista


---

## 🛡️ **PORTAL DO GESTOR - Interface Administrativa**

### **🎯 FEATURE-GEST-001: Dashboard Executivo**

**Descrição:** Visão geral da plataforma com métricas críticas**

#### **TASK-GEST-001: Dashboard Principal** ⏳

- **Specific:** Dashboard com KPIs: receita, usuários ativos, sessões realizadas, taxa no-show
- **Measurable:** Dados atualizados em tempo real, gráficos funcionais
- **Achievable:** Next.js + SQL queries + charts library
- **Relevant:** Visibilidade operacional para tomada de decisão
- **Time-bound:** 6 horas
- **Status:** Pendente


#### **TASK-GEST-002: Relatórios Analytics** ⏳

- **Specific:** Relatórios detalhados: conversão experimental→pago, retenção mentores, satisfação
- **Measurable:** Export PDF/Excel funcionando, filtros por período
- **Achievable:** SQL queries + React-PDF + date filters
- **Relevant:** Métricas para otimização de negócio
- **Time-bound:** 8 horas
- **Status:** Pendente


### **👥 FEATURE-GEST-002: Gestão de Usuários**

**Descrição:** Administração completa de usuários da plataforma**

#### **TASK-GEST-003: CRUD Usuários** ⏳

- **Specific:** Interface para visualizar, editar, banir/reativar usuários
- **Measurable:** Todas operações funcionando, histórico de ações
- **Achievable:** Admin routes + API calls + audit log
- **Relevant:** Moderação e suporte ao usuário
- **Time-bound:** 6 horas
- **Status:** Pendente


#### **TASK-GEST-004: Gestão de Mentores** ⏳

- **Specific:** Aprovação/rejeição de mentores, configuração de especialidades
- **Measurable:** Workflow completo de aprovação, notificações automáticas
- **Achievable:** Status management + email notifications
- **Relevant:** Controle de qualidade dos mentores
- **Time-bound:** 4 horas
- **Status:** Pendente


### **⚙️ FEATURE-GEST-003: Configurações da Plataforma**

**Descrição:** Configuração dinâmica de regras e preços**

#### **TASK-GEST-005: Configurações de Preços** ⏳

- **Specific:** Interface para ajustar preço experimental, comissões mentores
- **Measurable:** Mudanças aplicadas automaticamente, histórico de alterações
- **Achievable:** Settings API + validation + audit trail
- **Relevant:** Flexibilidade operacional e precificação dinâmica
- **Time-bound:** 3 horas
- **Status:** Pendente


#### **TASK-GEST-006: Regras de Negócio** ⏳

- **Specific:** Configuração de políticas: cancelamento, reembolso, antecedência
- **Measurable:** Regras aplicadas automaticamente em novos agendamentos
- **Achievable:** Business rules engine + database config
- **Relevant:** Adaptação às necessidades do negócio
- **Time-bound:** 4 horas
- **Status:** Pendente


### **🔒 FEATURE-GEST-004: Segurança e Monitoramento**

**Descrição:** Ferramentas de segurança e observabilidade**

#### **TASK-GEST-007: Logs de Auditoria** ⏳

- **Specific:** Visualização de logs: logins, pagamentos, alterações críticas
- **Measurable:** Busca por usuário/data, export de relatórios
- **Achievable:** Audit logging + search interface
- **Relevant:** Compliance e troubleshooting
- **Time-bound:** 5 horas
- **Status:** Pendente


#### **TASK-GEST-008: Monitoramento Sistema** ⏳

- **Specific:** Dashboard de health check: uptime, performance, erros
- **Measurable:** Alertas automáticos, métricas em tempo real
- **Achievable:** Monitoring tools integration + alerts
- **Relevant:** Manutenção proativa da plataforma
- **Time-bound:** 4 horas
- **Status:** Pendente


---

## 👨‍🏫 **PORTAL DO MENTOR - Ferramentas do Mentor**

### **📅 FEATURE-MENT-001: Gestão de Disponibilidade**

**Descrição:** Controle completo da agenda do mentor**

#### **TASK-MENT-001: Calendário de Disponibilidade** ⏳

- **Specific:** Interface para definir horários disponíveis, bloqueios, exceções
- **Measurable:** Calendário interativo funcionando, dados persistindo
- **Achievable:** React Big Calendar + drag-drop + API
- **Relevant:** Base para agendamentos dos mentorados
- **Time-bound:** 6 horas
- **Status:** Pendente


#### **TASK-MENT-002: Configuração de Sessões** ⏳

- **Specific:** Definição de duração padrão, modalidade (presencial/online), valor hora
- **Measurable:** Configurações aplicadas automaticamente nos agendamentos
- **Achievable:** Profile settings + validation
- **Relevant:** Personalização da oferta de mentoria
- **Time-bound:** 3 horas
- **Status:** Pendente


### **👥 FEATURE-MENT-002: Gestão de Mentorados**

**Descrição:** Acompanhamento e gestão dos alunos**

#### **TASK-MENT-003: Lista de Mentorados** ⏳

- **Specific:** Dashboard com lista de mentorados ativos, histórico de sessões
- **Measurable:** Filtros funcionando, detalhes de cada mentorado visíveis
- **Achievable:** Data table + filters + user profiles
- **Relevant:** Visibilidade dos alunos acompanhados
- **Time-bound:** 4 horas
- **Status:** Pendente


#### **TASK-MENT-004: PDI Centralizado** ⏳

- **Specific:** Interface para criar/editar PDI de cada mentorado
- **Measurable:** Templates estruturados, versionamento automático
- **Achievable:** Rich text editor + templates + versioning
- **Relevant:** Core da metodologia de mentoria
- **Time-bound:** 8 horas
- **Status:** Pendente


### **📝 FEATURE-MENT-003: Diário de Sessão**

**Descrição:** Registro e acompanhamento das sessões**

#### **TASK-MENT-005: Registro de Sessões** ⏳

- **Specific:** Formulário para registrar ocorrências, avanços, próximos passos
- **Measurable:** Dados salvos automaticamente, notificações para mentorado
- **Achievable:** Session forms + auto-save + notifications
- **Relevant:** Rastreabilidade do progresso
- **Time-bound:** 5 horas
- **Status:** Pendente


#### **TASK-MENT-006: Diário de Bordo** ⏳

- **Specific:** Espaço para anotações pessoais sobre evolução do mentorado
- **Measurable:** Notas privadas visíveis apenas para o mentor
- **Achievable:** Private notes + rich text + search
- **Relevant:** Reflexões estratégicas do mentor
- **Time-bound:** 3 horas
- **Status:** Pendente


### **💰 FEATURE-MENT-004: Gestão Financeira**

**Descrição:** Acompanhamento de receita e pagamentos**

#### **TASK-MENT-007: Relatório Financeiro** ⏳

- **Specific:** Dashboard com sessões realizadas, receita, comissões pendentes
- **Measurable:** Cálculos automáticos, export de comprovantes
- **Achievable:** Financial queries + PDF generation
- **Relevant:** Transparência financeira
- **Time-bound:** 4 horas
- **Status:** Pendente


---

## 🎓 **PORTAL DO ALUNO - Interface do Mentorado**

### **🔐 FEATURE-ALUN-001: Acesso e Perfil**

**Descrição:** Cadastro e gestão do perfil do mentorado**

#### **TASK-ALUN-001: Cadastro e Login** 🔄

- **Specific:** Fluxo completo de registro, validação email, recuperação senha
- **Measurable:** Taxa conversão >80%, zero erros no fluxo
- **Achievable:** NextAuth + React Hook Form + email validation
- **Relevant:** Barreira de entrada minimizada
- **Time-bound:** 6 horas
- **Status:** 🔄 EM DESENVOLVIMENTO (Gate Aprovado - Branch: feature/US-U001-auth-portal-aluno)


#### **TASK-ALUN-002: Perfil do Usuário** ⏳

- **Specific:** Formulário completo: dados pessoais, objetivos profissionais, experiência
- **Measurable:** Profile completion >90%, dados validados
- **Achievable:** Multi-step form + validation + progress indicator
- **Relevant:** Base para matching com mentores
- **Time-bound:** 5 horas
- **Status:** Pendente


### **📅 FEATURE-ALUN-002: Agendamento de Sessões**

**Descrição:** Processo completo de agendamento**

#### **TASK-ALUN-003: Busca de Mentores** ⏳

- **Specific:** Interface para filtrar mentores por especialidade, avaliação, preço
- **Measurable:** Filtros funcionando, perfis detalhados visíveis
- **Achievable:** Search + filters + mentor profiles
- **Relevant:** Matching eficiente mentor-mentorado
- **Time-bound:** 4 horas
- **Status:** Pendente


#### **TASK-ALUN-004: Agendamento Interativo** ⏳

- **Specific:** Calendário mostrando disponibilidade, seleção de horário
- **Measurable:** Zero conflitos, confirmação automática
- **Achievable:** Calendar component + booking logic
- **Relevant:** Experiência fluida de agendamento
- **Time-bound:** 6 horas
- **Status:** Pendente


### **💳 FEATURE-ALUN-003: Sistema de Pagamentos**

**Descrição:** Pagamento da taxa experimental**

#### **TASK-ALUN-005: Checkout PIX** ⏳

- **Specific:** Integração PIX com QR code, confirmação automática
- **Measurable:** Taxa conversão >85%, confirmações em <5min
- **Achievable:** Stripe/PagSeguro + webhooks
- **Relevant:** Monetização da plataforma
- **Time-bound:** 6 horas
- **Status:** Pendente


#### **TASK-ALUN-006: Reembolso Automático** ⏳

- **Specific:** Sistema de reembolso condicional baseado em participação
- **Measurable:** Reembolsos processados automaticamente conforme regras
- **Achievable:** Business logic + payment API
- **Relevant:** Redução da barreira financeira
- **Time-bound:** 4 horas
- **Status:** Pendente


### **📊 FEATURE-ALUN-004: Acompanhamento do PDI**

**Descrição:** Visibilidade do progresso pessoal**

#### **TASK-ALUN-007: Dashboard do PDI** ⏳

- **Specific:** Visualização do PDI atual, metas, progresso por competência
- **Measurable:** Progress tracking funcionando, notificações de avanços
- **Achievable:** Progress indicators + charts + notifications
- **Relevant:** Engajamento contínuo do mentorado
- **Time-bound:** 5 horas
- **Status:** Pendente


#### **TASK-ALUN-008: Histórico de Sessões** ⏳

- **Specific:** Lista de sessões realizadas, resumos, próximos passos
- **Measurable:** Histórico completo, acesso fácil aos registros
- **Achievable:** Session history + search + export
- **Relevant:** Continuidade do acompanhamento
- **Time-bound:** 3 horas
- **Status:** Pendente


### **📧 FEATURE-ALUN-005: Comunicação**

**Descrição:** Notificações e lembretes automáticos**

#### **TASK-ALUN-009: Notificações Automáticas** ⏳

- **Specific:** Lembretes 24h e 1h antes, confirmações, atualizações PDI
- **Measurable:** Taxa abertura >70%, redução no-show <10%
- **Achievable:** Email + push notifications + scheduler
- **Relevant:** Engajamento e redução de faltas
- **Time-bound:** 4 horas
- **Status:** Pendente


---

## 📊 **Métricas de Capacidade por Portal**

### **Portal do Gestor**

- **Total Tasks:** 8
- **Esforço Estimado:** 40 horas
- **Prioridade:** P0-P1 (crítico para operação)


### **Portal do Mentor**

- **Total Tasks:** 7
- **Esforço Estimado:** 33 horas
- **Prioridade:** P0-P1 (core da proposta de valor)


### **Portal do Aluno**

- **Total Tasks:** 9
- **Esforço Estimado:** 43 horas
- **Prioridade:** P0-P1 (experiência do usuário)


### **Comparativo com Backlog Anterior**

- **Tasks Totais:** 24 (vs 33 anteriores - mais focado)
- **Esforço Total:** 116 horas (vs 160h - 27% redução)
- **Foco:** 100% nas 3 personas principais


---

## 🔄 **Dependências Técnicas Compartilhadas**

### **Infraestrutura Comum (P0)**

- **TASK-001:** Setup Next.js com TypeScript
- **TASK-002:** Setup FastAPI com PostgreSQL
- **TASK-003:** Autenticação JWT
- **TASK-004:** Redis para Cache
- **TASK-005:** CI/CD GitHub Actions


### **APIs Compartilhadas**

- **TASK-007:** API de Usuários (perfis para todos os tipos)
- **TASK-011:** API de Agendamentos (usada por mentores e alunos)
- **TASK-014-017:** Sistema de Pagamentos (focado no aluno)


---

## 📈 **Roadmap de Implementação**

### **Sprint 1-2: Foundation + Portal Aluno (Básico)**

- Infraestrutura + Cadastro/Login + Perfil básico
- **Entregável:** MVP funcional para captação de usuários


### **Sprint 3-4: Portal Mentor (Core)**

- Disponibilidade + PDI Centralizado + Diário de Sessão
- **Entregável:** Mentoria básica funcionando


### **Sprint 5-6: Portal Gestor + Integração**

- Dashboard admin + analytics + configurações
- **Entregável:** Plataforma completa operacional


---

## ✅ **Critérios de Qualidade por Portal**

### **Portal do Gestor**

- **Performance:** Dashboard carregando em <2s
- **Usabilidade:** Operações críticas em ≤3 cliques
- **Confiabilidade:** 99.9% uptime dos dados críticos


### **Portal do Mentor**

- **Eficiência:** PDI criado em <10min
- **Precisão:** Zero conflitos de agendamento
- **Engajamento:** Taxa resposta notificações >80%


### **Portal do Aluno**

- **Conversão:** Taxa cadastro→pagamento >60%
- **Satisfação:** NPS >70 na primeira sessão
- **Retenção:** Taxa comparecimento >90%


## 📚 **LIÇÕES APRENDIDAS**

### **Estrutura de Registro**

Cada lição aprendida segue o formato padronizado para aprendizado contínuo:

**Código Sequencial:** LA-XXX (LA = Lição Aprendida)  
**Data:** DD/MM/YYYY  
**Contexto da Ocorrência:** Descrição detalhada da situação  
**Erro ou Impacto Gerado:** Consequências do problema  
**Qual a Lição Aprendida:** Aprendizado extraído e ação preventiva  
**Status:** [Registrado, Aplicado, Rejeitado]

---

**Última Atualização:** 02 de novembro de 2025
**Status:** 🔄 Aguardando validação das funcionalidades por portal
**Próximo Passo:** Implementação do Portal do Aluno (prioridade de captação)</content>
<parameter name="filePath">c:\repo\projetos\meu-pdi\planning\backlog-por-portais.md</content>
<parameter name="filePath">c:\repo\projetos\meu-pdi\planning\backlog-por-portais.md
 
 
