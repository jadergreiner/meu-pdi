#  Lições Aprendidas - Meu PDI

Este documento registra todas as lições aprendidas durante o desenvolvimento do projeto Meu PDI. Cada lição é documentada com contexto, erro identificado e aprendizado extraído.

##  Estrutura das Lições

Cada lição aprendida segue o formato padronizado:

`markdown

###  [Data] - [Título da Lição]

**Data:** YYYY-MM-DD

**Qual era o contexto:**
[Descrição detalhada do contexto onde ocorreu a situação]

**Qual foi o erro gerado:**
[Descrição específica do erro, problema ou situação indesejada]

**Qual a lição aprendida:**
[Aprendizado extraído, melhores práticas identificadas, recomendações]

**Status:** [Registrada | Aplicada | Descartada]
`

##  Processo de Gestão

- **Registrada:** Lição identificada e documentada
- **Aplicada:** Lição implementada nos processos atuais
- **Descartada:** Lição não aplicável ao contexto atual


---

##  Lições Aprendidas Registradas

### **LA-001: Desenvolvimento sem Gate de Qualidade**

**Data:** 02/11/2025

**Contexto da Ocorrência:** Durante a criação inicial do projeto, foi iniciado o desenvolvimento do src/ sem passar pelo gate de qualidade EPIC/SPIN/SMART, resultando em estrutura incorreta e retrabalho.

**Erro ou Impacto Gerado:** Criação de estrutura src/ que viola a arquitetura definida no ADR-002, causando desalinhamento técnico e necessidade de retrabalho futuro.

**Qual a Lição Aprendida:** Sempre aplicar o gate de qualidade antes de qualquer desenvolvimento. Validar estratégia, SPIN e SMART antes de iniciar qualquer task.

**Status:** Aplicado

---

### **LA-002: Backlog Genérico sem Personas**

**Data:** 02/11/2025

**Contexto da Ocorrência:** O backlog inicial foi criado com tasks genéricas sem considerar as 3 personas específicas (Gestor, Mentor, Aluno), resultando em funcionalidades desalinhadas com as necessidades reais de cada usuário.

**Erro ou Impacto Gerado:** Tasks que não atendem às jornadas específicas de cada persona, potencial para desenvolvimento de funcionalidades desnecessárias ou faltantes.

**Qual a Lição Aprendida:** Sempre iniciar o refinamento técnico identificando e documentando as personas principais e suas jornadas específicas antes de detalhar funcionalidades.

**Status:** Aplicado

---

### **LA-003: Falta de Critérios SMART Consistentes**

**Data:** 02/11/2025

**Contexto da Ocorrência:** Tasks do backlog anterior não seguiam rigorosamente os critérios SMART, com estimativas irreais e critérios de aceitação vagos.

**Erro ou Impacto Gerado:** Dificuldade de planejamento, medição de progresso e validação de conclusão das tasks.

**Qual a Lição Aprendida:** Aplicar sistematicamente os critérios SMART em todas as tasks: Specific (específico), Measurable (mensurável), Achievable (alcançável), Relevant (relevante), Time-bound (temporal).

**Status:** Aplicado

---

### **LA-004: Commits Diretos na Branch Main**

**Data:** 02/11/2025

**Contexto da Ocorrência:** Durante a atualização massiva das instruções do Copilot, todas as modificações foram commitadas diretamente na branch main sem utilizar branches feature, resultando em histórico não isolado e falta de code review.

**Erro ou Impacto Gerado:** Histórico de commits poluído na branch principal, ausência de pull requests para validação das mudanças, e risco de introdução de bugs sem revisão adequada.

**Qual a Lição Aprendida:** Sempre utilizar branches feature para desenvolvimento, nunca commitar diretamente na main. Implementar fluxo Git com feature branches, code review obrigatório via pull requests, e proteção da branch main.

**Status:** Aplicado

---

### **LA-005: Problemas de Formatação Markdown no Backlog**

**Data:** 02/11/2025

**Contexto da Ocorrência:** Durante a validação automática do projeto, foi identificado que o arquivo planning/backlog.md possui 87 erros de formatação markdown, incluindo headings sem linha em branco, listas mal formatadas e ausência de nova linha no final do arquivo.

**Erro ou Impacto Gerado:** Documentação com formatação inconsistente compromete a legibilidade, dificulta manutenção e pode causar problemas em ferramentas automatizadas de processamento de markdown.

**Qual a Lição Aprendida:** Implementar validação automática de markdown em todos os arquivos de documentação e corrigir problemas de formatação imediatamente quando identificados. Usar ferramentas como validate_markdown.py regularmente.

**Status:** Aplicada

---

### **LA-006: Auto-aprovação de Comandos Similares**

**Data:** 02/11/2025

**Contexto da Ocorrência:** Durante verificação de sintaxe do arquivo main.py, o comando `python -m py_compile main.py` foi cancelado desnecessariamente, apesar de ser um comando seguro de validação similar a outros já executados anteriormente.

**Erro ou Impacto Gerado:** Interrupção desnecessária do fluxo de trabalho, perda de tempo e frustração ao executar comandos de validação que são seguros e similares a outros já aprovados.

**Qual a Lição Aprendida:** Comandos similares de validação/verificação (como py_compile, pytest, validação de sintaxe) devem receber auto-aprovação quando já foram executados com sucesso anteriormente, evitando interrupções desnecessárias no fluxo de desenvolvimento. Descoberta adicional: uvicorn deve ser executado da raiz do projeto usando `python -m uvicorn src.backend.main:app` ao invés de dentro do diretório backend.

**Status:** Aplicada

---

### **LA-007: Rate Limiting em Operações Massivas de Edição**

**Data:** 03/11/2025

**Contexto da Ocorrência:** Durante a tradução sistemática dos nomes das funções de teste do inglês para o português, foram realizadas múltiplas chamadas individuais para edição de arquivos, resultando em rate-limiting frequente devido ao alto volume de operações de API.

**Erro ou Impacto Gerado:** Mensagens de rate-limited, excedente de uso de tokens, interrupções no fluxo de trabalho e necessidade de "Try Again" repetidas vezes.

**Qual a Lição Aprendida:** Unificar ações similares em operações em lote para reduzir o número de chamadas de API e consumo de tokens. Considerar o uso de scripts Python para processar edições repetitivas em massa, ou agrupar múltiplas edições em uma única operação quando possível. Por exemplo, ao invés de usar replace_string_in_file individualmente para cada nome de função, desenvolver um script que processe todas as traduções de uma vez.

**Status:** Registrada

---

## Estatísticas das Lições

- **Total de Lições:** 7
- **Aplicadas:** 6
- **Registradas:** 1
- **Descartadas:** 0


## Última Atualização

**Data:** 03 de novembro de 2025

**Responsável:** Sistema de Documentação Automatizada

**Próxima Revisão:** Mensal
