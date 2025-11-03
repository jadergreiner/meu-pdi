# 🤖 meu-pdi - Instrucoes Essenciais para Agentes de IA

## 🎯 Visao Geral do Projeto

Plataforma e servico de mentoria para Plano de Desenvolvimento Individual (PDI) personalizado para profissionais de tecnologia. Foco em crescimento de carreira atraves de PDI estrategico + acompanhamento senior.

* **Modelo de Negocio:** Service-First (mentoria) → Platform (automatizada).
* **Publico-Alvo:** Desenvolvedores Plenos/Seniors buscando crescimento estruturado.
* **Metodologia:** PDI Centralizado + Diario de Sessao + Diario de Bordo.

## 🏛️ Padroes Arquiteturais

* **Estrutura Atual:** Foco em documentacao de negocio e planejamento.
    * `business/` (Planos de negocio, financeiros, marketing)
    * `planning/` (Arquitetura tecnica, metodologia mentoria)
    * `tracking/` (Acompanhamento progresso)
* **Plataforma Futura:** Tech Stack: Calendly + Zoom + Notion + Google Workspace (MVP Lean).
* **Persistencia:** Documentacao em Markdown, dados em JSON/planilhas.
* **Multi-tenant:** Isolamento por cliente/mentorando.
* **Contexto de Negocio (Raiz Logica):** A documentacao de negocio principal do projeto e localizada na raiz logica: **`my-projects\projetos\meu-pdi`**. Ao referenciar documentos, o Agente de IA deve priorizar esta estrutura.

---

## ⚡ POLITICA DE OTIMIZACAO DE TOKENS E RATE LIMITS

### SEMPRE Aplicar

#### Limites de Consulta Padrao
* Listar issues/PRs: maximo 20 itens (usar paginacao se usuario solicitar mais)
* Buscar arquivos: priorizar top 5 mais relevantes
* Mostrar codigo: limite inicial de 100 linhas (oferecer expandir se necessario)
* Listar commits: maximo 15 commits mais recentes
* Discussoes/comentarios: maximo 10 itens

#### Hierarquia de Busca (Prioridade de Eficiencia)
1. **Primeiro:** Verificar contexto da conversa atual
2. **Segundo:** lexical-code-search (busca exata, menor custo)
3. **Terceiro:** semantic-code-search (busca contextual, maior custo)
4. **Ultimo recurso:** Analise profunda com multiplas chamadas

#### Consolidacao de Requisicoes
* Agrupar multiplas queries relacionadas em UMA unica chamada
* Usar filtros nativos da API GitHub (labels, state, author, date range)
* Preferir endpoints agregados vs multiplas chamadas individuais
* Exemplo: `state:open label:bug author:jadergreiner` vs 3 chamadas separadas

#### Reutilizacao de Contexto (Cache)
* SEMPRE verificar se informacao ja foi buscada na conversa atual
* Referenciar dados anteriores: "Conforme arquivo mencionado anteriormente..."
* Armazenar metadados de repositorio consultados (estrutura, branches, arquivos principais)
* NAO refazer buscas identicas em intervalo menor que 5 minutos

### NUNCA Fazer

* Buscar arquivos inteiros sem necessidade especifica
* Listar TODOS os issues/PRs sem filtro de status, label ou data
* Fazer lexical-code-search E semantic-code-search para mesma query
* Chamar githubread se dados ja estao disponiveis no contexto via mcp_github
* Expandir contexto desnecessariamente com informacoes nao solicitadas
* Buscar historico completo de commits (sem limite de data)

### PERGUNTAR ao Usuario Antes De

* Operacoes que requerem mais de 3 chamadas de API
* Buscas em repositorios com mais de 1000 arquivos sem escopo definido
* Analises que podem ser feitas localmente (grep, find, git log)
* Listar mais de 50 itens de qualquer tipo
* Buscas sem filtro temporal em repos com mais de 2 anos

### Estrategia de Busca por Tipo

#### Para Codigo (Funcoes, Classes, Implementacoes)
```
1. Usuario pergunta: "Onde esta a funcao authenticateUser?"
2. Acao: lexical-code-search com symbol:authenticateUser
3. Se nao encontrar: semantic-code-search "funcao de autenticacao de usuario"
```

#### Para Conceitos (Como funciona X, Explicar Y)
```
1. Usuario pergunta: "Como funciona a autenticacao?"
2. Acao: semantic-code-search "como funciona a autenticacao"
3. Limitar a top 5 resultados mais relevantes
```

#### Para Arquivos Especificos
```
1. Usuario pergunta: "Mostre o arquivo auth.py"
2. Acao: githubread com path exato
3. Se path desconhecido: lexical-code-search path:auth.py
```

#### Para Issues/PRs
```
1. Sempre usar filtros: state, label, author, created/updated date
2. Exemplo: "issues abertos com label bug dos ultimos 30 dias"
3. Query: state:open label:bug created:>2025-10-03
```

### Metricas de Eficiencia (Auto-Avaliacao)

A cada interacao, o agente deve avaliar:
* Numero de tool calls realizados (meta: maximo 2 por resposta simples)
* Dados reutilizados vs buscados (meta: 60% reutilizacao em conversas longas)
* Precisao da resposta (informacao solicitada vs informacao entregue)

---

## 🚧 Fluxo de Desenvolvimento e Qualidade

### Processo Lean MVP

1.  **OBRIGATORIO:** Validar hipoteses de negocio antes de desenvolvimento.
2.  Implementar com foco em ROI e metricas de sucesso.
3.  **OBRIGATORIO**: Atualizar documentacao a cada milestone.
4.  Criar ADRs em `docs/adrs/` para decisoes estrategicas.
5.  **Testes Alpha/Beta:** Validar com usuarios reais.

### 🚪 Gate de Inicio (EPIC/SPIN/SMART)

**Antes de iniciar qualquer desenvolvimento para uma nova Historia do Usuario (US):**

1.  **Apresentar Arvore Agil:** EPIC > FEATURE > HISTORIA (US) > TASKS (Propostas).
2.  **Validacao SPIN:** Refinar a Historia validando alinhamento com SPIN Selling (Situacao, Problema, Implicacao, Necessidade).
3.  **Refinamento SMART:** Apos aprovacao da Historia, aplicar SMART em cada Task tecnica.

**Objetivo:** Garantir valor de negocio validado e tasks especificas, mensuraveleis e alcancaveis.

**Finalizar refinamento:** Apos aprovacao, atualizar documentacoes com SPIN e SMART. Registrar nome do aprovador e data/horario da aprovacao.

### 📋 PADRAO OBRIGATORIO DE DOCUMENTACAO

**A CADA ENTREGA DE HISTORIA DO USUARIO, SEMPRE ATUALIZAR:**

* `docs/diario-projeto.md` - Progresso diario e marcos
* `docs/gestao-agil/backlog.md` - Status de features e user stories
* `README.md` - Instalacao, Uso, Credenciais, funcionalidades novas
* `docs/01-arquitetura.md` - Mudancas na estrutura ou componentes
* `docs/04-requisitos.md` - Novos requisitos ou modificacoes
* `ADRs relevantes` - Decisoes arquiteturais importantes
* `docs/05-data-lineage-mapping.md` - Fluxo de dados
* `C:\repo\projetos\my-projects\projetos\meu-pdi\**` - Documentacao de negocio
* `docs/02-fluxos-administrador` - Rotinas e fluxos do administrador
* `docs/07-fluxos-aluno` - Rotinas e fluxos do aluno
* `docs/08-fluxos-mentor` - Rotinas e fluxos do mentor

---

## 🚫 PADRAO CRITICO DE COMMITS (ALERTA!)

**NUNCA usar caracteres especiais, acentuacao ou emojis em mensagens de commit.**

* **Encoding:** Sempre ASCII puro nos commits.
* **Acentos:** Remover todos (á→a, ê→e, ç→c, ã→a).
* **Emojis/Especiais:** Proibidos (~, ^, ´, `, etc.).

### Exemplo:
* ❌ **ERRADO**: `docs: criar ADRs obrigatórias para decisões técnicas`
* ✅ **CORRETO**: `docs: criar ADRs obrigatorias para decisoes tecnicas`

### Fluxo Git
* Branches `feature/*` a partir de `develop`.
* Merge para `develop` apos testes passarem.
* Branch `release` para pacotes finais → `main`.
* **Commit final SEMPRE inclui atualizacoes de documentacao.**

---

## 🧪 Padroes de Codigo e Teste

### Padroes de Teste

* **TDD:** Adote TDD como pratica padrao.
* **Testes Unitarios:** Nomes verbosos em portugues. Estrutura dado_quando_entao.
* **Testes E2E:** Playwright para fluxos de UI.
* **Cobertura:** `pytest --cov=src tests/`

### Convencoes de Codigo

* **Rastreabilidade:** `# TASK-XXX: Descricao breve` em todo codigo novo/alterado.
* **Modelos:** Pydantic com restricoes `Field()` e validacao `EmailStr`.
* **Rotas:** Dados de formulario com parametros `Form(...)`, respostas HTML.
* **Nomenclatura:** Portugues (Testes, Variaveis, Funcoes, Classes) e Padrao (APIs, Frameworks).
* **Qualidade:** Todo codigo Python deve seguir PEP8 e ser validado por lint.

---

## 🧩 Organizacao de Trabalho e Agil

### Hierarquia Agil

| Nivel Hierarquico | Foco Principal | Padrao Aplicado | Exemplo de Foco |
| :---: | :--- | :--- | :--- |
| **1. Epico** | Objetivo Estrategico | Alto Nivel | Direcao de meses/trimestres |
| **2. Feature** | Funcionalidade Completa | Tatico | Quebra o Epico em partes tangiveis |
| **3. Historia** | Valor para o Usuario | SPIN Selling | Implicacao do Problema e Necessidade |
| **4. Tarefa** | Passos Tecnicos | Modelo SMART | Clareza e Executabilidade Tecnica |

### Processo de Refinamento de Tasks (Gate de Inicio)

**Antes de iniciar uma nova task, garantir aplicacao do modelo SMART:**

* **Requisitos Funcionais e Nao-Funcionais**
* **Criterios de Aceitacao**
* **Dependencias**
* **Estimativa de Esforco**
* **Testes Necessarios**
* **Impacto no Sistema e Riscos**
* **Documentacao Necessaria**

> 💡 **Principio de Valor (SPIN):** Garantir alinhamento com SPIN, foco em Implicacao e Necessidade de Solucao.

> 🌟 **Padrao SMART:** Tasks devem ser Especificas, Mensuraveis, Alcancaveis, Relevantes e Temporais.

* **Premissa:** Nada se desenvolve sem registro em `docs/gestao-agil/backlog.md` e aprovacao.

### 📋 Principios de Decisao para Backlog

**Ao avaliar e priorizar itens do backlog:**

#### Conceitos Aplicados

- **YAGNI** - Nao implementar funcionalidades desnecessarias. Focar no essencial.
- **KISS** - Manter solucoes simples. Evitar complexidade.
- **Incremental Delivery** - Entregar valor em incrementos pequenos para feedback rapido.
- **Data-Driven Design** - Decisoes baseadas em dados, nao suposicoes.

#### Exemplos de Mercado

- **Nubank:** Comecou simples, adicionou Ultravioleta apos validacao com milhoes de usuarios.
- **Inter:** Lancou com contas simples, expandiu para Inter Black aos 5M clientes.
- **C6 Bank:** Nasceu com categorizacao por parceria com Mastercard.

**Aplicacao Pratica:** Questionar todo item do backlog. Priorizar aprendizado e ROI com minimo esforco.

---

## 🗃️ Padrao para ADRs

* **Finalidade:** Documentar decisoes arquiteturais significativas.
* **Formato:** Template Padrao de ADR.
* **Regras:**
    * Numeracao Sequencial: `ADR-XXX`
    * Localizacao: `docs/adrs/`
    * Status: Sempre definido (Proposto, Aprovado, Superseded)
* **Gatilhos:** Mudancas arquiteturais, escolha de tecnologias, decisoes de design impactantes.

---

## ⚙️ Arquivos e Comandos Principais

* **Executar Servidor:** `uvicorn src.main:app --reload`
* **Executar Testes Unitarios:** `pytest tests/ -v`
* **Executar Testes E2E:** `python run_e2e_tests.py`
* **Instalar Dependencias:** `pip install -r requirements.txt`

---

## 📋 Checklist Final para Agentes (Prioridades)

* **Otimizacao de Tokens:** SEMPRE verificar contexto antes de buscar, limitar resultados, consolidar chamadas.
* **Gate de Inicio Obrigatorio:** Apresentar arvore agil e buscar aprovacao SPIN/SMART antes de codificacao.
* **Foco no Negocio:** Fonte de verdade em `C:\repo\projetos\my-projects\projetos\meu-pdi\**`
* **TDD e a Lei:** Sempre inicie escrevendo testes unitarios.
* **Rastreabilidade:** Use `# TASK-XXX` em todo codigo novo.
* **Compromisso Critico:** NUNCA use acentos, caracteres especiais ou emojis em commits (ASCII puro).
* **Documentacao:** Atualize Diario, Backlog e Docs Tecnicas a cada entrega.

---

## 🎯 Template de Prompt Otimizado para Usuario

**Para obter melhores resultados e evitar rate limits, estruture suas perguntas assim:**

```
Contexto: [especifico e conciso]
Repositorio: jadergreiner/meu-pdi
Objetivo: [unico e claro]
Limite: [numero de resultados desejado]
Formato: [resumido/detalhado/codigo]
```

**Exemplo Bom (Otimizado):**
```
Contexto: Implementando autenticacao JWT
Repositorio: jadergreiner/meu-pdi
Objetivo: Encontrar funcao que valida token
Limite: Apenas funcao principal
Formato: Codigo com explicacao breve
```

```
Contexto: Realizando testes funcionais navegando no portal do aluno
Repositorio: jadergreiner/meu-pdi
Objetivo: Testar a experiencia do aluno e testar funcoes e cliques
Limite: Apenas funcao principal
Formato: Orientações de acesso e jornada de testes
```

```
Contexto: Resolver erro de Credenciais inválidas. Tente novamente. ao logar no portal do aluno como teste
Repositorio: jadergreiner/meu-pdi
Objetivo: Resolver os bugs
Limite: Apenas funcao principal
Formato: Apenas trechos do codigo alterado
```

```
Contexto: Estruturar registros de Bugs
Repositorio: jadergreiner/meu-pdi
Objetivo: Manter um padrão da documentação. Gerar um codigo sequencial e data/hora do registro da ocorrencia
Limite: Apenas funcao principal
Formato: Descricao breve
```

```
Contexto: Gerar template padrao de abertura de Bugs
Repositorio: jadergreiner/meu-pdi
Objetivo: Registrar BUGs de forma simplificada
Limite: Apenas dados essenciais
Formato: Descricao breve
```

```
Contexto: Atualizar arquitetura alvo da aplicacão
Repositorio: jadergreiner/meu-pdi
Objetivo: Atualizar as documentacoes da arquitetura. Criar um documento unico de arquitetura. Ajustar o backlog contemplando a nova arquitetura. Ajustar o backlog para refatorar o que já está pronto. Nova arquitetura: {
                                                                                        Front-End: Angular,
                                                                                        Autenticação: PyJWT (focado em JWT/JWS) ou Authlib (suíte completa JOSE/OAuth)
                                                                                    }
Limite: Apenas dados essenciais
Formato: Descrição detalhada e ADRs

```
Contexto: Reorganizar o backlog
Repositorio: jadergreiner/meu-pdi
Objetivo: Com novas decisões de arquitetura, deve ser revisado o backlog e as prioridades de desenvolvimento
Limite: Apenas documentos relacionados
Formato: Descricao detalhada e analise geral do projeto
```

**Exemplo Ruim (Evitar):**
```
Me fale tudo sobre autenticacao, liste todos os arquivos,
mostre todos os commits, explique toda a estrutura e crie 5 issues
```

### Dicas para Usuarios

* **Seja Especifico:** Pergunte sobre 1 coisa por vez
* **Use Filtros:** "ultimos 30 dias", "apenas label:bug", "top 5"
* **Referencie Contexto:** "No arquivo anterior", "Na funcao mencionada"
* **Limite Escopo:** "apenas na pasta src/auth/", "somente arquivos Python"
* **Timing:** Aguarde 3-5 segundos entre perguntas complexas

---

**Versao:** 2.0 - Otimizada para Tokens e Rate Limits
**Data:** 2025-11-03
**Aprovador:** jadergreiner