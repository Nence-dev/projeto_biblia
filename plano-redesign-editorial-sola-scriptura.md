# Plano de Implementação: Redesign Editorial "Sola Scriptura"

> **Objetivo:** Reformular o design visual e a experiência de leitura do **Projeto Bíblia & Teologia Expositiva** com base estrita no layout editorial nobre da referência visual enviada pelo usuário, eliminando de vez elementos artificiais e adotando uma direção de arte cinematográfica, limpa, sóbria e teológica.

---

## 🎨 1. Decomposição Visual da Referência (Direção de Arte)

A imagem fornecida apresenta o ápice do design editorial teológico moderno (nível *Crossway*, *The Gospel Coalition*, *Desiring God*):

| Componente | Especificação Visual da Referência |
| :--- | :--- |
| **Navbar Superior** | Fundo escuro fosco translúcido (`rgba(17, 15, 13, 0.95)`). Logo com cruz dourada em moldura sutil, marca **SOLA SCRIPTURA** com subtítulo *TEOLOGIA EXPOSITIVA & DEVOCIONAL*. Menu central: *Início*, *Estudos Expositivos* (com sublinhado dourado elegante), *Devocionais / Minuto com Deus*, *Bíblia*, *Sobre*. Campo de busca arredondado à direita com ícone de lupa. |
| **Hero Cinematográfico** | Banner escuro com imagem de fundo de alta resolução de montanhas ao entardecer com uma Bíblia antiga em couro sobre rochas iluminada por luz dourada suave. Vinheta escura à esquerda garantindo legibilidade absoluta. Tag superior: `ESTUDO EXPOSITIVO ——`. Título monumental em serifa clássica de época com destaque sutil em ouro velho (`o sustentará;`). Referência com ícone de livro: `Salmos 55:22`. |
| **Área Editorial de Leitura** | Transição suave para um fundo claro editorial/papiro nobre (`#faf8f4` no modo claro, couro nobre `#161412` no modo escuro). Breadcrumb superior discreto (`Início > Estudos Expositivos > Salmos 55:22`). |
| **Coluna de Leitura (70%)** | Marcador de capítulo `CAPÍTULO I ——` em versalete dourada. Título da seção `O Contexto Histórico & Narrativo` em serifa encorpada e preta. Texto com altura de linha generosa (`1.78`), margens de leitura confortáveis (68ch). |
| **Callout de Citações Bíblicas** | Caixa estilizada com fundo creme suave (`#f7f2e8`), aspas duplas douradas decorativas `“`, texto da Escritura em itálico serifado clássico e referência canônica ao final (`2 Timóteo 3:16`). |
| **Sidebar Direita (30%)** | 1. **Card "SOBRE ESTE ESTUDO":** Metadados em lista (Livro/Capítulo, Tema, Tipo, Duração de leitura) com ícones minimalistas de traço fino.<br>2. **Card "APLICAÇÃO PRÁTICA" (Destaque Escuro):** Card contrastante em preto/carvão com ícone dourado, pergunta provocativa de reflexão pessoal e botão dourado arredondado `Refletir sobre isso →`.<br>3. **Card "OUTROS ESTUDOS SOBRE SALMOS":** Lista com mini-thumbnails de paisagens (Salmo 23, Salmo 91, Salmo 121) e setas sutis.<br>4. **Card de Citação/Frase de Impacto:** Bloco creme com aspas douradas e filete inferior. |
| **Rodapé de Fechamento** | Faixa preta sutil com versículo em itálico centralizado: *"Toda Escritura é inspirada por Deus..."* (`2 Timóteo 3:16`). |

---

## 🏗️ 2. Arquitetura Técnica e Mapeamento de Componentes

### 2.1. Estrutura HTML (`web/index.html` e `projeto_limpo_git/web/index.html`)
1. **Nova Barra de Navegação (`.site-navbar`):**
   - Logo à esquerda: Ícone da Cruz Sagrada Latina dentro de moldura dourada sutil + Tipografia `SOLA SCRIPTURA` / `TEOLOGIA EXPOSITIVA & DEVOCIONAL`.
   - Links centrais de navegação com indicador ativo (`.nav-link.is-active`).
   - Alternador de abas integrado (*Estudos Expositivos* | *Minuto com Deus*).
   - Input de busca com ícone de lupa e atalho visual (`Ctrl+K`).
   - Botões utilitários discretos à direita (Tema Claro/Escuro, Histórico de Estudos).

2. **Hero Section Dinâmico (`.editorial-hero`):**
   - Imagem de fundo panorâmica cinematográfica com sobreposição de gradiente vinheta escura à esquerda.
   - Tag em versalete com travessão: `ESTUDO EXPOSITIVO ——`.
   - Título monumental com realce dourado inteligente.
   - Referência bíblica com ícone de livro clássico.

3. **Grade Principal Editorial (`.editorial-layout-container`):**
   - Breadcrumb: `<nav class="editorial-breadcrumb">Início &gt; Estudos Expositivos &gt; <span id="breadcrumb-ref">Salmos 55:22</span></nav>`.
   - Grade de duas colunas:
     - **Coluna de Conteúdo (`.editorial-main-content`):**
       - Seções dinâmicas renderizadas com `CAPÍTULO I ——`, `CAPÍTULO II ——`, títulos serifados nobres.
       - Caixas de citação com aspas douradas (`.editorial-quote-box`).
       - Drop cap e tipografia ajustada.
     - **Coluna Lateral (`.editorial-sidebar`):**
       - Card 1: `.card-about-study` (Livro, Tema, Tipo, Tempo de Leitura).
       - Card 2: `.card-practical-app` (Fundo escuro contrastante, ícone de montanha, pergunta do dia, botão de reflexão).
       - Card 3: `.card-related-studies` (Estudos relacionados com thumbnails de acervo).
       - Card 4: `.card-quote-banner` (Frase teológica de impacto).

4. **Preservação de Todas as Funcionalidades Existentes:**
   - Alternância fluida para a aba **Minuto com Deus** (que mantém sua experiência de livro devocional com o relógio de bolso antigo hunter case).
   - Gaveta lateral de Histórico de Estudos (`#historico-drawer`).
   - Leitor de Áudio TTS com voz humanizada.
   - Caixa de Diário Espiritual / Anotações do dia.
   - Compartilhamento para WhatsApp e Copiar Mensagem.
   - Modo Noturno / Modo Claro com paleta fosca.

---

## 🎨 3. Especificação de Design Tokens (`DESIGN.md` e `web/style.css`)

### Paleta de Cores "Sola Scriptura":
- **Preto Carvão / Base Noturna:** `#110f0d` (fundo navbar e hero) e `#171513` (card de aplicação prática).
- **Papiro / Fundo Claro Editorial:** `#fbf9f5` (fundo principal) e `#f4eee3` (cards suaves).
- **Ouro Velho Sóbrio:** `#c9a050` (acentos nobres, tags de capítulo, aspas) e `#b8860b` (bordas sutis).
- **Texto Principal (Modo Claro):** `#1a1714` (títulos) e `#2e2822` (leitura fluida).
- **Texto Secundário / Metadados:** `#6d6458` (legível, contraste AA/AAA).
- **Superfícies Modo Noturno:** `#1a1714` (fundo de leitura), `#231f1b` (cards), `#eae3d2` (texto).

### Tipografia:
- **Títulos Hero e Display:** `'Cinzel'`, serif com versalete clássica.
- **Títulos de Capítulos e Seções:** `'Playfair Display'` ou `'Cinzel'`, peso 800, tracking equilibrado.
- **Corpo Editorial:** `'Georgia'`, `'Merriweather'`, 1.12rem, altura de linha 1.78.
- **UI & Metadados:** `'Plus Jakarta Sans'`, `'Inter'`, pesos 600 e 700.

---

## 📋 4. Plano de Fases da Orquestração

### FASE 1: Planejamento & Aprovação (Estado Atual)
- [x] Levantamento de todos os requisitos visuais da imagem de referência.
- [x] Criação deste plano de arquitetura e design `{task-slug}.md`.
- [ ] **Aprovação explícita do usuário (Y/N).**

### FASE 2: Implementação com Agentes Especializados (Após Aprovação)
1. **`frontend-specialist`:**
   - Reestruturar `web/index.html` e `projeto_limpo_git/web/index.html` com o novo Navbar Sola Scriptura, o Hero Cinematográfico, o breadcrumb e a grade editorial de 2 colunas com os 4 cards laterais.
   - Atualizar `web/style.css` e `projeto_limpo_git/web/style.css` com todo o design system da referência (grid, tipografia, card escuro de aplicação prática, thumbnails, caixas de citação).
   - Ajustar `web/app.js` e `projeto_limpo_git/web/app.js` para preencher os metadados dos cards laterais (Livro/Capítulo, Tema, Tempo estimado de leitura, Estudos relacionados).
2. **`test-engineer`:**
   - Executar verificações de integridade sintática e testes funcionais (busca, histórico, alternância de abas, cópia e salvamento).
   - Validar responsividade mobile e tablet.
3. **`documentation-writer` & `orchestrator`:**
   - Atualizar `DESIGN.md` e emitir relatório de orquestração unificado.
