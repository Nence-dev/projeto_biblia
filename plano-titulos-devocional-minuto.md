# Plano de Orquestração: Títulos Contextuais & Leituras Complementares ("Minuto com Deus")

> **Baseado nas Imagens de Referência do Devocional Físico:**
> - **Exemplo 1 (06/OUT - João 7.37,38 - Rios de água viva):** Título: **`INESGOTÁVEL`** | Frase: *"Só Deus pode satisfazer o anseio mais íntimo da sua alma."* | Leitura Bíblica: Lista vertical com 6 passagens canônicas sobre sede/fonte.
> - **Exemplo 2 (05/OUT - Apocalipse 2.2-4 - Perda do primeiro amor):** Título: **`DE VOLTA AO PRIMEIRO AMOR`** | Frase: *"Lembre-se de onde você caiu e volte ao primeiro amor."* | Leitura Bíblica: Lista vertical com 6 passagens canônicas sobre restauração do amor/perseverança.

---

## 🎯 Objetivo da Tarefa

Substituir o título estático/genérico (como *"NOVOS COMEÇOS"*) por **títulos de forte impacto contextual nascidos diretamente do coração do texto bíblico do dia**, além de permitir a exibição da **lista vertical de passagens complementares** na moldura lateral conforme o padrão visual das duas páginas reais.

---

## 📋 Diagnóstico e Regras de Negócio

### 1. Regra de Criação de Títulos (Extração Exegética & Emocional)
O título posicionado no canto superior da página deve ter de **1 a 4 palavras em CAIXA ALTA** e expressar a síntese máxima do versículo:
- **Salmos 55:22** (Entregar preocupações / Deus sustenta / justo não cai) ➔ **`SUSTENTO INABALÁVEL`** (ou `ELE TE SUSTENTARÁ`)
- **Judas 1:22** (Ter misericórdia dos que duvidam) ➔ **`O ABRIGO DA MISERICÓRDIA`** (ou `MISERICÓRDIA PARA QUEM DUVIDA`)
- **Salmos 51:10** (Cria em mim um coração puro) ➔ **`A PUREZA DO CORAÇÃO`** (ou `CORAÇÃO NOVO`)
- **Provérbios 4:23** (Guarda o teu coração, pois dele procedem as fontes da vida) ➔ **`A GUARDA DO CORAÇÃO`**
- **Romanos 8:1** (Nenhuma condenação há para os que estão em Cristo) ➔ **`LIVRES DA CONDENAÇÃO`**

### 2. Formato de Múltiplas Leituras Complementares
Na imagem do livro, a seção `LEITURA BÍBLICA †` lista de 4 a 6 passagens em cascata vertical:
```
LEITURA BÍBLICA †
APOCALIPSE 22.17
JEREMIAS 2.13
SALMOS 36.9
JOÃO 4.13,14
ISAÍAS 55.1
ISAÍAS 44.3
```
O modelo de dados e o frontend devem suportar tanto uma string única quanto uma lista/array de passagens bíblicas ou texto com quebras de linha, renderizando-as empilhadas com elegância na moldura arqueada.

---

## 🏗️ Frentes de Implementação

### 1. Backend & Inteligência de Prompts (`src/prompts.py` e `src/storage.py`)
- **`src/prompts.py`:** Atualizar o prompt `PROMPT_DERIVACAO_MINUTO_COM_DEUS` com diretrizes explícitas e os exemplos de João 7:37 (`INESGOTÁVEL`) e Apocalipse 2:4 (`DE VOLTA AO PRIMEIRO AMOR`), proibindo termos genéricos e instruindo a IA a gerar uma lista de 4 a 6 referências correlacionadas em `leiturasComplementares`.
- **`src/storage.py`:** Aprimorar o parser para extrair adequadamente o título temático e a lista de leituras complementares, com mapeamento inteligente de fallback baseado na referência e gênero literário caso o estudo venha de arquivo anterior.

### 2. Base de Dados Web (`web/data.js` e `projeto_limpo_git/web/data.js`)
- **Estudo 2026-10-06 (Salmos 55:22):**
  - Título: **`SUSTENTO INABALÁVEL`**
  - Frase do dia: *"Você não foi desenhado para carregar o peso do mundo sozinho; entregue o fardo a Quem sustenta o universo."*
  - Leituras complementares: `1 PEDRO 5.7`, `MATEUS 11.28-30`, `SALMOS 68.19`, `FILIPENSES 4.6,7`, `ISAÍAS 41.10`.
- **Estudo 2026-10-05 (Judas 1:22):**
  - Título: **`O ABRIGO DA MISERICÓRDIA`**
  - Frase do dia: *"A misericórdia não descarta quem está vacilando; ela estende a mão para curar."*
  - Leituras complementares: `LUCAS 15.11-24`, `MATEUS 12.20`, `ROMANOS 14.1`, `GÁLATAS 6.1,2`, `1 TESSALONICENSES 5.14`.
- Demais estudos do histórico receberão títulos e listas bíblicas sob medida.

### 3. Interface e Renderização (`web/app.js`, `web/style.css` e HTML)
- **`web/app.js`:**
  - `obterDadosMinutoComFallback()`: enriquecida para gerar títulos contextuais precisos para cada versículo do histórico.
  - `renderizarConteudoMinuto()`: renderizar a lista de passagens em bloco vertical estilizado (cada referência em uma linha própria com espaçamento elegante).
- **`web/style.css`:**
  - Ajustar `.reading-ref` e `.minuto-meta-reading` para suportar lista de múltiplas referências verticais com tipografia refinada e sem quebra indesejada.

---

## 👥 Especialistas Envolvidos (Mínimo de 3 Agentes)

| Agente | Responsabilidade |
|---|---|
| **`project-planner`** | Estruturação das regras de geração contextual de títulos e plano de entrega. |
| **`backend-specialist`** | Ajuste dos prompts em `src/prompts.py` e extração de metadados em `src/storage.py`. |
| **`frontend-specialist`** | Layout de múltiplas leituras em cascata, tipografia e renderização em `app.js` e `style.css`. |
| **`test-engineer`** | Validação de consistência de dados, ausência de títulos genéricos e integridade de carregamento. |
