# 🔗 Implementação Webhooks Calendly → Zapier

## 🎯 TASK-002: Implementar Webhooks Calendly → Zapier

**Status:** 🟡 EM ANDAMENTO
**Estimativa:** 4 horas
**Data Início:** 02 de novembro de 2025

---

## 📋 Objetivo da Task

Configurar webhooks no Calendly para enviar dados automaticamente para o Zapier sempre que um novo agendamento for criado, permitindo a automação completa do fluxo de agendamento → registro → notificação.

---

## 🏗️ Arquitetura Técnica

### **Fluxo de Dados**
```
Calendly Event Created
        ↓
    Webhook POST
        ↓
Zapier Webhook Trigger
        ↓
Process & Transform Data
        ↓
Create Notion Record
        ↓
Send Confirmation Email
```

### **Dados Enviados pelo Calendly**
```json
{
  "event": "invitee.created",
  "time": "2025-11-02T10:00:00Z",
  "payload": {
    "event_type": {
      "uuid": "EVENT_TYPE_UUID",
      "kind": "solo",
      "slug": "sessao-pdi-60min",
      "name": "Sessão PDI - 60 minutos",
      "duration": 60
    },
    "invitee": {
      "uuid": "INVITEE_UUID",
      "first_name": "João",
      "last_name": "Silva",
      "email": "joao.silva@email.com",
      "timezone": "America/Sao_Paulo",
      "created_at": "2025-11-02T09:30:00Z",
      "is_reschedule": false,
      "payments": [],
      "canceled": false,
      "canceled_at": null
    },
    "questions_and_answers": [
      {
        "question": "Qual seu objetivo principal com o PDI?",
        "answer": "Desenvolvimento de carreira em tecnologia"
      },
      {
        "question": "Você já fez PDI antes?",
        "answer": "Sim, mas não consegui manter"
      }
    ],
    "questions_and_responses": {
      "1_question": "Qual seu objetivo principal com o PDI?",
      "1_response": "Desenvolvimento de carreira em tecnologia",
      "2_question": "Você já fez PDI antes?",
      "2_response": "Sim, mas não consegui manter"
    },
    "tracking": {
      "utm_campaign": null,
      "utm_source": null,
      "utm_medium": null,
      "utm_content": null,
      "utm_term": null,
      "salesforce_uuid": null
    },
    "source": "API",
    "reschedule_url": "https://calendly.com/reschedule/RESCHEDULE_URL",
    "cancel_url": "https://calendly.com/cancel/CANCEL_URL"
  }
}
```

---

## ⚙️ Configuração Calendly

### **Pré-requisitos**
- ✅ Conta Calendly Pro ativa
- ✅ Pelo menos 1 tipo de evento criado
- ✅ Branding personalizado configurado

### **Passos de Configuração**

#### **1. Acessar Configurações de Webhooks**
1. Logar no Calendly (https://calendly.com)
2. Ir para **Account Settings** → **Apps & Integrations**
3. Selecionar **Webhooks**
4. Clicar em **Add Webhook**

#### **2. Configurar Webhook**
```
Webhook URL: [URL do Zapier Webhook Trigger - será gerada no próximo passo]
Event Types: invitee.created (apenas)
```

#### **3. Testar Webhook**
- Criar um agendamento de teste
- Verificar se o webhook foi disparado no Zapier

---

## 🔧 Configuração Zapier

### **Pré-requisitos**
- ✅ Conta Zapier ativa (plano Starter ou superior)
- ✅ Acesso ao Notion workspace

### **Criar Zap: Calendly → Notion**

#### **1. Trigger: Webhooks by Zapier**
```
App: Webhooks by Zapier
Trigger: Catch Hook
Pick off a Child Key: payload (opcional)
```

**URL do Webhook Gerada:** `https://hooks.zapier.com/hooks/catch/123456/abcdef/`

#### **2. Action: Notion**
```
App: Notion
Action: Create Database Item
Database: [Selecionar database "Sessões PDI"]
```

**Mapeamento de Campos:**
```
Nome Completo: {{payload__invitee__first_name}} {{payload__invitee__last_name}}
Email: {{payload__invitee__email}}
Data da Sessão: {{payload__start_time}}
Tipo de Sessão: {{payload__event_type__name}}
Duração: {{payload__event_type__duration}} minutos
Objetivo Principal: {{payload__questions_and_responses__1_response}}
Experiência Anterior: {{payload__questions_and_responses__2_response}}
Status: Agendado
URL de Reagendamento: {{payload__reschedule_url}}
URL de Cancelamento: {{payload__cancel_url}}
Data de Criação: {{payload__invitee__created_at}}
```

#### **3. Action: Gmail (Confirmação)**
```
App: Gmail
Action: Send Email
To: {{payload__invitee__email}}
Subject: ✅ Confirmação de Agendamento - Sessão PDI
```

**Template do Email:**
```html
Olá {{payload__invitee__first_name}},

Sua sessão de PDI foi agendada com sucesso!

📅 **Data e Horário:** {{payload__start_time}}
⏱️ **Duração:** {{payload__event_type__duration}} minutos
🎯 **Tipo:** {{payload__event_type__name}}

📝 **Seus Objetivos:**
{{payload__questions_and_responses__1_response}}

🔗 **Links Úteis:**
- Reagendar: {{payload__reschedule_url}}
- Cancelar: {{payload__cancel_url}}

Estamos ansiosos para sua sessão!
Equipe Meu PDI
```

---

## 🧪 Testes e Validação

### **Cenários de Teste**

#### **Teste 1: Agendamento Básico**
- ✅ Criar agendamento via Calendly
- ✅ Verificar criação automática no Notion
- ✅ Confirmar envio de email de confirmação

#### **Teste 2: Dados Personalizados**
- ✅ Preencher perguntas customizadas
- ✅ Verificar mapeamento correto no Notion
- ✅ Validar conteúdo do email

#### **Teste 3: Reagendamento**
- ✅ Reagendar sessão existente
- ✅ Verificar atualização no Notion
- ✅ Confirmar novo email enviado

#### **Teste 4: Cancelamento**
- ✅ Cancelar agendamento
- ✅ Verificar atualização de status no Notion
- ✅ Confirmar email de cancelamento (futuro)

---

## 📊 Monitoramento e Logs

### **Zapier Monitoring**
- **Task History:** Verificar execuções bem-sucedidas/falhas
- **Alerts:** Configurar notificações para falhas
- **Logs:** Revisar dados processados

### **Calendly Monitoring**
- **Webhook Logs:** Verificar disparos bem-sucedidos
- **Event History:** Auditar agendamentos criados

### **Notion Monitoring**
- **Database Updates:** Confirmar registros criados
- **Data Integrity:** Validar mapeamento de campos

---

## 🚨 Tratamento de Erros

### **Cenários de Falha**

#### **Falha no Webhook Calendly**
- **Sintomas:** Agendamento criado, mas sem ação no Zapier
- **Solução:** Verificar URL do webhook, testar conectividade
- **Prevenção:** Monitorar status do webhook no Calendly

#### **Falha na Criação Notion**
- **Sintomas:** Webhook disparado, mas registro não criado
- **Solução:** Verificar permissões do Zapier no Notion
- **Prevenção:** Testar conexão Zapier-Notion regularmente

#### **Falha no Email**
- **Sintomas:** Registro criado, mas email não enviado
- **Solução:** Verificar configuração Gmail no Zapier
- **Prevenção:** Usar templates testados

---

## 📈 Métricas de Sucesso

### **KPIs Técnicos**
- **Uptime do Webhook:** 99.9%
- **Tempo de Resposta:** < 5 segundos
- **Taxa de Sucesso:** > 95% dos agendamentos processados

### **KPIs de Negócio**
- **Conversão:** 100% dos agendamentos → registros criados
- **Satisfação:** Feedback positivo dos usuários
- **Automação:** Zero intervenção manual necessária

---

## 🔄 Próximos Passos

### **Após Implementação**
1. ✅ **TASK-003:** Criar templates de email adicionais
2. ⏳ **TASK-004:** Configurar Stripe/PagSeguro
3. ⏳ **TASK-005:** Implementar webhooks de pagamento

### **Otimização Futura**
- Adicionar validações de dados
- Implementar retry logic para falhas
- Criar dashboard de monitoramento
- Automatizar testes de saúde

---

## 📝 Documentação Relacionada

- **ADR-001:** Arquitetura No-Code First
- **TASK-001:** Configurar Calendly Pro
- **Business Baseline:** Visão Estratégica e Modelo de Receita
- **Roadmap:** Fase 1 - No-Code MVP

---

**Última Atualização:** 02 de novembro de 2025
**Responsável:** GitHub Copilot
**Status da Task:** Em andamento - Configuração técnica documentada, pronto para implementação prática