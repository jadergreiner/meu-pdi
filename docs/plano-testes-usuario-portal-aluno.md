# 🧪 Plano de Testes de Usuário - Portal do Aluno MVP

## 🎯 Objetivo

Validar as hipóteses de negócio do Portal do Aluno através de testes com usuários reais, coletando métricas de engajamento, usabilidade e feedback para decisões data-driven.

## 📊 Metodologia

### **Abordagem Lean**

- **Mínimo Viável de Testes:** Foco em hipóteses críticas com investimento mínimo
- **Iteração Rápida:** Testes curtos (15-30 min) com feedback imediato
- **Métricas Quantitativas:** Taxas de conversão, tempo de tarefa, satisfação
- **Feedback Qualitativo:** Entrevistas curtas para insights profundos

### **Hipóteses a Validar**

#### **H1: Cadastro e Login**

- Usuários conseguem se cadastrar sem dificuldades
- Processo de login é intuitivo e seguro
- Recuperação de senha funciona quando necessário

#### **H2: Dashboard PDI**

- Usuários entendem o conceito de PDI através da interface
- Dashboard carrega rapidamente (<2s)
- Informações são apresentadas de forma clara e organizada

#### **H3: Engajamento**

- Usuários identificam próximos passos claramente
- Interface responsiva funciona bem em mobile
- Experiência geral é positiva e motivadora

## 👥 Recrutamento de Usuários

### **Perfil dos Testadores**

- **Persona Primária:** Desenvolvedores Plenos/Seniors (25-40 anos)
- **Persona Secundária:** Jovens profissionais em transição de carreira
- **Critérios:**
  - Interesse em desenvolvimento profissional
  - Acesso a computador/smartphone
  - Disponibilidade para sessão de 30 minutos

### **Canais de Recrutamento**

1. **LinkedIn:** Posts em grupos de tecnologia e carreira
2. **Comunidades Técnicas:** Discord, Slack, Telegram
3. **Redes Pessoais:** Contatos diretos do empreendedor
4. **Grupos de Facebook:** Desenvolvimento de carreira

### **Incentivo**

- **Valor:** Sessão gratuita de mentoria (30 min) após teste
- **Alternativa:** Certificado de participação + feedback personalizado

## 📋 Protocolo de Teste

### **Sessão Estruturada (30 minutos)**

#### **1. Preparação (5 min)**

- Apresentação do projeto e objetivos
- Consentimento para gravação (áudio/tela)
- Coleta de dados demográficos básicos

#### **2. Teste Exploratório (15 min)**

- **Cenário:** "Você acabou de se inscrever em um programa de mentoria para desenvolvimento profissional. Explore a plataforma e veja como ela pode te ajudar."
- **Tarefas:**
  1. Criar conta e fazer login
  2. Explorar o dashboard
  3. Verificar informações do perfil
  4. Identificar próximos passos
- **Observação:** Think-aloud protocol (usuário verbaliza pensamentos)

#### **3. Entrevista (5 min)**

- **SUS (System Usability Scale):** Questionário padronizado
- **Perguntas abertas:**
  - O que achou da experiência geral?
  - Algum ponto de confusão ou dificuldade?
  - Como você descreveria a plataforma para um amigo?
  - Quais funcionalidades você gostaria de ver?

#### **4. Follow-up (5 min)**

- Agradecimento e entrega do incentivo
- Coleta de contato para feedback adicional
- Agendamento da sessão de mentoria (se aplicável)

## 📊 Métricas de Sucesso

### **Métricas Quantitativas**

#### **Taxa de Conversão**

- **Cadastro:** % de usuários que completam o cadastro
- **Login:** % de usuários que fazem login com sucesso
- **Engajamento:** % que exploram todas as seções do dashboard

#### **Performance Técnica**

- **Tempo de Carregamento:** Média <2s por página
- **Tempo de Tarefa:** Média para completar ações principais
- **Responsividade:** Funciona em desktop/tablet/mobile

#### **Usabilidade (SUS Score)**

- **Target:** Score >70 (escala 0-100)
- **Benchmark:** Bom = 70+, Excelente = 85+

### **Métricas Qualitativas**

- **Satisfação Geral:** NPS-style question
- **Pontos de Dor:** Issues recorrentes identificados
- **Sugestões de Melhoria:** Features mais solicitadas

## 🛠️ Setup Técnico

### **Ambiente de Teste**

- **URL:** `http://localhost:3000` (frontend) + `http://localhost:8000` (backend)
- **Dados de Teste:** Usuários pré-cadastrados disponíveis
- **Monitoramento:** Hotjar/Lucky Orange para analytics

### **Ferramentas**

- **Gravação:** OBS Studio (tela + webcam)
- **Analytics:** Google Analytics/Mixpanel
- **Feedback:** Typeform/Google Forms
- **Comunicação:** Google Meet/Zoom

## 📈 Plano de Execução

### **Fase 1: Testes Internos (Semana 1)**
- **Objetivo:** Validar setup técnico e protocolo
- **Participantes:** 3-5 pessoas (familiares/amigos)
- **Foco:** Funcionalidades técnicas e usabilidade básica

### **Fase 2: Testes com Público-Alvo (Semana 2)**
- **Objetivo:** Validar hipóteses de negócio
- **Participantes:** 10-15 usuários do público-alvo
- **Foco:** Experiência completa e feedback qualitativo

### **Fase 3: Análise e Iteração (Semana 3)**
- **Objetivo:** Sintetizar aprendizados e planejar melhorias
- **Atividades:**
  - Análise quantitativa dos dados
  - Síntese de insights qualitativos
  - Priorização de melhorias
  - Plano de ação para iteração

## 📋 Checklist de Preparação

### **Técnico**
- [ ] Servidor backend rodando (FastAPI)
- [ ] Frontend buildado e otimizado
- [ ] Dados de teste criados
- [ ] Analytics configurado
- [ ] Formulários de feedback prontos

### **Operacional**
- [ ] Script de recrutamento preparado
- [ ] Calendário de sessões organizado
- [ ] Incentivos definidos e disponíveis
- [ ] Protocolo de teste documentado

### **Comunicação**
- [ ] Posts de recrutamento prontos
- [ ] Email de confirmação preparado
- [ ] Briefing para moderadores definido

## 🎯 Critérios de Sucesso

### **Sucesso Mínimo**
- 8/10 usuários completam todas as tarefas principais
- SUS Score médio >65
- Tempo de carregamento <3s
- Feedback qualitativo identifica 2-3 pontos de melhoria

### **Sucesso Ótimo**
- 9/10 usuários completam todas as tarefas
- SUS Score médio >75
- Tempo de carregamento <2s
- Feedback positivo sobre conceito geral
- Insights claros para roadmap de produto

## 📊 Template de Relatório

### **Estrutura do Relatório Final**
1. **Resumo Executivo:** Principais achados e recomendações
2. **Métricas Quantitativas:** Gráficos e estatísticas
3. **Análise Qualitativa:** Temas recorrentes e citações
4. **Problemas Identificados:** Lista priorizada por impacto
5. **Recomendações:** Plano de ação para melhorias
6. **Próximos Passos:** Roadmap baseado nos resultados

---

**Data de Criação:** 02/11/2025
**Status:** 🟡 PRONTO PARA EXECUÇÃO
**Responsável:** Equipe de Produto</content>
<parameter name="filePath">c:\repo\projetos\meu-pdi\docs\plano-testes-usuario-portal-aluno.md