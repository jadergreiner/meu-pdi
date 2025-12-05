# 🚀 Guia de Configuração: Stripe/PagSeguro para Meu PDI

**Data:** 03 de novembro de 2025
**Status:** ✅ PRONTO PARA EXECUÇÃO
**Tempo Estimado:** 4 horas
**TASK-004:** Configurar Conta Stripe/PagSeguro

---

## 📋 Pré-requisitos

### **Documentação Necessária**
- [ ] CNPJ da empresa (obrigatório para conta comercial)
- [ ] Comprovante de endereço da empresa
- [ ] Documento de identidade do responsável
- [ ] Comprovante de faturamento (opcional, acelera aprovação)

### **Informações da Empresa**
- Razão Social: Meu PDI Consultoria Ltda
- CNPJ: [Inserir CNPJ válido]
- Endereço: [Endereço comercial]
- Responsável: [Nome do responsável]
- Email: contato@meupdi.com
- Telefone: [Telefone comercial]

---

## 💳 **OPÇÃO 1: STRIPE (Recomendado para Internacional)**

### **Passo 1: Criar Conta Stripe**
1. Acesse: https://stripe.com/br
2. Clique: **Começar Agora** → **Criar Conta**
3. Preencha dados pessoais do responsável
4. Selecione: **Empresa** (não individual)
5. Informe dados da empresa (CNPJ, razão social, etc.)

### **Passo 2: Verificação da Conta**
1. Faça upload dos documentos:
   - RG/CPF do responsável
   - CNPJ da empresa
   - Comprovante de endereço
2. Aguarde aprovação (2-5 dias úteis)
3. Ative 2FA na conta

### **Passo 3: Configurar Produtos**
1. No Dashboard → **Produtos**
2. Criar produto: "Sessão PDI Individual"
   - Preço: R$ 150,00
   - Tipo: Serviço
   - Descrição: "Sessão individual de mentoria PDI (60 min)"

3. Criar produto: "Pacote PDI 5 Sessões"
   - Preço: R$ 650,00
   - Tipo: Serviço
   - Descrição: "Pacote com 5 sessões de mentoria PDI"

### **Passo 4: Configurar Métodos de Pagamento**
1. **PIX:** Ativar automaticamente (padrão Brasil)
2. **Cartão de Crédito:** Ativar Visa, Mastercard, etc.
3. **Boleto:** Opcional para pagamentos recorrentes

### **Passo 5: Configurar Webhooks**
1. No Dashboard → **Desenvolvedores** → **Webhooks**
2. Adicionar endpoint: [URL do seu servidor]/webhooks/stripe
3. Eventos a escutar:
   - `checkout.session.completed`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.created`

### **Passo 6: Chaves de API**
1. No Dashboard → **Desenvolvedores** → **Chaves de API**
2. Copiar:
   - **Publishable Key** (pk_test_... ou pk_live_...)
   - **Secret Key** (sk_test_... ou sk_live_...)
3. **IMPORTANTE:** Nunca expor Secret Key no frontend!

---

## 💰 **OPÇÃO 2: PAGSEGURO (Recomendado para Brasil)**

### **Passo 1: Criar Conta PagSeguro**
1. Acesse: https://pagseguro.uol.com.br/
2. Clique: **Criar Conta** → **Conta Empresarial**
3. Preencha dados da empresa (CNPJ obrigatório)
4. Selecione segmento: **Consultoria/Educação**

### **Passo 2: Verificação e Ativação**
1. Faça upload da documentação:
   - Contrato social
   - RG/CPF dos sócios
   - Comprovante de endereço
2. Aguarde análise (3-7 dias úteis)
3. Configure senha e 2FA

### **Passo 3: Configurar Produtos/Serviços**
1. No painel → **Produtos e Serviços**
2. Criar produto: "Sessão PDI Individual"
   - Valor: R$ 150,00
   - Tipo: Serviço
   - Descrição detalhada

3. Criar produto: "Pacote PDI 5 Sessões"
   - Valor: R$ 650,00
   - Tipo: Pacote
   - Descrição: "5 sessões de mentoria PDI"

### **Passo 4: Configurar Formas de Pagamento**
1. **PIX:** Ativar (gratuito, instantâneo)
2. **Cartão:** Ativar débito e crédito
3. **Boleto:** Ativar para pagamentos à vista

### **Passo 5: Configurar Notificações**
1. No painel → **Integrações** → **Notificações**
2. Configurar URL de notificação: [seu-servidor]/webhooks/pagseguro
3. Tipos de notificação:
   - Pagamento aprovado
   - Pagamento cancelado
   - Estorno
   - Chargeback

### **Passo 6: Credenciais de Integração**
1. No painel → **Integrações** → **Credenciais**
2. Copiar:
   - **Email da conta**
   - **Token de produção**
3. Configurar permissões para API

---

## 🔧 **INTEGRAÇÃO TÉCNICA**

### **Para Stripe**
```javascript
// Instalar: npm install stripe
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Criar sessão de checkout
const session = await stripe.checkout.sessions.create({
  payment_method_types: ['card', 'pix'],
  line_items: [{
    price_data: {
      currency: 'brl',
      product_data: { name: 'Sessão PDI Individual' },
      unit_amount: 15000, // R$ 150,00 em centavos
    },
    quantity: 1,
  }],
  mode: 'payment',
  success_url: 'https://meupdi.com/sucesso',
  cancel_url: 'https://meupdi.com/cancelar',
});
```

### **Para PagSeguro**
```javascript
// Instalar: npm install pagseguro-node
const pagseguro = require('pagseguro-node');

// Configurar credenciais
pagseguro.configure({
  email: process.env.PAGSEGURO_EMAIL,
  token: process.env.PAGSEGURO_TOKEN,
  mode: 'production' // ou 'sandbox'
});

// Criar pagamento
const payment = {
  items: [{
    id: '1',
    description: 'Sessão PDI Individual',
    amount: '150.00',
    quantity: '1'
  }],
  sender: {
    name: customerName,
    email: customerEmail
  },
  redirectURL: 'https://meupdi.com/sucesso'
};
```

---

## 📊 **TESTES RECOMENDADOS**

### **Testes em Ambiente de Desenvolvimento**
1. **Stripe Test Mode:**
   - Usar cartões de teste: 4242 4242 4242 4242
   - PIX: Usar QR code de teste

2. **PagSeguro Sandbox:**
   - Conta separada para testes
   - Valores fictícios

### **Cenários de Teste**
- [ ] Pagamento aprovado (PIX)
- [ ] Pagamento aprovado (cartão)
- [ ] Pagamento rejeitado (saldo insuficiente)
- [ ] Estorno solicitado
- [ ] Webhook recebido corretamente

---

## ⚖️ **COMPARAÇÃO: STRIPE vs PAGSEGURO**

| Aspecto | Stripe | PagSeguro |
|---------|--------|-----------|
| **Taxas** | 3.4% + R$ 0.49 (crédito)<br>1.5% (PIX) | 4.99% (crédito)<br>0.99% (PIX) |
| **Setup** | 2-5 dias | 3-7 dias |
| **Internacional** | Excelente | Limitado |
| **API** | Moderna, bem documentada | Boa, mas mais antiga |
| **Suporte** | Em inglês | Em português |
| **Recomendação** | Para crescimento internacional | Para foco Brasil |

---

## 🚀 **IMPLEMENTAÇÃO NO SISTEMA**

### **Variáveis de Ambiente**
```bash
# Stripe
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# PagSeguro
PAGSEGURO_EMAIL=contato@meupdi.com
PAGSEGURO_TOKEN=...
PAGSEGURO_APP_ID=...
PAGSEGURO_APP_KEY=...
```

### **Fluxo de Pagamento**
1. Usuário seleciona produto no portal
2. Sistema cria sessão de checkout
3. Usuário é redirecionado para gateway
4. Após pagamento, webhook confirma
5. Sistema atualiza status e envia confirmação

---

## 📋 **CHECKLIST FINAL**

### **Configuração Conta**
- [ ] Conta criada e verificada
- [ ] Documentação aprovada
- [ ] 2FA ativado

### **Produtos Configurados**
- [ ] Sessão individual: R$ 150,00
- [ ] Pacote 5 sessões: R$ 650,00
- [ ] Descrições detalhadas

### **Pagamentos Ativados**
- [ ] PIX funcional
- [ ] Cartão de crédito
- [ ] Cartão de débito

### **Integração Técnica**
- [ ] Webhooks configurados
- [ ] Credenciais armazenadas com segurança
- [ ] Testes realizados com sucesso

### **Conformidade**
- [ ] LGPD compliance
- [ ] Política de privacidade
- [ ] Termos de uso

---

## 🎯 **PRÓXIMOS PASSOS APÓS CONFIGURAÇÃO**

1. **TASK-005:** Implementar webhooks de pagamento no backend
2. **TASK-006:** Sistema de recibos automáticos
3. Testes de usuário com pagamentos reais
4. Monitoramento de conversão e abandono

---

**Status:** Guia completo criado
**Responsável:** Sistema de Documentação Automatizada
**Próxima Revisão:** Após implementação e testes