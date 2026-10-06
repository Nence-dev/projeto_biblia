# Plano de Implementação: Devocional Vivo com Histórias Narrativas (Estilo "Café com Deus Pai")

> **Slug:** `plano-devocional-vivo-historias-narrativas`  
> **Data:** 06/10/2026  
> **Status:** Proposto para Aprovação (Fase 1 - Orchestration)  
> **Objetivo:** Transformar o texto do Devocional ("Minuto com Deus" / "Café com Deus Pai") de um resumo acadêmico/frio em um devocional vibrante, caloroso e visceral, guiado por histórias de terceiros (fatos reais marcantes ou narrativas bíblicas ricas em drama humano), seguindo fielmente a estrutura das páginas originais do "Café com Deus Pai".

---

## 1. Diagnóstico do Problema & Análise das Referências Visuais

### O Problema Atual:
O texto devocional gerado anteriormente em `minutoComDeus.textoDevocional` era apenas um parágrafo curto e genérico (gerado via template estático quando o modelo gerava apenas os 5 capítulos expositivos):
> *"O mundo tenta nos convencer de que a paz é encontrada quando todas as variáveis estão sob nosso controle... A paz de Cristo não depende do silêncio das ondas..."*

Faltava **vida, drama humano, narrativa e conexão visceral**.

### O Padrão das Imagens de Referência ("Café com Deus Pai" - Junior Rostirola):
Analisando as 3 imagens fornecidas pelo usuário:
1. **03 JUN - A Importância do Testemunho (Marcos 5:19):**
   - *Frase lateral:* "Em um mundo cheio de ódio, seja amor." `@juniorrostirola`
   - *História:* Começa com a queixa humana x contar bênçãos, traz uma canção antiga e relata uma história pessoal concreta (*"Certa vez, me perguntaram se eu era forte. Minha resposta foi que, onde termina a minha força, a força de Deus Pai começa a agir..."*).
2. **04 JUN - Ele Cuida de Você (1 Reis 17:13,14):**
   - *Frase lateral:* "Você acessa o milagre por meio da sua confiança em Deus." `@juniorrostirola`
   - *História:* O drama visceral da viúva de Sarepta — sem horizontes, com um punhado de farinha, um coração angustiado e o peso da morte iminente. Conecta a dor da viúva com o leitor no "último fio de esperança". Termina com chamada de ação: *"Confie, entregue e obedeça, para que o milagre aconteça"*.
3. **09 JUN - A Brevidade da Vida (Salmos 90:12):**
   - *Frase lateral:* "A vida é breve; aproveite-a com sabedoria!" `@juniorrostirola`
   - *História:* Dilemas reais de tragédias e sonhos interrompidos, desconstrução da necessidade de agradar aos outros, fechamento com intencionalidade.

---

## 2. Nova Arquitetura do Texto Devocional (Estrutura de 4 Movimentos)

Todo texto devocional passará a ter **4 parágrafos robustos e envolventes**, obrigatoriamente contendo:

1. **Movimento 1 — O Gancho Narrativo / A História Concreta:**
   - Abre com uma história real de terceiro (biografia cristã clássica, fato histórico comovente, ilustração real do cotidiano) OU uma narrativa bíblica com profunda textura e empatia humana (os sentimentos, a dor, o desespero e a surpresa dos personagens).
2. **Movimento 2 — A Tensão da Vida & O Ponto de Virada:**
   - Mostra o momento em que as forças humanas se esgotam e a verdade da Palavra de Deus intervém de forma surpreendente, desmontando o medo e restaurando o propósito.
3. **Movimento 3 — A Aplicação Pessoal no Coração do Leitor:**
   - Transição direta para o leitor: *"Quantas vezes você também se sentiu assim?"*, *"Talvez hoje você esteja diante de um cenário onde..."*. Mostra o acolhimento do Pai e a graça prática para o dia a dia.
4. **Movimento 4 — A Frase de Selamento & Desafio de Fé:**
   - Conclusão inspiradora, memorável e encorajadora em uma ou duas frases fortes que ecoam na mente do leitor ao longo do dia.

---

## 3. Plano de Engenharia e Alterações de Código

### A. Atualização dos Prompts do Gemini (`src/prompts.py`)
- Redefinir `PROMPT_DERIVACAO_MINUTO_COM_DEUS` e criar `PROMPT_DEVOCIONAL_CAFE_NARRATIVO`.
- Instruir explicitamente o Gemini a pesquisar/resgatar **histórias reais de terceiros, episódios biográficos inspiradores ou narrativas humanas bíblicas vívidas** relacionadas à temática do versículo do dia.
- Exigir o formato JSON estruturado com:
  - `titulo`: 1 a 4 palavras em caixa alta (ex: `A PAZ INABALÁVEL`, `ELE CUIDA DE VOCÊ`).
  - `fraseDoDia`: Pensamento curto e memorável para o card lateral.
  - `autorFrase`: `@juniorrostirola` ou pensador/autor correspondente.
  - `leiturasComplementares`: Array com 4 a 6 leituras bíblicas.
  - `historiaContexto`: Resumo da história/fato real utilizado.
  - `textoDevocional`: O texto completo nos 4 movimentos narrativos.

### B. Integração no Pipeline da API (`src/llm_client.py`)
- Adicionar o método `gerar_devocional_narrativo(...)` no `GeminiClient`.
- Chamar a geração do devocional narrativo tanto no fluxo principal quanto nas rotinas diárias.

### C. Persistência e Compilação (`src/storage.py`)
- No `salvar_estudo`: incluir a seção `## ⏱️ Devocional Minuto com Deus / Café com Deus Pai` com o JSON ou blocos formatados no Markdown.
- No `parse_estudo_markdown`: extrair o devocional narrativo completo gerado pela IA.
- Se o devocional não vier no Markdown (retrocompatibilidade), garantir uma biblioteca enriquecida com histórias reais para cada passagem.

### D. Atualização do Teste Local de João 14:27
- Aplicar a emocionante história real de **Horatio Spafford** (que em meio à perda devastadora de suas filhas no naufrágio do navio Ville du Havre no Atlântico, escreveu as palavras imortais sobre a paz de Cristo que vence a tempestade: *"Sou Feliz com Jesus / It Is Well with My Soul"*).
- Atualizar imediatamente `projeto_limpo_git/estudos/2026-10-07_joao_14_27.md` e `web/data.js` para que o teste local exiba a nova narrativa comovente no navegador.

### E. Garantia para a Geração Automática de Amanhã
- Sincronizar em `projeto_limpo_git` e testar com `main.py` e `gerar_hoje.py`.
- Fazer o commit e push para o repositório GitHub para que o cron das 03:23 execute a nova lógica com o Gemini.

---

## 4. Matriz de Agentes Envolvidos (Fase 2 - Mínimo 3 Agentes)

| Agente | Área de Foco | Responsabilidade |
|---|---|---|
| `project-planner` | Arquitetura | Elaboração do plano e orquestração do fluxo |
| `backend-specialist` | Python & Prompts | Implementação do novo prompt narrativo no Gemini, `llm_client.py` e `storage.py` |
| `frontend-specialist` | Interface Web | Refinamento da diagramação do devocional narrativo no leitor web |
| `test-engineer` | Validação | Teste de geração da API e validação do JSON e Markdown |

---

## 5. Checkpoint de Aprovação

Você aprova este plano para iniciarmos a implementação na Fase 2?
- **Y**: Iniciar a implementação imediatamente com os agentes especializados.
- **N**: Revisar ou ajustar algum ponto do plano.
