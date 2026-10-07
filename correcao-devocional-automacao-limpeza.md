# Plano de Correção e Limpeza: Automação do Estudo Diário, Devocional Completo e Limpeza de Código

**Status:** Aguardando Aprovação do Usuário (Fase 1 - Planejamento)  
**Task Slug:** `correcao-devocional-automacao-limpeza`  
**Escopo:** `projeto_limpo_git` e raiz do projeto  
**Data:** 07/10/2026  
**Agentes Responsáveis:** `project-planner`, `explorer-agent`, `backend-specialist`, `devops-engineer`, `test-engineer`

---

## 1. Visão Geral do Problema e Diagnóstico

### 1.1 Por que o devocional de hoje foi enviado "resumido"?
O usuário recebeu a seguinte mensagem de 1 frase:
> *"Amensagem de Colossenses 3:23 nos resgata: 'Tudo o que fizerem, façam de todo o coração, como para o Senhor, e não para os homens,'. O Senhor nos convida a descansar na Sua fidelidade soberana para cada instante deste dia."*

**Causa Raiz Identificada:**
1. **Bug Crítico de Regex com o Emoji `⏱️` em `src/storage.py`:**
   - Em `converter_estudo_markdown_para_dict_web()` e `parse_estudo_markdown()`, o regex usado para capturar o bloco devocional era:
     `r"##\s*[⏱️☕]?\s*(?:Devocional\s+)?(?:Minuto com Deus|Café com Deus Pai)..."`
   - O emoji `⏱️` no padrão Unicode é composto por **dois code points**: `\u23f1` (cronômetro) + `\ufe0f` (seletor de variação).
   - O caractere de classe `[⏱️☕]?` em Python consome apenas **um** code point (`\u23f1`), deixando o segundo (`\ufe0f`) solto. Como `\ufe0f` não é espaço (`\s`), a expressão falhava **sempre** que o cabeçalho continha `⏱️`.
2. **Captura Silenciosa de Erros de JSON:**
   - Em caso de quebras de linha em strings ou falha de parse no JSON retornado pela LLM, o `try...except` executava `pass` silenciosamente sem tentar recuperação nem extrair a prosa da história.
3. **Ativação do Fallback de Frase Estática:**
   - Ao não encontrar nem `minuto_com_deus` nem `cafe_com_deus_pai`, o código caía em um fallback hardcoded em `src/storage.py` (linha 651):
     `f"A mensagem de {referencia} nos resgata: \"{versiculo_texto}\". O Senhor nos convida a descansar..."`
   - Esse texto estático sobrescrevia o devocional completo no `web/data.js` e na interface.

### 1.2 Por que o workflow não rodou automaticamente no horário certo hoje?
1. **Atraso da Fila do Agendador do GitHub Actions (`schedule`):**
   - No workflow `.github/workflows/estudo_diario.yml`, o agendador estava configurado para `cron: '23 8 * * *'` (08:23 UTC = 05:23 horário de Brasília).
   - A fila de runners gratuitos do GitHub sofreu um **atraso de mais de 7 horas** (o job só começou a rodar às 15:38 UTC = 12:38 BRT).
2. **Modelo Gemini 404 e Falta de Idempotência Segura:**
   - A variável padrão `GEMINI_MODEL: gemini-3.5-flash` tenta um modelo que não existe na API do Google, gerando erros 404 iniciais e consumindo tempo para alternar para outros modelos.
   - O comando no GitHub Actions usava `python main.py --force` sem verificar se o estudo já havia sido gerado com sucesso, correndo o risco de sobrescrever dados caso houvesse retentativas.

### 1.3 Presença de Arquivos e Código Não Utilizados em `projeto_limpo_git`:
Identificados arquivos de teste pontual e scripts descartáveis deixados na pasta do projeto limpo:
- `testar_atos1725.py` (script pontual de teste)
- `testar_joao1427.py` (script pontual de teste)
- `teste_atos_17_25_resultado.md` (resultado descartável de teste)
- `visualizar_teste_web.py` (script pontual de teste local)
- `gerar_hoje.py` (duplicação desnecessária de `main.py`)
- Fallbacks hardcoded e mocks mortos em `src/storage.py`.

---

## 2. Plano de Ação em Fases

### Fase 1: Correção do Mecanismo de Devocional (Garantir 100% Completo e Vivo)
1. **Refatorar o Parser em `src/storage.py`:**
   - Reescrever a regex de captura de blocos devocionais para ser tolerante a quaisquer emojis e variações de cabeçalho:
     `r"##[^\n]*(?:Minuto com Deus|Café com Deus Pai)[\s\S]*?```(?:json)?\s*([\s\S]*?)\s*```"`
   - Adicionar parser resiliente de JSON com sanitização de quebras de linha em literais de string (usando regex para corrigir `\n` não escapados antes de `json.loads`).
   - Implementar fallback de extração de história caso o bloco JSON falhe: extrair automaticamente os parágrafos de texto da seção devocional.
   - **Eliminar definitivamente a frase de fallback de 1 linha** que gerava o resumo indesejado.
2. **Validação Rigorosa em `src/cli.py` e `src/llm_client.py`:**
   - Garantir que `gerar_devocional_narrativo` utilize uma instrução de sistema focada especificamente no formato devocional (e não o prompt de 5 etapas teológicas, evitando confusão de contexto na IA).
   - Caso o devocional gerado venha vazio ou menor que 200 caracteres, realizar **retentativa automática imediata** antes de salvar o arquivo markdown.
   - Bloquear o salvamento de devocionais vazios ou truncados.

### Fase 2: Blindagem da Automação e Execução Pontual (GitHub Actions & Crons)
1. **Otimização do Workflow `.github/workflows/estudo_diario.yml`:**
   - Atualizar o modelo padrão de fallback para `gemini-2.5-flash` ou `gemini-2.0-flash` (evita 404 e respostas lentas).
   - Adicionar **múltiplas janelas de acionamento de cron** na madrugada/início da manhã:
     - `17 8 * * *` (05:17 BRT)
     - `47 8 * * *` (05:47 BRT)
     - `17 9 * * *` (06:17 BRT)
   - Tornar o comando do runner inteligente: se o estudo da data de hoje já existir e contiver todas as seções e devocional completo, encerra imediatamente sem duplicar tokens. Se a run anterior atrasou ou falhou, a próxima recupera automaticamente.
2. **Gatilho de Alta Precisão (Zero Delay):**
   - Documentar e fornecer o comando curl/webhook para disparo pontual via cron externo (ex.: cron-job.org chamando `POST /repos/Nence-dev/projeto_biblia/actions/workflows/estudo_diario.yml/dispatches`), garantindo início em menos de 10 segundos pontualmente às 06:00 BRT.

### Fase 3: Limpeza Completa de Código e Arquivos Não Utilizados em `projeto_limpo_git`
1. **Remoção de Arquivos Descartáveis:**
   - Deletar `testar_atos1725.py`
   - Deletar `testar_joao1427.py`
   - Deletar `visualizar_teste_web.py`
   - Deletar `teste_atos_17_25_resultado.md`
   - Deletar `gerar_hoje.py` (usar exclusivamente `main.py`)
2. **Limpeza Interna de Código em `src/storage.py`:**
   - Remover código morto, variáveis não usadas e blocos de fallback obsoletos.
   - Manter apenas funções ativas e necessárias para o ciclo de vida do estudo e exportação web.

### Fase 4: Regeneração e Atualização do Estudo de Hoje (Colossenses 3:23)
1. **Regenerar o estudo completo de hoje (07/10/2026):**
   - Gerar o estudo de Colossenses 3:23 com o devocional completo nos 4 movimentos (incluindo história real/terceiro, ganho narrativo, tensão e aplicação pastoral).
   - Reexportar `web/data.js` para que a interface web e o compartilhamento WhatsApp contenham o devocional rico e detalhado.
2. **Executar Testes de Validação:**
   - Rodar a suíte de testes com `pytest` para certificar que todos os parsers, scrapers e formatos estão 100% funcionais.

---

## 3. Matriz de Agentes Envolvidos

| Agente | Papel e Responsabilidade |
|---|---|
| `project-planner` | Mapeamento, estruturação do plano e gestão do ciclo de aprovação |
| `explorer-agent` | Auditoria forense no código, inspeção de commits e diagnóstico de bugs |
| `backend-specialist` | Correção dos parsers em `storage.py`, prompts em `prompts.py` e fluxo CLI |
| `devops-engineer` | Ajustes e blindagem de pontualidade no workflow `.github/workflows/estudo_diario.yml` |
| `test-engineer` | Execução dos testes automatizados e verificação de regressão |

---

## 4. Critérios de Aceite

1. [ ] Regex do devocional em `storage.py` captura perfeitamente qualquer cabeçalho com emoji sem falhar.
2. [ ] O texto devocional nunca mais recorre à frase estática de 1 linha.
3. [ ] `estudo_diario.yml` configurado com múltiplos agendamentos e modelo válido `gemini-2.5-flash`.
4. [ ] Todos os 5 arquivos descartáveis de teste removidos de `projeto_limpo_git`.
5. [ ] O estudo de Colossenses 3:23 (07/10/2026) atualizado em `estudos/` e `web/data.js` com o devocional vivo e completo.
6. [ ] Todos os testes unitários passando.
