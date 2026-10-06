# Plano de Orquestração: Aba "Minuto com Deus" (Devocional Estilo Livro Impresso)

> **Referência Visual:** Baseado fielmente na diagramação editorial da imagem do livro devocional enviada pelo usuário (cabeçalho de data compacta, título em caixa alta, versículo no topo direito, sidebar em moldura curva com frase curta de pensador cristão/filósofo, contador do dia do ano `279/365`, leitura bíblica complementar `†`, linhas de anotações pautadas e texto com letra capitular *Drop Cap*).

---

## 🎯 1. Visão Geral e Identidade

1. **Nome da Nova Experiência:** **"Minuto com Deus"** (Subtítulo: *Devocional Diário*).
   - Substitui a nomenclatura anterior "Café com Deus Pai".
   - Botão de navegação por abas atualizado para: `⏱️ Minuto com Deus` (Badge: *Devocional Diário*).
2. **Proposta Visual e Editorial:**
   - Em vez de cartões de dashboard convencionais, a aba renderiza uma **página de livro devocional impresso de alta qualidade** (*Book Page Canvas*).
   - Fundo com textura suave de papel nobre / encorpado (marfim/creme `#fcfbf7` em modo clássico; obsidiana suave com tinta âmbar luminosa no modo escuro).
   - Tipografia de livro com tons terrosos, canela e café queimado (`#78350f`, `#92400e`, `#b45309`) idênticos à paleta da publicação física.

---

## 📐 2. Anatomia e Diagramação da Página (Fiel à Imagem)

A página será dividida nas seguintes zonas diagramadas com precisão:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 06 | OUT                                                     NOVOS COMEÇOS  │  <-- Cabeçalho da Página
├──────────────────────────┬──────────────────────────────────────────────────┤
│                          │ "Mudaste o meu pranto em dança... eu te darei   │  <-- Versículo do Dia
│   [ SELO CIRCULAR ]      │ graças para sempre."                             │      (Itálico + Serif)
│   Minuto com Deus        │                                   SALMOS 55.22   │  <-- Referência
│                          ├──────────────────────────────────────────────────┤
│ ┌──────────────────────┐ │                                                  │
│ │ As cicatrizes geram  │ │ █   á alguns anos, quando passei por aquele      │  <-- DROP CAP (H gigante)
│ │ em nós força para    │ │ █   momento difícil, achei que tudo estava       │      + Texto corrido em
│ │ vencer um dia de     │ │ perdido. Mas o Pai vê além das aparências...     │      prosa devocional
│ │ cada vez.            │ │                                                  │      profunda e sensível
│ │                      │ │ Às vezes a vida parece quebrar nossos planos ao  │
│ │ @cslewis             │ │ meio. Mas Deus transforma perdas em novos        │
│ ├──────────────────────┤ │ começos. A forma como enxergamos as circunstâncias│
│ │ DEVOCIONAL 365       │ │ muda tudo quando olhamos com os olhos da fé.     │
│ │ 279/365              │ │                                                  │
│ ├──────────────────────┤ │ Talvez hoje você esteja segurando pedaços de um  │
│ │ LEITURA BÍBLICA †    │ │ sonho. Mas o Senhor sussurra: "Eu estou          │
│ │ 1 PEDRO 5.6-11       │ │ multiplicando." Confie e dê o próximo passo.     │
│ └──────────────────────┘ │                                                  │
│                          │                                                  │
│ ANOTAÇÕES                │                                                  │
│ ───────────────────────  │                                                  │
│ ───────────────────────  │                     [ ✦ ]                        │  <-- Selo de rodapé
│ ───────────────────────  │                                                  │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### Componentes Detalhados:

1. **Cabeçalho Superior da Página:**
   - **Canto Esquerdo:** Data compacta do dia (ex: `06 | OUT`, `05 | OUT`), calculada dinamicamente a partir do estudo selecionado.
   - **Canto Direito:** Título do devocional em caixa alta com espaçamento nobre de letras (`NOVOS COMEÇOS`, `CARGA DE RUPTURA`, `DESCANSO E SUSTENTO`).
2. **Versículo Bíblico em Destaque:**
   - Posicionado no topo direito, ao lado do selo.
   - Tipografia em itálico com aspas refinadas e serifa clássica.
   - Referência bíblica alinhada à direita em versalete/caixa alta (`SALMOS 55.22`), **rigorosamente conectada ao versículo do dia**.
3. **Coluna Lateral Esquerda (Sidebar Editorial em Moldura Curva):**
   - **Selo Circular da Marca:** Emblema circular elegante no topo com acabamento de anel terroso e tipografia "Minuto com Deus".
   - **Moldura Arqueada (Bordas arredondadas):**
     - **Frase Curta para o Dia:** Pensamento curto e impactante de pensador cristão ou filósofo conectado à mensagem (ex: C.S. Lewis, Agostinho, Tim Keller, Kierkegaard, Bonhoeffer). Em negrito terroso (`#92400e`).
     - **Assinatura do Autor:** Com arroba ou nome do autor (ex: `@cslewis`, `@timkeller`).
     - **Linha Divisória Sutil.**
     - **Indicador do Dia do Ano:** Rótulo `DEVOCIONAL 365` e contagem `279/365` calculada dinamicamente para o dia exato do ano.
     - **Leitura Bíblica Complementar:** Rótulo `LEITURA BÍBLICA †` com cruz latina estilizada e a passagem sugerida para aprofundamento (ex: `1 PEDRO 5.6-11` ou `MATEUS 11.28-30`).
   - **Bloco de Anotações Pessoais (Abaixo da moldura):**
     - Título: `ANOTAÇÕES` em caixa alta e serifa sóbria.
     - Linhas pautadas horizontais de caderno/diário onde o leitor pode digitar e salvar reflexões com persistência automática no `localStorage`.
4. **Coluna Principal Direita (Texto do Devocional):**
   - **Letra Capitular (*Drop Cap*):** A primeira letra do primeiro parágrafo estilizada em caixa alta clássica, ocupando 3 linhas de altura, exatamente como o "H" da foto enviada.
   - **Corpo do Texto:** 3 a 4 parágrafos reflexivos, afetuosos e bem diagramados, com espaçamento generoso e leitura confortável.
   - **Selo de Fechamento da Página:** Pequeno adorno decorativo circular no rodapé inferior.
5. **Barra Inferior de Utilidades & Compartilhamento:**
   - Botão **"Copiar Devocional Formatado"** (gera texto pronto para WhatsApp ou anotações).
   - Botão **"Compartilhar no WhatsApp"** (link direto com emoji e formatação).
   - Indicador de status de gravação do diário de anotações.

---

## 🗂️ 3. Mapeamento de Arquivos e Alterações

| Arquivo | Responsabilidade | Alterações Principais |
|---|---|---|
| `web/index.html` e `projeto_limpo_git/web/index.html` | Estrutura Markup | Renomear aba para "Minuto com Deus"; substituir cards antigos pelo container de página impressa `.minuto-book-page` com cabeçalho, versículo superior, sidebar curva com frase, dia `279/365`, leitura complementar `†`, pauta de anotações e coluna de texto com drop cap. |
| `web/style.css` e `projeto_limpo_git/web/style.css` | Design System & CSS | Estilos da folha de livro `.minuto-book-page`, grid editorial de 2 colunas, moldura curva da sidebar, `.drop-cap` estilizado, linhas pautadas interativas `.notebook-lines`, selo circular e compatibilidade com os temas Claro e Escuro. |
| `web/app.js` e `projeto_limpo_git/web/app.js` | Lógica & Interatividade | Função `obterDiaDoAno(data)`, `formatarDataCompacta(data)`, renderizador `renderizarMinutoComDeus(data)`, suporte à edição e persistência nas linhas de anotação, e gerador de mensagem para compartilhamento. |
| `web/data.js` e `projeto_limpo_git/web/data.js` | Dados Históricos | Atualização dos dados dos estudos bíblicos com a estrutura `minutoComDeus` (título em caixa alta, frase curta, autor, dia do ano, leitura complementar e texto devocional com capitular). |
| `src/prompts.py` | Prompt IA | Atualização do prompt para geração de novos estudos com os campos editoriais de "Minuto com Deus". |
| `src/storage.py` | Persistência & Exportação | Atualização do parser de markdown e fallbacks para garantir a estrutura `minutoComDeus` em todos os estudos. |

---

## 👥 4. Distribuição de Especialistas na Fase 2 (Strict Orchestration)

Conforme o protocolo do `/orchestrate`, após a aprovação deste plano, 3 agentes especialistas atuarão:

1. **`frontend-specialist`**:
   - Construir o markup semântico em `index.html` e estilização editorial em `style.css` com foco na experiência de página de livro físico, drop cap e linhas pautadas.
2. **`backend-specialist`**:
   - Implementar os cálculos matemáticos do dia do ano em `app.js`, estruturar os dados em `data.js`, atualizar `prompts.py` e `storage.py`, e sincronizar arquivos com `projeto_limpo_git`.
3. **`test-engineer`**:
   - Validar a alternância entre abas, renderização responsiva em desktop e mobile, persistência do diário de anotações e executar scripts de validação (`lint_runner.py`).

---

## ⏸️ CHECKPOINT DE APROVAÇÃO

✅ **Plano criado: `plano-minuto-com-deus.md`**

Você aprova o plano acima para iniciarmos a implementação? (Y/N)
- **Y**: Iniciar implementação imediatamente com os especialistas
- **N**: Informar ajustes desejados no plano
