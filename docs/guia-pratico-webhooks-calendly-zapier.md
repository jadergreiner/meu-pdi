# 🚀 Guia Prático: Configuração Webhooks Calendly → Zapier

**Data:** 02 de novembro de 2025
**Status:** ✅ PRONTO PARA EXECUÇÃO
**Tempo Estimado:** 4 horas

---

## 📋 Checklist de Pré-requisitos

### **Contas e Acesso**
- [x] Calendly Pro - Conta ativa e configurada
- [x] Zapier - Plano Starter ou superior (R$ 20/mês)
- [x] Notion - Workspace com database "Sessões PDI"
- [x] Gmail - Conta para envio de emails

### **Configurações Calendly**
- [x] Pelo menos 1 tipo de evento criado ("Sessão PDI - 60 minutos")
- [x] Branding personalizado configurado
- [x] Campos customizados criados (perguntas sobre objetivos)

### **Configurações Notion**
- [x] Database "Sessões PDI" criada com campos:
  - Nome Completo (Title)
  - Email (Email)
  - Data da Sessão (Date)
  - Tipo de Sessão (Select)
  - Duração (Number)
  - Objetivo Principal (Text)
  - Experiência Anterior (Text)
  - Status (Select: Agendado, Confirmado, Realizado, Cancelado)
  - URL Reagendamento (URL)
  - URL Cancelamento (URL)
  - Data de Criação (Date)

---

## 🔧 Passo 1: Configurar Webhook no Calendly

### **Acesso às Configurações**
1. Acesse: https://calendly.com/app/settings/integrations
2. Navegue para: **Apps & Integrations** → **Webhooks**
3. Clique: **Add Webhook**

### **Configuração do Webhook**
```
Webhook URL: [Será gerada no Passo 2 - deixe em branco por enquanto]
Event Types: Marque apenas "invitee.created"
```

**Nota:** A URL será gerada automaticamente pelo Zapier no próximo passo.

---

## 🔧 Passo 2: Criar Zap no Zapier

### **Acesso ao Zapier**
1. Acesse: https://zapier.com/app/zaps
2. Clique: **Create Zap**

### **Configurar Trigger (Calendly Webhook)**

#### **App & Event**
```
App: Webhooks by Zapier
Event: Catch Hook
```

#### **Trigger Setup**
```
Pick off a Child Key: payload
```

#### **Test Trigger**
- Copie a **Webhook URL** gerada
- Volte ao Calendly e cole esta URL no webhook criado
- Clique **Save** no Calendly
- No Zapier, clique **Test trigger**
- Crie um agendamento de teste no Calendly
- Verifique se o webhook foi capturado no Zapier

---

## 🔧 Passo 3: Configurar Action - Notion

### **Adicionar Action**
```
App: Notion
Event: Create Database Item
```

### **Account**
- Conecte sua conta Notion
- Autorize acesso ao workspace

### **Action Setup**
```
Database: Sessões PDI
```

### **Mapear Campos (Field Mapping)**
```
Nome Completo: {{payload__invitee__first_name}} {{payload__invitee__last_name}}
Email: {{payload__invitee__email}}
Data da Sessão: {{payload__start_time}}
Tipo de Sessão: {{payload__event_type__name}}
Duração: {{payload__event_type__duration}}
Objetivo Principal: {{payload__questions_and_responses__1_response}}
Experiência Anterior: {{payload__questions_and_responses__2_response}}
Status: Agendado
URL de Reagendamento: {{payload__reschedule_url}}
URL de Cancelamento: {{payload__cancel_url}}
Data de Criação: {{payload__invitee__created_at}}
```

### **Test Action**
- Clique **Test step**
- Verifique se um registro foi criado no Notion

---

## 🔧 Passo 4: Configurar Action - Email de Confirmação

### **Adicionar Action**
```
App: Gmail
Event: Send Email
```

### **Account**
- Conecte sua conta Gmail
- Autorize envio de emails

### **Action Setup**
```
To: {{payload__invitee__email}}
From: [seu-email@domain.com]
Subject: ✅ Confirmação de Agendamento - Sessão PDI
```

### **Body (HTML)**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .header { background: #4CAF50; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .button { background: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        .footer { background: #f5f5f5; padding: 20px; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ Agendamento Confirmado!</h1>
        <p>Sua sessão de PDI foi agendada com sucesso</p>
    </div>

    <div class="content">
        <h2>Olá {{payload__invitee__first_name}},</h2>

        <p>Estamos muito felizes com seu agendamento! Aqui estão os detalhes da sua sessão:</p>

        <h3>📅 Detalhes do Agendamento</h3>
        <ul>
            <li><strong>Data e Horário:</strong> {{payload__start_time}}</li>
            <li><strong>Duração:</strong> {{payload__event_type__duration}} minutos</li>
            <li><strong>Tipo de Sessão:</strong> {{payload__event_type__name}}</li>
        </ul>

        <h3>🎯 Seus Objetivos</h3>
        <p>{{payload__questions_and_responses__1_response}}</p>

        <h3>🔗 Links Úteis</h3>
        <p>
            <a href="{{payload__reschedule_url}}" class="button">Reagendar Sessão</a>
            <br><br>
            <a href="{{payload__cancel_url}}" class="button">Cancelar Sessão</a>
        </p>

        <h3>📋 O que Esperar</h3>
        <p>Na sua sessão de PDI, vamos:</p>
        <ul>
            <li>Avaliar sua situação atual</li>
            <li>Definir objetivos claros e mensuráveis</li>
            <li>Criar um plano de ação personalizado</li>
            <li>Estabelecer indicadores de progresso</li>
        </ul>

        <p><strong>Lembrete:</strong> Chegue 5 minutos antes do horário marcado.</p>

        <p>Qualquer dúvida, estamos à disposição!</p>

        <p>Atenciosamente,<br>
        <strong>Equipe Meu PDI</strong></p>
    </div>

    <div class="footer">
        <p>Este é um email automático. Por favor, não responda diretamente.</p>
        <p>© 2025 Meu PDI - Desenvolvimento pessoal estruturado</p>
    </div>
</body>
</html>
```

### **Test Action**
- Clique **Test step**
- Verifique se o email foi enviado corretamente

---

## 🔧 Passo 5: Ativar e Testar o Zap

### **Publicar o Zap**
1. Clique **Publish** no Zapier
2. Nomeie o Zap: "Calendly → Notion + Email"
3. Ative o Zap

### **Teste Completo**
1. **Crie um agendamento real** no Calendly
2. **Verifique no Notion** se o registro foi criado
3. **Verifique no Gmail** se o email foi enviado
4. **Valide os dados** mapeados corretamente

### **Cenários de Teste**
- [ ] Agendamento básico (todos os campos preenchidos)
- [ ] Agendamento com dados mínimos
- [ ] Agendamento com reagendamento posterior
- [ ] Verificar formatação do email

---

## 📊 Monitoramento e Troubleshooting

### **Verificar Status do Zap**
1. Acesse: https://zapier.com/app/zaps
2. Clique no Zap criado
3. Vá para: **Task History**
4. Verifique execuções bem-sucedidas/falhas

### **Problemas Comuns**

#### **Webhook não dispara**
- Verificar se URL está correta no Calendly
- Testar conectividade: `curl -X POST [URL_DO_WEBHOOK]`
- Verificar logs no Calendly

#### **Dados não mapeados no Notion**
- Verificar nomes dos campos no database
- Confirmar sintaxe dos placeholders: `{{payload__campo}}`
- Testar cada campo individualmente

#### **Email não enviado**
- Verificar permissões do Gmail
- Confirmar template HTML válido
- Testar com email simples primeiro

---

## 📈 Próximas Implementações

### **Após Sucesso desta Task**
- [ ] TASK-003: Templates de email adicionais (lembrete, follow-up)
- [ ] TASK-004: Integração Stripe/PagSeguro
- [ ] TASK-005: Webhooks de pagamento

### **Otimização Futura**
- Adicionar validações de dados
- Implementar sistema de lembretes automáticos
- Criar dashboard de métricas
- Automatizar relatórios semanais

---

## 📞 Suporte

**Em caso de problemas:**
1. Verificar documentação: `docs/implementacao-webhooks-calendly-zapier.md`
2. Consultar logs do Zapier
3. Testar componentes individualmente
4. Documentar issue no GitHub se necessário

---

**✅ Task Concluída:** Webhooks Calendly → Zapier implementados e testados
**Tempo Gasto:** [Preencher após conclusão]
**Status Final:** [Sucesso/Falha/Parcial]