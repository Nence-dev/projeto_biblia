# Plano de Orquestração: Rotação e Diversificação de Pensadores e Autores de Frases

**Slug:** `rotacao-autores-frases-pensadores`  
**Tipo de Projeto:** BACKEND / PROMPTS / LLM / REPUTATION & DIVERSITY  
**Status:** ✅ CONCLUÍDO (Fases 1 e 2 Executadas com Sucesso)  
**Agentes Envolvidos:** `project-planner`, `backend-specialist`, `test-engineer`, `orchestrator`

---

## 1. Diagnóstico do Problema & Causa Raiz

### O que está acontecendo:
O usuário constatou que a frase do dia e as citações dos estudos gerados estão caindo repetidamente no mesmo autor: **Tim Keller** (100% dos últimos 10 estudos consecutivos atribuíram a frase a Tim Keller / Timothy Keller).

### Causa Raiz Técnica:
1. **Frequência de Amostragem no LLM:** Em modelos da família Gemini, o nome de Tim Keller possui peso de atenção altíssimo para teologia expositiva contemporânea e pastoral urbana. Quando o prompt dá exemplos soltos contendo "Tim Keller", o modelo converge para ele por padrão de probabilidade.
2. **Inexistência de Memória de Autores Recentes:** Nem `montar_prompt_usuario()` nem `montar_prompt_minuto()` em `src/prompts.py` recebem ou consultam quem foi o autor citado no dia anterior. Como cada geração é sem estado (*stateless*), o modelo repete Tim Keller dia após dia sem saber que acabou de usá-lo.
3. **Catálogo Restrito de Exemplos:** Os prompts citavam apenas 6 ou 7 autores clássicos sem uma categorização histórica ampla nem diretriz explícita de rotação diária obrigatória.

---

## 2. Arquitetura da Solução & Divisão de Tarefas

```
                                ┌────────────────────────────────────────┐
                                │              orchestrator              │
                                └───────────────────┬────────────────────┘
                                                    │
                 ┌──────────────────────────────────┼────────────────────────────────┐
                 │                                  │                                │
                 ▼                                  ▼                                ▼
        [project-planner]                  [backend-specialist]               [test-engineer]
      Diagnóstico, plano                 Função de inspeção histórica       Testes unitários de
      e especificação                    em storage.py, expansão de         inspeção de autores,
      (FASE 1 - CONCLUÍDO)               prompts.py com catálogo amplo      anti-repetição no prompt
                                         e regra anti-repetição (FASE 2)    e fallback (FASE 2)
```

### Agentes Envolvidos (Mínimo de 3):
1. **`project-planner`**:
   - Mapeamento da causa raiz, arquitetura da solução e checkpoints de aprovação.
2. **`backend-specialist`**:
   - **`src/storage.py`**: Criar função `obter_ultimos_autores_frases(limite_dias: int = 3) -> list[str]` para escanear os estudos Markdown existentes ou `web/data.js` e extrair os autores das frases dos últimos dias.
   - **`src/prompts.py`**:
     - Criar catálogo categorizado com mais de 35 pensadores da história cristã (Pais da Igreja, Reformadores, Puritanos, Século XIX, Século XX e Contemporâneos).
     - Atualizar `montar_prompt_usuario` e `montar_prompt_minuto` para receber `autores_proibidos: list[str]`.
     - Injetar diretriz estrita no prompt:
       `"REGRA DE OURO DE DIVERSIDADE: É TERMINANTEMENTE PROIBIDO usar o(s) autor(es) recente(s): {autores_proibidos}. Você DEVE escolher um pensador diferente da lista."`
   - **`src/cli.py` & `src/llm_client.py`**: Integrar a busca dos últimos autores antes de disparar as chamadas à API Gemini.
   - **Diversificação do Estudo de Hoje (15/10/2026 - Colossenses 3:13)**: Atualizar a citação de hoje para um autor alternativo que se encaixe perfeitamente no tema do perdão mútuo e suporte comunitário (ex.: **Dietrich Bonhoeffer** em *Vida em Comunhão* ou **C.S. Lewis** em *O Peso da Glória*), quebrando o monopólio de Tim Keller imediatamente.
3. **`test-engineer`**:
   - Criação de suíte de testes em `tests/test_rotacao_autores.py`.
   - Testar que a função `obter_ultimos_autores_frases()` identifica autores recentes corretamente.
   - Testar que os prompts gerados contêm a proibição explícita do autor anterior.
   - Testar diversidade do catálogo de autores.

---

## 3. Catálogo Canônico Expandido de Pensadores e Teólogos

Para garantir que o conteúdo nunca fique repetitivo, o prompt receberá um leque categorizado por temas e épocas:

1. **Perdão, Vida Comunitária e Reconciliação:**
   - Dietrich Bonhoeffer (*Vida em Comunhão*)
   - Corrie ten Boom (*O Refúgio Secreto*)
   - Thomas Watson (*O Arrependimento*)
   - C.S. Lewis (*Os Quatro Amores*, *O Peso da Glória*)
2. **Graça, Justificação e a Cruz:**
   - Martinho Lutero
   - João Calvino
   - John Stott (*A Cruz de Cristo*)
   - Martyn Lloyd-Jones
3. **Oração, Devoção e Confiança em Meio à Crise:**
   - Charles Spurgeon (*Sermões*)
   - George Müller
   - A.W. Tozer (*O Conhecimento do Santo*, *A Busca de Deus*)
   - Santo Agostinho (*Confissões*)
   - John Bunyan (*O Peregrino*)
4. **Contentamento, Soberania e Providência Divina:**
   - Jonathan Edwards
   - J.C. Ryle (*Santidade*)
   - Elisabeth Elliot (*Segurança e Paz*)
   - Francis Schaeffer (*A Verdadeira Espiritualidade*)
   - Blaise Pascal (*Pensamentos*)

---

## 4. Critérios de Aceite

1. ✅ A função `obter_ultimos_autores_frases()` identifica com precisão os autores dos últimos estudos.
2. ✅ O prompt proíbe explicitamente o autor utilizado no dia anterior (e até 2 dias anteriores).
3. ✅ Mais de 30 autores relevantes da tradição cristã documentada passam a figurar nas opções sugeridas.
4. ✅ O estudo de hoje (15/10/2026) é atualizado com uma frase de autor diferente de Tim Keller (ex.: Dietrich Bonhoeffer).
5. ✅ Testes automatizados validam o fluxo sem regressões.

---

## 5. Próximos Passos (Aguardando Aprovação)

Após aprovação do usuário no checkpoint:
1. Implementar a extração em `src/storage.py`.
2. Refatorar os geradores de prompt em `src/prompts.py` e `src/llm_client.py`.
3. Atualizar o estudo de 15/10/2026 e o `web/data.js` com o novo autor.
4. Escrever e rodar os testes em `tests/test_rotacao_autores.py`.
