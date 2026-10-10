# Plano: Migração para Gemini 3.6 Flash & Substituição de Referências Teológicas

> **Documento de Planejamento de Orquestração**
> **Slug:** `atualizacao-gemini-teologos`
> **Projeto:** `Projeto_Biblia / projeto_limpo_git`
> **Data:** 2026-10-09

---

## 1. Overview
Adequação do motor de geração de estudos bíblicos e devocionais diários em `projeto_limpo_git` após notificação de descontinuação do modelo `gemini-3.5-flash` para substituição oficial pelo `gemini-3.6-flash`. Paralelamente, atualização editorial da geração da "Palavra do Dia / Minuto com Deus / Café com Deus Pai": remoção definitiva de referências a `@juniorrostirola` e enriquecimento das citações com pensadores e teólogos clássicos e contemporâneos de peso (ex: C.S. Lewis, Dietrich Bonhoeffer, Charles Spurgeon, A.W. Tozer, John Stott, Martinho Lutero, Santo Agostinho, Tim Keller).

---

## 2. Project Type
**BACKEND / DATA PIPELINE (Python + GitHub Actions + Web Showcase estático)**

---

## 3. Success Criteria
1. **Configuração e Fallback do Modelo**:
   - `GEMINI_MODEL` atualizado para `gemini-3.6-flash` como padrão em `src/config.py`, `.env`, `.env.example`, `estudo_diario.yml` e `README.md`.
   - `MODELOS_PADRAO_FALLBACK` em `src/llm_client.py` inclui `gemini-3.6-flash` com alta prioridade.
2. **Substituição Editorial da "Palavra do Dia"**:
   - Prompts de sistema e derivação em `src/prompts.py` desvinculados de `@juniorrostirola`.
   - Inserção de diretrizes para teólogos e pensadores renomados da história da igreja e do pensamento cristão, correlacionados ao teor bíblico do texto.
   - Fallbacks em código (`src/storage.py` e `web/app.js`) atualizados com teólogos contextualizados (ex: A.W. Tozer, Charles Spurgeon, C.S. Lewis).
   - Estudos já gerados em `estudos/*.md` que continham a referência atualizados com pensadores coerentes com as narrativas (Horatio Spafford, Eric Liddell/Martinho Lutero, Dietrich Bonhoeffer).
   - Re-exportação do arquivo `web/data.js` via `exportar_todos_estudos_para_web_data()`, garantindo consistência total do frontend.
3. **Validação & Testes**:
   - Toda a suíte de testes unitários (`pytest`) passa com 100% de sucesso sem regressões.

---

## 4. Tech Stack & Ferramentas
- **Linguagem**: Python 3.11+
- **SDK LLM**: `google-genai` (com fallback para `google-generativeai`)
- **Automação**: GitHub Actions (`.github/workflows/estudo_diario.yml`)
- **Frontend de Visualização**: Vanilla JS / HTML (`web/app.js`, `web/data.js`)
- **Testes**: `pytest`

---

## 5. File Structure & Arquivos Afetados
```
projeto_limpo_git/
├── .env.example                                      # Atualização do modelo padrão
├── .env                                              # Chave e modelo ativo local
├── README.md                                         # Documentação do modelo ativo
├── .github/workflows/estudo_diario.yml               # Variável padrão no CI
├── src/
│   ├── config.py                                     # GEMINI_MODEL fallback default
│   ├── llm_client.py                                 # MODELOS_PADRAO_FALLBACK
│   ├── prompts.py                                    # Diretrizes e exemplos sem juniorrostirola
│   └── storage.py                                    # Fallbacks de frases e re-exportação
├── web/
│   ├── app.js                                        # Fallback no client-side
│   └── data.js                                       # Base JSON gerada dos estudos
├── estudos/
│   ├── 2026-10-06_joao_14_27.md                      # Autor da frase -> pensador/autor histórico
│   ├── 2026-10-07_colossenses_3_23.md                # Autor da frase -> pensador/autor histórico
│   └── 2026-10-08_tiago_5_16.md                      # Autor da frase -> pensador/autor histórico
└── tests/
    └── test_storage.py                               # Ajuste em fixture de teste
```

---

## 6. Task Breakdown

### Tarefa 1: Migração do Modelo LLM para `gemini-3.6-flash`
- **Agente:** `backend-specialist`
- **Skill:** `@clean-code`, `@python-patterns`
- **Prioridade:** P0
- **Dependências:** Nenhuma
- **INPUT:** Arquivos `src/config.py`, `src/llm_client.py`, `.env`, `.env.example`, `.github/workflows/estudo_diario.yml`, `README.md`.
- **OUTPUT:** Modelo padrão definido como `gemini-3.6-flash`, adicionado à lista de fallback prioritário.
- **VERIFY:** Inspeção das variáveis e teste de importação de `config.py` e `llm_client.py`.

### Tarefa 2: Reformulação dos Prompts e Critérios da "Palavra do Dia"
- **Agente:** `backend-specialist`
- **Skill:** `@clean-code`
- **Prioridade:** P1
- **Dependências:** Tarefa 1
- **INPUT:** `src/prompts.py`
- **OUTPUT:** Eliminação de qualquer menção a `@juniorrostirola`. Diretrizes orientando a geração de frases de impacto baseadas em teólogos e pensadores clássicos e reformados (C.S. Lewis, Charles Spurgeon, Dietrich Bonhoeffer, A.W. Tozer, John Stott, Agostinho, Martinho Lutero, Tim Keller).
- **VERIFY:** `grep -i "juniorrostirola" src/prompts.py` retorna zero ocorrências.

### Tarefa 3: Atualização dos Fallbacks de Código e Dados Históricos
- **Agente:** `backend-specialist`
- **Skill:** `@clean-code`
- **Prioridade:** P1
- **Dependências:** Tarefa 2
- **INPUT:** `src/storage.py`, `web/app.js`, `estudos/2026-10-06_joao_14_27.md`, `estudos/2026-10-07_colossenses_3_23.md`, `estudos/2026-10-08_tiago_5_16.md`, `tests/test_storage.py`.
- **OUTPUT:**
  - `src/storage.py` e `web/app.js` utilizam teólogos reconhecidos (ex: `@awtozer`, `@charlesspurgeon`).
  - Estudos históricos ajustados com os autores das narrativas/teologias (ex: Horatio Spafford, Eric Liddell / Martinho Lutero, Dietrich Bonhoeffer).
  - Execução de `exportar_todos_estudos_para_web_data()` para atualizar `web/data.js`.
- **VERIFY:** `grep -i "juniorrostirola" projeto_limpo_git` não encontra nenhuma ocorrência de código ou dado ativo.

### Tarefa 4: Verificação da Suíte de Testes e Integridade
- **Agente:** `test-engineer`
- **Skill:** `@testing-patterns`, `@verify-changes`
- **Prioridade:** P2
- **Dependências:** Tarefas 1, 2, 3
- **INPUT:** Repositório completo `projeto_limpo_git`.
- **OUTPUT:** Execução completa de `pytest` com todos os 35+ testes passando.
- **VERIFY:** `pytest` com exit code 0.

---

## 7. Phase X: Final Verification
- [x] Nenhum resquício de `juniorrostirola` em código ativo (`src/`, `web/`, `estudos/`).
- [x] `gemini-3.6-flash` configurado em `src/config.py`, `src/llm_client.py`, `.env`, `.env.example`, `.github/workflows/estudo_diario.yml` e `README.md`.
- [x] `web/data.js` regenerado com dados atualizados.
- [x] Execução da suíte de testes `pytest` sem falhas (35/35 testes aprovados).

## ✅ PHASE X COMPLETE
- Model Migration: ✅ `gemini-3.6-flash` ativo
- Theologians Refinement: ✅ Pensadores e teólogos consagrados vinculados tematicamente
- Tests: ✅ 35 passed
- Date: 2026-10-09
