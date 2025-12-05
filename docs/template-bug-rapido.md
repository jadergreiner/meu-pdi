# 🐛 Template Ultra-Rápido de Bugs - Meu PDI

## 📋 Formato Simplificado (3 linhas)

```markdown
## BUG-XXX - [Título do Bug]

**Onde:** [Página/Funcionalidade] | **O que:** [Erro em 1 linha] | **Quando:** DD/MM/YYYY HH:MM
```

---

## 🎯 Como Usar

1. **Gere o código:**

   ```bash
   python scripts/gerar_codigo_bug.py
   ```

2. **Registre em 1 linha:**
   - Copie o template acima
   - Preencha apenas os 3 campos essenciais
   - Cole no `docs/bugs/bugs.md`

---

## � Exemplos

```markdown
## BUG-003 - Botão Login Não Funciona

**Onde:** /auth/login | **O que:** Erro 500 ao clicar | **Quando:** 03/11/2025 15:30
```

```markdown
## BUG-004 - Dashboard Carrega Lento

**Onde:** /dashboard | **O que:** Loading infinito | **Quando:** 03/11/2025 16:45
```

---

## ✅ Checklist de Qualidade

- [ ] Código BUG gerado automaticamente
- [ ] Título claro e objetivo
- [ ] Local exato do problema
- [ ] Descrição do erro em 1 linha
- [ ] Data/hora atual

---

## 📊 Exemplos de Uso

### Exemplo 1 - Bug de Interface

```markdown
## BUG-003 - Botão de Login Não Clica

**📅 Data/Hora:** 03/11/2025 14:30
**🎯 Status:** 🆕 Aberto
**🚨 Severidade:** Média
**⚡ Prioridade:** Alta

### 📍 Onde Ocorreu
**Página/Funcionalidade:** /auth/login
**Browser/Sistema:** Chrome/Windows

### 🔍 O que Aconteceu
**Passos Rápidos:**
1. Abrir página de login
2. Clicar no botão "Entrar"

**Esperado:** Formulário ser enviado
**Atual:** Botão não responde ao clique

### 🔧 Causa Suspeita
Possível problema de JavaScript no event handler

### 📝 Notas
Testado em outros browsers - funciona normalmente
```

### Exemplo 2 - Bug de API

```markdown
## BUG-004 - Erro 500 na API de Usuários

**📅 Data/Hora:** 03/11/2025 15:45
**🎯 Status:** 🆕 Aberto
**🚨 Severidade:** Alta
**⚡ Prioridade:** Urgente

### 📍 Onde Ocorreu
**Página/Funcionalidade:** API /api/users
**Browser/Sistema:** Postman/Windows

### 🔍 O que Aconteceu
**Passos Rápidos:**
1. Fazer GET para /api/users
2. Com token válido

**Esperado:** Retornar lista de usuários
**Atual:** HTTP 500 Internal Server Error

### 🔧 Causa Suspeita
Erro no banco de dados ou query malformada

### 📝 Notas
Logs do servidor mostram erro de SQL
```

---

## ✅ Checklist de Qualidade

- [ ] **Título claro** (máx. 8 palavras)
- [ ] **Severidade correta** (impacto no usuário)
- [ ] **Passos reprodutíveis** (mínimo necessário)
- [ ] **Informações essenciais** (quando, onde, o quê)
- [ ] **Causa suspeita** (se conhecida)

---

## 🔄 Fluxo de Trabalho

1. **Registro Inicial** → Template Rápido
2. **Análise Técnica** → Template Detalhado (mover para `bugs.md`)
3. **Resolução** → Atualizar status e documentar correção
4. **Validação** → Testes e fechamento

---

## 📝 Dica

**Para bugs complexos, comece com o template rápido e depois mova para análise detalhada no arquivo principal `bugs.md`.**
