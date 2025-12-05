# 🚀 Guia de Validação Local - Portal do Aluno MVP

**Data:** 03/11/2025
**Versão:** 1.0.0
**Status:** ✅ Pronto para Validação

---

## 🎯 Objetivo

Este guia fornece instruções passo a passo para configurar e executar localmente o **Portal do Aluno MVP** do projeto Meu PDI, permitindo validação completa das funcionalidades implementadas.

## 📋 Pré-requisitos do Sistema

### 🔧 Requisitos Técnicos

- **Python:** 3.8 ou superior
- **Node.js:** 18.0 ou superior
- **Git:** Para controle de versão
- **Sistema Operacional:** Windows 10+, macOS 10.15+, ou Linux




### 📦 Dependências de Sistema

- **Windows:** PowerShell ou Command Prompt
- **macOS/Linux:** Terminal bash/zsh
- **Conexão Internet:** Para download de dependências




---

## 📁 Estrutura do Projeto

```
meu-pdi/
├── src/
│   ├── backend/          # API FastAPI
│   └── frontend/         # Aplicação Next.js
├── tests/                # Testes automatizados
├── scripts/              # Scripts de automação
├── requirements.txt      # Dependências Python
└── docs/                 # Documentação
```

---

## ⚡ Instalação e Configuração Rápida

### Passo 1: Clonagem do Repositório

```bash

# Clone o repositório

git clone https://github.com/jadergreiner/meu-pdi.git
cd meu-pdi

# Verificar branch atual

git branch

# Deve estar em: feature/US-U001-auth-portal-aluno

```

### Passo 2: Configuração do Ambiente Python

```bash

# Instalar dependências do backend

pip install -r requirements.txt

# Instalar dependências de teste (opcional, para desenvolvimento)

pip install -r requirements-test.txt

# Verificar instalação

python --version
pip list | grep -E "(fastapi|uvicorn|pydantic)"
```

### Passo 3: Configuração do Ambiente Node.js

```bash

# Navegar para o diretório do frontend

cd src/frontend

# Instalar dependências

npm install

# Verificar instalação

node --version
npm --version
npm list next react
```

---

## 🚀 Execução dos Servidores

### Método 1: Script Automático (Recomendado)

```bash

# Do diretório raiz do projeto

python scripts/start_test_servers.py
```

**O que o script faz:**

- ✅ Inicia servidor backend (FastAPI) na porta 8000
- ✅ Inicia servidor frontend (Next.js) na porta 3000
- ✅ Aguarda inicialização completa
- ✅ Fornece URLs de acesso




### Método 2: Execução Manual

#### Terminal 1 - Backend (FastAPI)

```bash

# Do diretório raiz

cd src/backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

#### Terminal 2 - Frontend (Next.js)

```bash

# Do diretório raiz

cd src/frontend
npm run dev
```

---

## 🔍 Validação das Funcionalidades

### ✅ Checklist de Validação

#### 1. **Servidores Online**

- [ ] Backend responde em: http://127.0.0.1:8000
- [ ] Frontend responde em: http://127.0.0.1:3000
- [ ] API docs disponível em: http://127.0.0.1:8000/docs




#### 2. **Autenticação - TASK-T001 & TASK-T002**

- [ ] Página de cadastro acessível
- [ ] Validação de campos funcionais
- [ ] Email de validação enviado (simulado)
- [ ] Confirmação de cadastro bem-sucedida




#### 3. **Login - TASK-T003**

- [ ] Página de login acessível
- [ ] Autenticação com credenciais válidas
- [ ] Redirecionamento para dashboard
- [ ] Proteção de rotas funcionais




#### 4. **Recuperação de Senha - TASK-T004**

- [ ] Link "Esqueci minha senha" funcional
- [ ] Email de recuperação enviado
- [ ] Reset de senha bem-sucedido




#### 5. **Dashboard - TASK-T005, TASK-T006, TASK-T007**

- [ ] Perfil do usuário exibido corretamente
- [ ] Visão geral do PDI funcional
- [ ] Próximos passos interativos
- [ ] Interface responsiva (mobile/desktop)




---

## 🧪 Execução de Testes

### Testes Unitários (Backend)

```bash

# Do diretório raiz

pytest tests/ -v

# Com cobertura

pytest tests/ --cov=src/backend --cov-report=html
```

**Testes esperados:**

- ✅ `test_auth.py` - Autenticação e autorização
- ✅ `test_email_validation.py` - Validação de email
- ✅ `test_login.py` - Sistema de login
- ✅ `test_password_reset.py` - Recuperação de senha
- ✅ `test_profile.py` - Perfil do usuário




### Testes E2E (Frontend)

```bash

# Do diretório frontend

cd src/frontend
npm run test:e2e  # Se configurado
```

---

## 🔧 Comandos Úteis para Desenvolvimento

### Backend (FastAPI)

```bash

# Executar apenas backend

cd src/backend
uvicorn main:app --reload

# Ver documentação da API
# Acesse: http://127.0.0.1:8000/docs

# Executar testes específicos

pytest tests/test_auth.py -v
```

### Frontend (Next.js)

```bash

# Executar apenas frontend

cd src/frontend
npm run dev

# Build de produção

npm run build

# Verificar tipos TypeScript

npm run type-check

# Lint do código

npm run lint
```

### Desenvolvimento Geral

```bash

# Ver status do Git

git status

# Ver logs recentes

git log --oneline -10

# Executar linting geral

python validate_markdown.py
```

---

## 🚨 Solução de Problemas

### Problema: Porta já em uso

```bash

# Windows - Verificar processos

netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Matar processo (substitua PID)

taskkill /PID <PID> /F
```

### Problema: Dependências não instaladas

```bash

# Reinstalar dependências Python

pip install -r requirements.txt --force-reinstall

# Limpar cache Node.js

cd src/frontend
rm -rf node_modules package-lock.json
npm install
```

### Problema: Erro de CORS

- Verificar se ambos os servidores estão rodando
- Verificar configurações de CORS no backend
- Limpar cache do navegador




### Problema: Testes falhando

```bash

# Executar testes com mais detalhes

pytest tests/ -v -s

# Executar teste específico

pytest tests/test_auth.py::test_register_user -v
```

---

## 📊 Métricas de Validação

### Performance Esperada

- **Tempo de inicialização:** < 30 segundos
- **Tempo de resposta da API:** < 500ms
- **Tempo de carregamento da página:** < 2 segundos
- **Taxa de sucesso dos testes:** > 95%




### Funcionalidades Críticas

- ✅ Cadastro de usuário (TASK-T001)
- ✅ Validação de email (TASK-T002)
- ✅ Sistema de login (TASK-T003)
- ✅ Recuperação de senha (TASK-T004)
- ✅ Perfil do usuário (TASK-T005)
- ✅ PDI Overview (TASK-T006)
- ✅ Próximos passos (TASK-T007)




---

## 📞 Suporte e Contato

### Documentação Relacionada

- `docs/diario-projeto.md` - Progresso diário
- `docs/gate-qualidade-portal-aluno.md` - Especificações técnicas
- `planning/backlog.md` - Backlog completo




### Em caso de problemas

1. Verificar logs dos servidores
2. Consultar documentação específica da task
3. Verificar issues no repositório GitHub
4. Contatar equipe de desenvolvimento

---

## ✅ Checklist Final de Validação

- [ ] Ambiente configurado corretamente
- [ ] Servidores iniciados sem erros
- [ ] Todas as funcionalidades testadas
- [ ] Testes automatizados passando
- [ ] Performance dentro dos parâmetros
- [ ] Documentação atualizada com feedback




**Status da Validação:** ___ / ___

**Responsável:** ____________________

**Data:** ____/____/____

---

*Guia criado para facilitar a validação local do Portal do Aluno MVP. Última atualização: 03/11/2025*
