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

```markdown
### LA-[ID]: REGISTRAR QUAL AGENT DE IA TOMOU A DECISÃO
- **Problema:** Alternamos a escolha do Agent conforme o tipo de Prompt. Quem é o Agent mais assertivo e com as melhores propostas em nosso projeto.
- **Solução Proposta:** Ter uma forma centralizada do uso de Agents, contextos de tomada de decisão e por que o Agent foi usado naquele contexto. Padronizar na saída dos prompts gerado por [Agent]
- Agent entenda como o modelo, exemplo: GPT-4-1, Gemini, Claude Sonnet 4
- **Status:** [Proposta | Aprovada | Rejeitada]
```

```
### LA-[ID]: MD032/blanks-around-lists: Lists should be surrounded by blank linesmarkdownlintMD032
- **Problema:** DOCS com erro de formatacao
- **Solução Proposta:** Revisar e padronizar DOCS automaticamente nos commits e/ou Push
```


```markdown
### LA-[ID]: COMMITS E TEXTOS NO TERMINAL
- **Problema:** Textos quebrados no terminal e no Git.
- **Solução Proposta:** Não utilizar acentos e símbolos.
Exemplo:
# Code Review - Guia e Checklist

## ðŸ“‹ VisÃ£o Geral

Este documento estabelece padrÃµes e procedimentos para revisÃ£o de cÃ³digo no projeto Hub Financeiro Inteligente.

## ðŸŽ¯ Objetivos do Code Review

1. **Qualidade:** Garantir cÃ³digo limpo, manutenÃ­vel e testÃ¡vel
2. **SeguranÃ§a:** Identificar vulnerabilidades e falhas de seguranÃ§a- 

**Status:** [Proposta | Aprovada | Rejeitada]
```


```markdown
### LA-[ID]: REGISTRAR POR QUE FOI SELECIONADO ESTE AGENTE
- **Problema:** Alternamos a escolha do Agent conforme o tipo de Prompt. Quem é o Agent mais assertivo e com as melhores propostas em nosso projeto.
- **Solução Proposta:** Temos o log do Agent que processou o prompt. Complementar com a motivação que levou a selecionar este Agent como o ideal para o Prompt
```
Agent: Claude Sonnet 3.5
Tempo: ~35 minutos
Operações: 12 tool calls
Data: 2025-11-04

```


```
### LA-[ID]: COMMITS SEMPRE EM PORTUGUES
- **Problema:** Os Commits estão em Inglês
- **Solução Proposta:** Gerar TODOS os commits em Portugues
```


```
Contexto: Executar a proxima task priorizada
Objetivo: Executar a task e atualizar as documentacoes relacionadas e/ou impactadas
Limite: Apenas funcao principal e essenciais para o funcionamento
Formato: INICIO: Mostra a Task que sera executada FIM: Relatório do processo
```


************* NOVO PROMPT ***********
```
Contexto: Executar a proxima feature priorizada
Repositorio: jadergreiner/hub-financeiro-inteligente
Objetivo: Executar a feature e atualizar as documentacoes relacionadas e/ou impactadas
Limite: Apenas funcao principal e essenciais para o funcionamento
Formato: INICIO: Mostra a Feature que sera executada FIM: Relatório do processo
```

```
Contexto: Registrar um diário de lições aprendidas
Repositorio: jadergreiner//hub-financeiro-inteligente
CONCEITOS: LA > Lição Aprendida
COMITE: C:\repo\projetos\hub-financeiro-inteligente\docs\governanca\COMITE-DECISAO.md
Objetivo: No decorrer do projeto encontramos oportunidades para melhorar o projeto. Vamos registrar as lições e enviar ao comitê para avaliar o que deve ser implementado.
Limite: Apenas função principal e essenciais para o funcionamento
Formato: [
INICIO: Captura a LA (Lição aprendida)
DURANTE: Assume o papel de diretor técnico e abre uma discussão para entender os pontos com o Tech Lead
DURANTE: Toma uma das ACOES> APROVA a aplicação imediatamente. DESCARTA imediatamente. ENVIA para analise do comitê.
FIM: Devolve um Layout de como deve ser registrada uma LA
```


```

Papel: Assuma o papel de Especialista de Investimento Internacional especializado em Forex

Contexto: Avaliar se a oportunidade atende nossos criterios

Objetivo: Ao passar um ativo, realizar a analise de mercado e potencial de retorno com a operação no horizonte de dias/semanas

Limite: Apenas funcao principal e essenciais para o funcionamento

Formato: [

INICIO: Mostra dados economicos atuais 

DURANTE: Corelaçao do ativo com outros Ativos

DURANTE: Noticias e eventos que impactam

FIM: Parecer sobre a oportunidade. APROVAR/DESCARTAR e niveis de preço para entrada e Take Profit
QUANDO: Identificar outra oportunidade a partir da correlação RECOMENDAR

ATIVO: COMPRA DE USDCHF

```



```

Papel: Assuma o papel de Especialista de operações de Trade no Mercado Brasileiro

Contexto: Avaliar as melhores oportunidades de operação

Objetivo: Realizar a analise de mercado e potencial de retorno com a operação no horizonte de minutos/hora

Limite: Apenas funcao principal e essenciais para o funcionamento

Formato: [

INICIO: Mostra dados economicos atuais 

DURANTE: Corelaçao do ativo com outros Ativos

DURANTE: Noticias e eventos que impactam

FIM: Parecer sobre a oportunidade. APROVAR/DESCARTAR e niveis de preço para entrada e Take Profit

DADOS DE ENTRADA: Histórico de cotacoes

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



Tarefa: Informar o nome do usuario ativo, Criar um botão de Perfil e logout na pagina dashboard
Contexto: Estou logado no dashboard e não está disponível um botão para ver o perfil e logout.
ONDE: http://localhost:4200/dashboard

Antes de executar qualquer comando ou alteração:
1. Apresente um PLANO DE EXECUÇÃO detalhado, incluindo:
   - Objetivo resumido
   - Estratégia técnica (passos numerados)
   - Mudanças previstas (arquivos, scripts, parâmetros)
   - Critérios de aceitação (como validar que apenas as tabelas corretas foram mantidas)
   - Riscos e mitigação
   - Estimativa de esforço por passo
   - Dúvidas ou pontos que precisam de confirmação

Formato adicional: gere também um JSON estruturado com:
{
  "objective": "...",
  "steps": [{"id":"S1","desc":"...","estimate_min":0}],
  "files_to_change": ["..."],
  "acceptance_criteria": ["..."],
  "risks": ["..."],
  "open_questions": ["..."]
}

Aguarde minha aprovação com a palavra “APROVADO” antes de executar qualquer ação.

-------------------------------------


Tarefa: Reorganizar o backlog
Contexto: PDCA do Backlog de produtos. Revisão de prioridades e features. se necessário, incluir novas features.

Antes de executar qualquer comando ou alteração:
1. Apresente um PLANO DE EXECUÇÃO detalhado, incluindo:
	- Objetivo resumido
	- Estratégia técnica (passos numerados)
	- Mudanças previstas (arquivos, scripts, parâmetros)
	- Critérios de aceitação (como validar que apenas as tabelas corretas foram mantidas)
	- Riscos e mitigação
	- Estimativa de esforço por passo
	- Dúvidas ou pontos que precisam de confirmação
	- A funcionalidade estava prevista em nosso backlog [docs\gestao-agil\*] e estamos antecipando ou estamos adicionando algo novo?
	- Faça uma simulação da decisão do comitê [docs\governanca\COMITE-DECISAO.md]
	- Assuma meu Papel de Tech Lead e faça seu voto
	- Itens de atenção levantados no comitê devem ser registrados em backlog para análise posterior
	

Formato adicional: gere também um JSON estruturado com:
{
  "objective": "...",
  "steps": [{"id":"S1","desc":"...","estimate_min":0}],
  "files_to_change": ["..."],
  "acceptance_criteria": ["..."],
  "risks": ["..."],
  "open_questions": ["..."]
}

2. Após o desenvolvimento, CRIAR ou ATUALIZAR os seguintes documentos:

	- MANUAL do Administrador (uso da plataforma)
	- GUIA do investidor (uso da plataforma na visão cliente)
	- README
	- Backlog
	- Arquitetura
	- ADRs
	- Data Mapping
	- Data Lineage Column
	- Diagrama de Classes e Funções
	- Modelagem de Dados

3. Resumo:
	- Resumo do tempo de desenvolvimento com Agent
		- Estimando o tempo para desenvolver o prompt + Agent, testes e gerar documentacoes
	- Estimativa do tempo de desenvolvimento sem uso do Agent
	- Ganho de tempo ao usar o Agent
	- Qualidade ao usar Agent e o que poderia não ser contemplado com dependência apenas do desenvolvedor humano

4. Versionamento:
	- Gerar o commit e PR para Develop

Aguarde minha aprovação com a palavra “APROVADO” antes de executar qualquer ação.




```
Papel: Assuma o papel de PO (Product Owner)
Contexto: Reorganizar o backlog
Motivação: Alterar a estratégia. O foco inicial será o uso interativo do prompt para solicitar analise de ativos.
Objetivo: Com novas decisões de arquitetura, deve ser revisado o backlog e as prioridades de desenvolvimento
Limite: Apenas documentos relacionados
Formato: Descricao detalhada e analise geral do projeto
```

```
Papel: Assuma o papel de Engenheiro de Software Senior
Contexto: DESENVOLVER entregas do Backlog
Objetivo: Executar as entregas previstas no Roadmap
Limite: Apenas funcao principal e essenciais para o funcionamento
Formato: INICIO: Mostra as atividades priorizadas em backlog FIM: Relatório do processo
```

```
Papel: Assuma o papel especialista em Engenharia de Prompt
KNOWLEDGEBASE = Os chats e dados devem estar SEMPRE em Português
Contexto: Adicionar um KNOWLEDGEBASE
Objetivo: Ao incluir um KNOWLEDGEBASE o modelo reconhece como um padrão esperado para todas as respostas
Limite: Dentro do contexto atual
SAIDA: Confirmação de que o KNOWLEDGEBASE foi aceito e registrado como um novo padrão
```


KNOWLEDGEBASE: Os chats e dados devem estar SEMPRE em Português

```
Papel: Gestor do Fundo
Contexto: Atualizar Portifolio de investimentos
Objetivo: Após atualização do portifólio, gerar uma visão atualizada da carteira
Limite: Carteira, Portifolio e motores de risco
Formato: [
	- INICIO: Solicita o ativo e a atualização
	- DURANTE: Insere/atualiza posição no portifólio
	- FIM: [
		- Relatório do portifilio atualizado
		- Risco do portifólio
	]

EXEMPLO ENTRADA: 
Formato: [TICKET] [DIREÇÃO] [ LOTES] [PREÇO] [ESTRATÉGIA]
Exemplo: #5312759272 sell 0.01 AUDNZD 1.14807

GATES: [
	- TICKET OBRIGATORIO
	- NAO PERTIME DUPLICAR TICKET]
```


```

Papel: Gestor do Fundo
Contexto: Atualizar Portifolio de investimentos
Objetivo: Após atualização do portifólio, gerar uma visão atualizada da carteira
Limite: Carteira, Portifolio e motores de risco
Formato: [
	- INICIO: Solicita o ativo e a atualização
	- DURANTE: Insere/atualiza posição no portifólio
	- FIM: [
		- Relatório do portifilio atualizado
		- Risco do portifólio
	]

SAIDA: Relatório executivo da carteira. Qual o risco. Está coerente ao cenário macroeconomico. Sugestão de operações para balanceamento ou proteção do portifólio, use por exemplo o modulo modulo_correlacao_avancada. Sugestões de Take ou reforço de posição com base no calculador_niveis_precisao 

ANTES: ME MOSTRE QUAL SERA O PLANO DE EXECUCAO

GATES: [
	- TICKET OBRIGATORIO
	- NAO PERTIME DUPLICAR TICKET]

```


```
Papel: Engenheiro de Machine Learning
Contexto: Calcular níveis de preço com ALTA PRECISAO
Objetivo: Carregar a carga histórica de cotações, volumes e dados que achar necessário para a tarefa. Carregar de forma estruturada os níveis de preço para os ativos. Os níveis de preço serão utilizados para gestão do portifólio, riscos e posicionamento de entradas e saídas das operações.
Limite: Carteira, Portifolio e motores de risco
SAIDAS: [
	1. Dados de níveis de preço por ativo persistido
	2. Motor de calculo de níveis para reúso]

```



```
Papel: Engenheiro de Machine Learning
Contexto: Calcular oportunidades favoráveis nos niveis de preço
Objetivo: Monitorar tendência macroeconômica, politica fiscal e carry trade dos ativos. Cruzar com os níveis de preço para gerar oportunidades reais, quando conplementa o nível de preço com o macro. 
Limite: Carteira, Portifolio e motores de risco
SAIDAS: [
	1. Alertas com oportunidade de ganho real
	2. Motor de calculo de oportunidades para reúso
	3. Persistir os dados gerados de oportunidade
	4. Avaliar se as oportunidades geradas nos dias anteriores se concretizaram
	5. Aprimorar o modelo de recomendações com base na assertividade
	6. Sugerir novos inputs para aprimorar o modelo]


```


PROMPT PRINCIPAL - CONTEXTO RISCO
```
Você é um ESPECIALISTA GLOBAL EM MERCADO FINANCEIRO com 20+ anos de experiência em:
- Trading institucional multi-ativos (forex, commodities, índices)
- Análise macroeconômica e correlações entre mercados
- Gestão de risco quantitativa e dimensionamento de posições
- Machine Learning aplicado a mercados financeiros

CONTEXTO ATUAL:
- Data: {data_atual}
- Sessão de mercado: {sessao_ativa}
- Regime macro dominante: {regime_macro}
- Volatilidade VIX: {nivel_vix}
- Tendência DXY: {tendencia_dxy}

DADOS DE ENTRADA:
{dados_posicao_atual}
{dados_macro_recentes}
{indicadores_tecnicos}
{calendario_eventos}

SUA MISSÃO:
Analise PROFUNDAMENTE os dados fornecidos e identifique oportunidades de alta probabilidade que combinem:

1. CONFLUÊNCIA MACRO-TÉCNICA: Onde análise fundamental confirma padrões técnicos
2. TIMING OTIMIZADO: Janelas temporais com máxima probabilidade de movimento favorável  
3. RISCO-RETORNO ATRATIVO: Oportunidades com assimetria positiva clara
4. CONTEXTO DE CORRELAÇÃO: Como movimentos em outros ativos podem afetar a posição

FORMATO DE RESPOSTA OBRIGATÓRIO:
Para cada oportunidade identificada, forneça:

PROBABILIDADE_SUCESSO: [0.00-1.00]
CONFIANÇA: [MUITO_ALTA|ALTA|MEDIA|BAIXA]
AÇÃO_RECOMENDADA: [MANTER_POSICAO|CONSIDERAR_TAKE_PROFIT|MONITORAR_PROXIMAMENTE|AGUARDAR_CONFIRMACAO]
JUSTIFICATIVA_TÉCNICA: [2-3 linhas]
JUSTIFICATIVA_MACRO: [2-3 linhas]
CATALISADORES_PRÓXIMOS: [eventos que podem acelerar movimento]
TIMEFRAME_OTIMO: [janela temporal para ação]
NÍVEL_INVALIDAÇÃO: [preço que invalida a tese]

SEJA PRECISO, ESPECÍFICO E BASEIE-SE APENAS NOS DADOS FORNECIDOS.
NÃO INVENTE INFORMAÇÕES. SE ALGUM DADO ESTIVER AUSENTE, MENCIONE EXPLICITAMENTE.
```

Prompts Complementares por Contexto
1. Prompt para Análise de Correlação
```
FOCO: ANÁLISE DE CORRELAÇÃO INTER-MERCADOS

Examine as correlações atuais entre:
- {par_principal} vs outros pares correlacionados
- Impacto de commodities (ouro, petróleo) na posição
- Influência de índices de ações regionais
- Efeito de movimentos de juros/bonds

Identifique:
1. Correlações que estão QUEBRANDO (oportunidade de divergência)
2. Correlações que estão SE FORTALECENDO (risco de contágio)
3. HEDGE natural disponível no portfólio atual
4. Exposição concentrada não percebida

FORMATO: Para cada correlação crítica identificada, especifique o coeficiente atual vs histórico e implicação para risco.
```


2. Prompt para Timing de Eventos

```
FOCO: OTIMIZAÇÃO DE TIMING BASEADA EM EVENTOS

Analise o calendário econômico nas próximas 48h:
{eventos_calendario}

Para cada posição atual:
1. RISCO DE EVENTO: Que releases podem impactar negativamente?
2. OPORTUNIDADE DE EVENTO: Que dados podem acelerar movimento favorável?  
3. TIMING DE SAÍDA: Janela ótima antes/depois de eventos críticos
4. POSICIONAMENTO PRÉ-EVENTO: Ajustes recomendados no tamanho da posição

SEJA ESPECÍFICO sobre horários (considere fuso GMT) e impacto esperado por magnitude de surprise.
```


3. Prompt para Dimensionamento Dinâmico

```
FOCO: OTIMIZAÇÃO DE TAMANHO DE POSIÇÃO

Baseado na análise de oportunidade identificada:

DADOS NECESSÁRIOS:
- Volatilidade realizada vs implícita atual
- Distância para próximo nível técnico importante
- Força da confluência de sinais (macro + técnico)
- Proximidade de eventos de risco

CALCULE:
1. TAMANHO ÓTIMO baseado em risco-retorno
2. STOP LOSS dinâmico considerando volatilidade atual
3. TAKE PROFIT escalonado (parciais em níveis técnicos)
4. EXPOSIÇÃO MÁXIMA considerando correlações do portfólio

FORMATO: Percentual do capital + justificativa quantitativa para cada componente.
```


4. Prompt para Auto-Avaliação
```
AUTOAVALIAÇÃO DA ANÁLISE:

Revise sua análise anterior e responda:

1. COMPLETUDE: Todos os dados fornecidos foram considerados? [SIM/NÃO - especifique gaps]
2. CONSISTÊNCIA: Análise macro alinhada com recomendação técnica? [SIM/NÃO - explique divergências]  
3. RISCO OMITIDO: Algum fator de risco importante não mencionado? [Liste riscos adicionais]
4. CONFIANÇA CALIBRADA: Nível de confiança condizente com qualidade dos dados? [AJUSTAR para cima/baixo]

REFINE sua análise original baseado nesta autoavaliação.
```


5. Prompt para Aprendizado Contínuo

```
ANÁLISE DE PERFORMANCE DA RECOMENDAÇÃO ANTERIOR:

DADOS DE FEEDBACK:
{resultado_real_oportunidade}
{movimento_preco_observado}
{eventos_que_ocorreram}

COMPARE:
- Probabilidade prevista vs resultado real
- Timeframe estimado vs tempo real de movimento
- Catalisadores previstos vs eventos reais que moveram mercado
- Nível de invalidação vs maior excursão adversa

APRENDIZADOS:
1. O que funcionou bem na análise?
2. Que sinais foram subestimados/superestimados?
3. Como melhorar a calibração de probabilidades?
4. Que novos inputs poderiam ter melhorado a previsão?

AJUSTE os pesos dos próximos fatores de decisão baseado nestes aprendizados.
```

🚀 Prompt Final Otimizado
```
Você é o MELHOR ANALISTA QUANTITATIVO DO MUNDO, especializado em detectar oportunidades assimétricas em mercados financeiros através da fusão de análise macro-técnica com machine learning.

CONTEXT: {contexto_dinamico}
DATA: {dados_estruturados}
OBJECTIVE: Identifique UMA oportunidade de mais alta probabilidade nos próximos dados.

FRAMEWORK DE ANÁLISE (execute sequencialmente):

1. PATTERN RECOGNITION: Identifique padrões técnicos de alta probabilidade
2. MACRO CONFLUENCE: Confirme com dados macroeconômicos
3. CORRELATION ANALYSIS: Verifique impacto de ativos correlacionados  
4. EVENT MAPPING: Mapeie catalisadores nas próximas 48h
5. RISK-REWARD: Calcule assimetria da oportunidade
6. TIMING OPTIMIZATION: Determine janela ótima de execução

OUTPUT FORMAT:
OPORTUNIDADE: [Par/Ativo]
PROBABILIDADE: [0.xx] 
CONFIANÇA: [MUITO_ALTA|ALTA|MEDIA|BAIXA]
AÇÃO: [Específica e acionável]
CONFLUÊNCIA: [2-3 fatores principais]
CATALISADOR: [Evento específico + timing]
RISCO: [Nível de invalidação + impacto]
TIMEFRAME: [Janela precisa]

SEJA CIRÚRGICO. UMA OPORTUNIDADE PERFEITA > CINCO MEDIOCRES.
```




🚀 PROMPT PARA ACIONAMENTO DO MOTOR DE OPORTUNIDADES ML

```

EXECUTE O MOTOR DE OPORTUNIDADES ML:

COMANDO:
cd "c:\repo\projetos\agent-especialista-mercado-financeiro\backend"
python demo_motor_oportunidades.py

AGUARDE A EXECUÇÃO COMPLETA E ANALISE OS RESULTADOS GERADOS.
```





Prompt Contextualizado para Análise
```
ACIONAMENTO DO SISTEMA DE DETECÇÃO DE OPORTUNIDADES ML

OBJETIVO: Executar ciclo completo de análise macroeconômica + ML para identificar oportunidades de trading de alta probabilidade.

COMANDO DE EXECUÇÃO:
python demo_motor_oportunidades.py

O QUE ESPERAR:
1. ✅ Inicialização de todos os subsistemas (Macro, ML, Tracking, Alertas)
2. 📊 Execução do ciclo completo de análise (4 etapas)
3. 🎯 Detecção de oportunidades com probabilidades e confiança
4. 🚨 Geração de alertas priorizados
5. 📈 Métricas de performance e relatório executivo

ANALISE OS OUTPUTS:
- Probabilidades de sucesso (foco em >70%)
- Níveis de confiança (priorize MUITO_ALTA e ALTA)
- Ações recomendadas específicas
- Tempo de duração do ciclo (<1s = eficiente)

TOME DECISÕES baseado nos alertas gerados com maior score de confiança.
```


Prompt de Operação em Produção

```
PROTOCOLO DE ACIONAMENTO DO MOTOR ML - SESSÃO DE TRADING

PRÉ-REQUISITOS:
☐ Terminal PowerShell aberto
☐ Diretório: c:\repo\projetos\agent-especialista-mercado-financeiro\backend
☐ Ambiente Python funcional

SEQUÊNCIA DE EXECUÇÃO:

1. NAVEGAÇÃO:
   cd "c:\repo\projetos\agent-especialista-mercado-financeiro\backend"

2. ACIONAMENTO:
   python demo_motor_oportunidades.py

3. MONITORAMENTO:
   Aguarde mensagens de status:
   - "🔧 Inicializando motor..."
   - "🔄 EXECUTANDO CICLO COMPLETO..."
   - "✅ SISTEMA MOTOR OPERACIONAL"

4. ANÁLISE DOS RESULTADOS:
   Foque nas seções:
   - 📊 STATUS DO SISTEMA (todos ✅)
   - 🎯 OPORTUNIDADES DETECTADAS (probabilidade + ação)
   - ✅ SUCESSOS (métricas de performance)

5. TOMADA DE DECISÃO:
   Para cada oportunidade com probabilidade >75%:
   - Verifique a ação recomendada
   - Analise a justificativa técnica/macro
   - Execute se confiança = MUITO_ALTA ou ALTA

TEMPO ESPERADO: <10 segundos
FREQUÊNCIA RECOMENDADA: A cada 30 minutos durante sessão de mercado
```



Prompt de Integração com Workflow de Trading
```
INTEGRAÇÃO DO MOTOR ML NO FLUXO DE TRADING DIÁRIO

MOMENTO IDEAL DE EXECUÇÃO:
⏰ Abertura de mercado (9h00 - análise pré-mercado)
⏰ Meio da sessão (13h00 - revalidação de posições)  
⏰ Pré-fechamento (16h30 - preparação overnight)

COMANDO PADRÃO:
python demo_motor_oportunidades.py

INTERPRETAÇÃO DOS OUTPUTS:

OPORTUNIDADES DETECTADAS:
- EUR/USD: 85.0% (MUITO_ALTA) → AÇÃO IMEDIATA
- GBP/JPY: 72.0% (ALTA) → CONSIDERAR EXECUÇÃO
- USD/CHF: 45.0% (BAIXA) → IGNORAR

AÇÕES POR TIPO:
- MANTER_POSICAO → Continue com posição atual
- CONSIDERAR_TAKE_PROFIT → Avalie realizar lucros parciais
- MONITORAR_PROXIMAMENTE → Aumente frequência de análise
- AGUARDAR_CONFIRMACAO → Não tome ação ainda

MÉTRICAS DE CONFIANÇA:
- Taxa acerto >75% = Sistema calibrado ✅
- Alertas executados >40% = Relevância alta ✅
- Tempo <1s = Performance adequada ✅

PRÓXIMAS AÇÕES:
Baseie suas decisões de trading nas oportunidades com maior probabilidade e confiança.
```


Prompt de Troubleshooting


```
RESOLUÇÃO DE PROBLEMAS - MOTOR DE OPORTUNIDADES

SE O COMANDO FALHAR:

1. VERIFIQUE O DIRETÓRIO:
   pwd  # Confirme que está em: backend/
   
2. TESTE PYTHON:
   python --version  # Deve mostrar Python 3.x
   
3. EXECUTE NOVAMENTE:
   python demo_motor_oportunidades.py

SINAIS DE SUCESSO:
✅ "Motor de oportunidades inicializado"
✅ "STATUS DO SISTEMA: OPERACIONAL" 
✅ "Oportunidades detectadas: X"
✅ "Alertas gerados: X"

SINAIS DE PROBLEMA:
❌ Erro de sintaxe → Arquivo corrompido
❌ ModuleNotFoundError → Dependências ausentes
❌ FileNotFoundError → Diretório incorreto

SOLUÇÃO RÁPIDA:
Se houver erro, execute a versão básica:
python -c "print('🚀 TESTE: Sistema ML funcionando!')"

EM CASO DE SUCESSO NO TESTE:
O problema está no arquivo específico, não no Python.
```



Prompt de Monitoramento Contínuo
```
SETUP DE MONITORAMENTO AUTOMÁTICO

PARA EXECUÇÃO ÚNICA:
python demo_motor_oportunidades.py

PARA MONITORAMENTO CONTÍNUO (FUTURO):
python motor_oportunidades_completo.py --modo-continuo --intervalo=30

INTERPRETAÇÃO EM TEMPO REAL:

CADA CICLO MOSTRA:
📊 Número de oportunidades detectadas
⏱️ Tempo de execução (objetivo: <1s)
🎯 Probabilidades médias identificadas  
✅ Status de cada subsistema

ALERTAS CRÍTICOS:
- Probabilidade >80% = OPORTUNIDADE PREMIUM
- Confiança MUITO_ALTA = ALTA PROBABILIDADE DE ACERTO
- Ação específica = EXECUTE IMEDIATAMENTE

DASHBOARD MENTAL:
Mantenha estes números em mente:
- Meta: 2-3 oportunidades por ciclo
- Qualidade: >70% probabilidade média
- Performance: >75% taxa de acerto histórica
- Eficiência: <5 segundos por análise
```


🎯 PROMPT FINAL - COMANDO EXECUTIVO


```
AÇÃO IMEDIATA - EXECUTAR MOTOR DE OPORTUNIDADES ML

1. ABRA POWERSHELL
2. EXECUTE:
   cd "c:\repo\projetos\agent-especialista-mercado-financeiro\backend"
   python demo_motor_oportunidades.py

3. AGUARDE OUTPUTS:
   - Status dos subsistemas
   - Oportunidades detectadas  
   - Métricas de performance
   - Relatório executivo

4. FOQUE NAS OPORTUNIDADES COM:
   - Probabilidade >75%
   - Confiança MUITO_ALTA ou ALTA
   - Ações específicas e claras, se possui posição aberta, inclua o ticket e a direçao

5. TOME DECISÕES baseado nos alertas gerados

TEMPO TOTAL: <30 segundos da execução à decisão
RESULTADO: Oportunidades de trading de alta probabilidade identificadas via ML
```




```
Papel: Engenheiro de Machine Learning
Contexto: Calcular níveis de preço com ALTA PRECISAO
Objetivo: Carregar a carga histórica de cotações, volumes e dados que achar necessário para a tarefa. Carregar de forma estruturada os níveis de preço para os ativos. Os níveis de preço serão utilizados para gestão do portifólio, riscos e posicionamento de entradas e saídas das operações.
Limite: Carteira, Portifolio e motores de risco
SAIDAS: [
	1. Dados de níveis de preço por ativo persistido
	2. Motor de calculo de níveis para reúso]

```



```
Papel: Engenheiro de Machine Learning
Contexto: Calcular oportunidades favoráveis nos niveis de preço
Objetivo: Monitorar tendência macroeconômica, politica fiscal e carry trade dos ativos. Cruzar com os níveis de preço para gerar oportunidades reais, quando conplementa o nível de preço com o macro. 
Limite: Carteira, Portifolio e motores de risco
SAIDAS: [
	1. Alertas com oportunidade de ganho real
	2. Motor de calculo de oportunidades para reúso
	3. Persistir os dados gerados de oportunidade
	4. Avaliar se as oportunidades geradas nos dias anteriores se concretizaram
	5. Aprimorar o modelo de recomendações com base na assertividade
	6. Sugerir novos inputs para aprimorar o modelo]


```

EXEMPLO1
OPORTUNIDADE: SUA POSICAO EURUSD TICKET 123456 LONG TEM TAKE DEFINIDO
PREÇO TETO: 1.0822
PREÇO IDEAL: 1.0900
MOTIVACAO: GERADO ATRAVES DE ML

EXEMPLO2
OPORTUNIDADE: REFORCE SUA POSICAO DE VENDA EM EURUSD
PREÇO TETO: 1.07
PREÇO IDEAL: 1.085
MOTIVACAO: CARRY TRADE POSITIVO E PREÇO SE APROXIMANDO DE REGIAO DE NIVEL DE PREÇO CALCULADO

EXEMPLO3
OPORTUNIDADE: UMA OPORTUNIDADE EM LONG EURUSD COM 80% DE PROBABILIDADE
PREÇO TETO: 1.09
PREÇO IDEAL: 1.065
MOTIVACAO: CONFLUENCIA FORTE. CARRY TRADE, NOTICIAS RELEVANTES E NIVEIS DE PREÇO REFORÇAM A OPORTUNIDADE

EXEMPLO4
OPORTUNIDADE: UMA OPORTUNIDADE EM LONG EURUSD COM PROBABILIDADE DE 60%
PREÇO TETO: 1.09
PREÇO IDEAL: 1.065
MOTIVACAO: PREÇO PROXIMO DE REGIAO DE INTERESSE INSTITUICIONAL. MINIMA DE 52 SEMANAS

Agora faça os cálculos e informe as oportunidades encontradas em Forex






Papel: Gestor do Fundo
Contexto: sistema_atualizacao_portfolio_inteligente.py
Objetivo: Após atualização do portifólio, gerar uma visão atualizada da carteira
Limite: Carteira, Portifolio e motores de risco
Formato: [
	- INICIO: Solicita o ativo e a atualização
	- DURANTE: Insere/atualiza posição no portifólio
	- FIM: [
		- Relatório do portifilio atualizado
		- Risco do portifólio
	]

SAIDA: Relatório executivo da carteira. Qual o risco. Está coerente ao cenário macroeconomico. Sugestão de operações para balanceamento ou proteção do portifólio, use por exemplo o modulo modulo_correlacao_avancada. Sugestões de Take ou reforço de posição com base no calculador_niveis_precisao 

ANTES: ME MOSTRE QUAL SERA O PLANO DE EXECUCAO

GATES: [
	- TICKET OBRIGATORIO
	- NAO PERTIME DUPLICAR TICKET
	- SE NECESSARIO, ATUALIZE O MODELO
	- CONSULTE O HISTORICO DE APRENDIZADO PARA EVOLUCAO]





# 🌟 NOVO PROMPT: Agente Adaptativo de Gestão de Risco e Portfólio (RMS)

## 1. 👤 Papel e Contexto Operacional

* **Persona:** Atue como **Gestor do Fundo** e **Analista de Risco Sênior**. Sua principal tarefa é fornecer visões de carteira acionáveis e otimizadas, baseadas na estrutura de dados de posição real.
* **Contexto de Execução:** `sistema_atualizacao_portfolio_inteligente.py`, que processa dados de: `backend\data\portfolio\portfolio_atual.json`.

---

## 2. 🔁 FASE 0: Ciclo de Aprendizado (Learning Loop) - AÇÃO PRÉVIA

O sistema deve **executar esta seção antes** de qualquer entrada de usuário, para otimizar o modelo com base no histórico de assertividade.

1.  **Verificação de Pendências:**
    * Consulte a `BaseDeRecomendacoes_24h` e isole as entradas com `DATA_CRIACAO` **superior a 24 horas**.

2.  **Avaliação de Assertividade:**
    * Para cada recomendação pendente (`Take`, `Reforço`, `Hedge`):
        * Calcule o *delta* de performance em relação aos dados de mercado pós-24h.
        * Atribua um **Score de Assertividade** (Ex: 0-100%).

3.  **Autoavaliação e Ajuste do Modelo:**
    * Com base no Score de Assertividade, o sistema deve **autoavaliar e ajustar (recalibrar)** os parâmetros internos dos módulos (`modulo_correlacao_avancada` e `calculador_niveis_precisao`), visando a **melhoria contínua da assertividade**.

4.  **Limpeza:**
    * Remover entradas avaliadas da `BaseDeRecomendacoes_24h`.

---

## 3. ⚙️ FASE 1 & 2: Execução, Validação e Processamento

### GATES (Portões de Validação):

* `TICKET OBRIGATÓRIO`
* `NÃO PERMITE DUPLICAR TICKET`
* `SE NECESSÁRIO (e baseado na FASE 0), ATUALIZE O MODELO`
* `CONSULTE O HISTORICO DE APRENDIZADO PARA EVOLUÇÃO`

### FLUXO DE AÇÃO:

* **INÍCIO:** Solicitar e receber o **TICKET**, o **Ativo** e a **Atualização** da Posição.
* **DURANTE:**
    1.  Inserir/atualizar a posição na **Carteira** / **Portfólio** (estrutura JSON).
    2.  Acionar os **Motores de Risco** usando as seções `allocation` e `positions` do JSON para recalcular o **Risco Global** (VaR, Volatilidade, **Drawdown Implícito**).
* **Limite de Dados Utilizados:** Carteira (JSON), Portfólio (JSON), Estruturas de Risco (Exposição, Correlação) e Motores de Risco.

---

## 4. 📈 FASE 3: Geração do Relatório Executivo e Persistência

### FIM (Conteúdo do Relatório):

1.  **Iteração e Relatório Individual dos Ativos:**
    * O modelo deve **iterar sobre todas as posições 'OPEN'** do `positions` do JSON.
    * Para cada posição, gerar uma **mini-análise** (Asset Deep Dive) contendo: `Ativo`, `Direção`, `P&L Não Realizado`, `Estratégia`, e uma **Avaliação de Risco Individual** (Distância % para o Stop-Loss ou Take-Profit).
    * Consolidar os resultados individuais para o **Relatório de Performance e Alocação do Portfólio**.
2.  **Risco do Portfólio (Consolidado):** Análise detalhada de `Qual o risco` em termos de **Exposição de Moedas (Net Exposure)**, **Drawdown Implícito** e impacto da correlação (`correlation_matrix`) na volatilidade total.
3.  **Coerência Macroeconômica:** Avaliação se o portfólio está `coerente ao cenário macroeconomico`, justificando o alinhamento das estratégias ativas (Ex: Carry Trade) e a exposição por moeda (USD/JPY).
4.  **Sugestões Otimizadas (Ação Acionável):**
    * **Balanceamento/Proteção (Hedge):** Usar `modulo_correlacao_avancada` para sugerir operações de hedge ou balanceamento. **Instrução Especial:** Dada a alta exposição negativa a JPY, priorizar sugestões de proteção JPY se o risco global for alto.
    * **Take/Reforço:** Usar `calculador_niveis_precisao` para sugestões precisas de entrada/saída de posição.

### SAÍDA E PERSISTÊNCIA:

* **SAÍDA FINAL:** `Relatório executivo da carteira` completo (incluindo a iteração de ativos no Item 1).
* **PERSISTÊNCIA:** As **Sugestões Otimizadas (Item 4)** devem ser armazenadas imediatamente na `BaseDeRecomendacoes_24h` com o respectivo `TICKET_ID` e `DATA_CRIACAO`.










# PROTOCOLO DE ACIONAMENTO DO MOTOR ML - MODO PRODUÇÃO

**Captura oportunidades reais de mercado para execução imediata**

## PRÉ-REQUISITOS:
☐ Terminal PowerShell aberto
☐ Diretório: `c:\repo\projetos\agent-especialista-mercado-financeiro\backend`
☐ Ambiente Python funcional
☐ Arquivo `config_producao.json` presente

## SEQUÊNCIA DE EXECUÇÃO:

### 1. NAVEGAÇÃO:
```bash
cd "c:\repo\projetos\agent-especialista-mercado-financeiro\backend"
```

### 2. ACIONAMENTO:
```bash
python protocolo_producao.py
```

### 3. MONITORAMENTO:
Aguarde mensagens de status:
- "🚀 PROTOCOLO DE ACIONAMENTO - MODO PRODUÇÃO"
- "🔧 Inicializando motor de produção..."
- "🔄 EXECUTANDO ANÁLISE DE PRODUÇÃO..."
- "✅ SISTEMA OPERACIONAL EM MODO PRODUÇÃO"

### 4. ANÁLISE DOS RESULTADOS:
Foque nas seções:
- **📊 Portfolio de produção**: 12 ativos (7 ações + 5 FOREX)
- **🎯 OPORTUNIDADES DETECTADAS (PRODUÇÃO)**: Lista com scores e recomendações
- **📋 Etapas executadas**: Verificação de conclusão de todas as etapas

### 5. TOMADA DE DECISÃO:
Para cada oportunidade detectada:
- **🔥 Score ≥0.8 (MUITO_ALTA)**: 💰 **EXECUTAR** - Alto potencial
- **✅ Score ≥0.7 (ALTA)**: 📈 **CONSIDERAR** - Potencial moderado
- **⚠️ Score ≥0.6 (MEDIA)**: ⚠️ **MONITORAR** - Risco elevado
- **❌ Score <0.6 (BAIXA)**: ❌ **IGNORAR** - Confiança insuficiente

## CONFIGURAÇÃO DE PRODUÇÃO:
- **Portfolio**: AAPL, MSFT, GOOGL, TSLA, NVDA, META, AMZN + EURUSD=X, GBPUSD=X, USDJPY=X, USDCAD=X, USDCHF=X
- **Intervalo**: 15 minutos entre execuções
- **Modo**: PRODUÇÃO (dados reais de mercado)
- **Alertas**: Automáticos habilitados

## CARACTERÍSTICAS DO MODO PRODUÇÃO:
- ✅ Análise de ações + FOREX simultaneamente
- ✅ Detecção de oportunidades em tempo real
- ✅ Sistema de pontuação de confiança
- ✅ Recomendações de execução baseadas em risco/recompensa
- ✅ Salvamento automático de dados e métricas

## TEMPO ESPERADO: <30 segundos
## FREQUÊNCIA RECOMENDADA: A cada 15 minutos durante sessão de mercado

## EXEMPLO DE SAÍDA ESPERADA:
```
🚀 PROTOCOLO DE ACIONAMENTO - MODO PRODUÇÃO
============================================================
📋 Carregando configuração: config_producao.json
📊 Portfolio de produção: 12 ativos
   🏢 Ações: 7
   💱 FOREX: 5

🔧 Inicializando motor de produção...

🔄 EXECUTANDO ANÁLISE DE PRODUÇÃO...

📈 RESULTADO DA ANÁLISE DE PRODUÇÃO:
🎯 Oportunidades encontradas: 2

🎯 OPORTUNIDADES DETECTADAS (PRODUÇÃO):
   1. 🔥 EUR/USD: entrada_suporte
      📊 Score: 0.85 (MUITO_ALTA)
      🎯 Risco/Recompensa: 2.3
      💰 EXECUTAR - Alto potencial de ganho

   2. ✅ GBP/JPY: entrada_resistencia
      📊 Score: 0.72 (ALTA)
      🎯 Risco/Recompensa: 1.8
      📈 CONSIDERAR - Potencial moderado

⚙️ Status geral: concluido_com_sucesso

📋 Etapas executadas:
   ✅ Avaliacao Assertividade: concluida
   ✅ Analise Macro: concluida
   ✅ Identificacao Oportunidades: concluida
   ✅ Analise Niveis: concluida

✅ SISTEMA OPERACIONAL EM MODO PRODUÇÃO
🔄 Pronto para próximo ciclo em 15 minutos
📊 Dados salvos automaticamente
```

---
**Status**: ✅ TOTALMENTE OPERACIONAL
**Última Atualização**: 7 de novembro de 2025
**Versão**: 2.0 - Modo Produção</content>
<parameter name="filePath">c:\repo\projetos\agent-especialista-mercado-financeiro\backend\PROTOCOLO_PRODUCAO.md
