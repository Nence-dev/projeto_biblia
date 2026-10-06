---
name: Projeto Bíblia & Minuto com Deus
description: Sistema de design canônico para códice teológico expositivo e devocional editorial
colors:
  parchment-bg: "#fbf8f2"
  parchment-card: "#f4ede0"
  dark-bg: "#13100d"
  dark-surface: "#1c1814"
  dark-surface-elevated: "#241f1a"
  gold-primary: "#d4af37"
  gold-aged: "#b8860b"
  gold-amber: "#f59e0b"
  gold-soft: "#fef3c7"
  leather-coffee: "#2d1607"
  leather-deep: "#1a0c04"
  ink-primary-light: "#1c150c"
  ink-secondary-light: "#5a4835"
  ink-primary-dark: "#f5eedc"
  ink-secondary-dark: "#c7b79d"
  border-subtle-light: "rgba(140, 95, 25, 0.22)"
  border-subtle-dark: "rgba(212, 175, 55, 0.2)"
  border-gold: "#d4af37"
typography:
  display:
    fontFamily: "'Cinzel', Georgia, serif"
    fontWeight: 700
    letterSpacing: "0.04em"
  body:
    fontFamily: "'Georgia', serif"
    fontSize: "1.08rem"
    lineHeight: 1.75
  prose:
    fontFamily: "'Cormorant Garamond', Georgia, serif"
    fontSize: "1.2rem"
    lineHeight: 1.65
  ui:
    fontFamily: "'Plus Jakarta Sans', -apple-system, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
rounded:
  sm: "4px"
  md: "8px"
  lg: "16px"
  xl: "20px"
  full: "9999px"
spacing:
  xs: "0.25rem"
  sm: "0.5rem"
  md: "1rem"
  lg: "1.5rem"
  xl: "2.5rem"
  xxl: "3.5rem"
components:
  verse-card:
    backgroundColor: "{colors.parchment-card}"
    textColor: "{colors.ink-primary-light}"
    rounded: "{rounded.lg}"
    padding: "2.5rem 2rem"
  button-gold:
    backgroundColor: "{colors.gold-aged}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "0.6rem 1.2rem"
---

# Design System: Códice Sagrado & Minuto com Deus

## Overview
O sistema visual deste projeto foi desenhado para evocar a solenidade, beleza e reverência dos grandes volumes teológicos históricos (Bíblia de Genebra, códices renascentistas e comentários expositivos clássicos), em harmonia com o acolhimento pastoral e intimista do devocional diário *Minuto com Deus*.

Este projeto rejeita a estética de painéis modernos de tecnologia (dashboards SaaS com bento boxes soltos e brilhos fluorescentes) e adota a arquitetura de **livro aberto, leitura contínua e iluminuras de latão fosco**.

---

## Colors

### Paleta Primária (Pergaminho & Ébano)
- **`parchment-bg` (`#fbf8f2`)**: Fundo nobre em pergaminho clássico sob luz diurna.
- **`dark-bg` (`#13100d`)**: Fundo nobre em ébano/couro envelhecido sob modo escuro.
- **`parchment-card` (`#f4ede0`)**: Superfície de fólio em velino antigo.
- **`dark-surface` (`#1c1814`)**: Superfície escura de gabinete teológico.

### Metais & Acentos Nobres
- **`gold-primary` (`#d4af37`)**: Ouro clássico para capitulares e epígrafes sacras.
- **`gold-aged` (`#b8860b`)**: Latão usinado e ouro velho para aros, cantoneiras e botões.
- **`gold-amber` (`#f59e0b`)**: Âmbar quente para destaques e ponteiros de relógio.

### Tipografia & Tinta Caligráfica
- **Modo Claro:**
  - Título / Corpo Primário: `#1c150c` (tinta ferrogálica envelhecida).
  - Texto Secundário: `#5a4835` (sépia escuro).
- **Modo Escuro:**
  - Título / Corpo Primário: `#f5eedc` (tinta em papiro iluminado).
  - Texto Secundário: `#c7b79d` (âmbar acinzentado).

---

## Typography

### Fontes Autorizadas
1. **`Cinzel`**: Usada exclusivamente para títulos monumentais, cabeçalhos de capítulos (`CAPÍTULO I`, `EPÍLOGO`), numerais romanos do relógio e versículo de capa.
2. **`Georgia` / `Cormorant Garamond`**: Usada para a prosa teológica contínua, exegese, citações e texto devocional.
3. **`Plus Jakarta Sans`**: Usada apenas para controles de interface (rótulos de botões, tags de versículo, badges e wayfinding).

### Regra Áurea de Leitura (`measure: 65–75ch`)
O corpo da prosa expositiva e devocional respeita rigorosamente o limite de **65 a 75 caracteres por linha** (`max-width: 70ch`), garantindo ritmo natural aos olhos, respiração e conforto prolongado.

---

## Layout

### Estrutura Bimodal
1. **Visão Estudo Expositivo:**
   - Tratado Teológico Contínuo (`.study-codex-volume`) de fólio único.
   - Divisores sacros com florão (`— ❖ —`) entre seções.
   - Coluna lateral como margem de anotação com o Devocional Rápido e dados do cânon.
2. **Visão Minuto com Deus:**
   - Grade editorial clássica com proporção inspirada no livro impresso.
   - Coluna lateral de 265px comportando o Relógio Sagrado e o Card Arqueado em alinhamento vertical perfeito.
   - Coluna de leitura com letra capitular (Drop Cap) e parágrafos fluidos.

---

## Elevation & Depth

- **Zero Halos de Neon:** Proibição de bordas `box-shadow: 0 0 15px rgba(..., 1)`.
- **Sombras Físicas Suaves:** Sombras projetadas com desfoque suave (`drop-shadow(0 4px 10px rgba(0, 0, 0, 0.35))` e `box-shadow: 0 10px 28px rgba(45, 20, 5, 0.12)`).
- **Chanfros de Latão:** Gradientes radiais sutis simulando torneamento de metal.

---

## Shapes

- Cantoneiras de iluminura (`.codex-corner`) com 4px de raio e traço de 2px.
- Círculo de relógio clássico (`aspect-ratio: 1`) com mostrador usinado.
- Card arqueado com curvatura de 20px no topo evocando arcos arquitetônicos românicos/góticos.

---

## Components

### 1. Relógio de Bolso Antigo Aberto "Minuto com Deus" (Hunter Case Pocket Watch)
- Vetor SVG de alta precisão anatômica baseado em relógios de bolso de época do século XIX:
  - **Tampa Articulada Aberta (à esquerda):** Concha metálica com relevos e hachuras em gravura à pena, arabescos clássicos e inscrição entalhada de época em três níveis: `MINUTO` (versalete geométrica), `com` (itálico manuscrito de caligrafia clássica) e `DEUS` (caixa alta serifada em romano de pedra).
  - **Dobradiça Mecânica Central:** Pino usinado articulando tampa e caixa.
  - **Corpo do Relógio (à direita):** Argola oval (bow), coroa estriada de dar corda (winding crown) no topo, bisel usinado, mostrador em pergaminho seco com trilha completa de 60 minutos, numerais romanos de I a XII, ponteiros spade & leaf clássicos e pino central com acabamento em latão velho.
- **Posicionamento Superior:** Inicia no topo absoluto da grade editorial alinhado à primeira linha do devocional, eliminando qualquer vão ocioso. Acabamento 100% fosco e seco (zero neon).

### 2. Navbar Editorial "Sola Scriptura"
- **Logo & Badge:** Moldura quadrada com cruz latina dourada em relevo seco e tipografia clássica monumental `SOLA SCRIPTURA` acompanhada pelo subtítulo `TEOLOGIA EXPOSITIVA & DEVOCIONAL`.
- **Navegação Central:** Links com sublinhado/linha dourada horizontal indicadora de página ativa.
- **Busca em Pílula:** Campo de busca arredondado (`.navbar-search-pill`) com ícone de lupa e fundo escuro fosco de alta legibilidade.

### 3. Hero Cinematográfico (Bíblia nas Montanhas)
- Composição vetorial de alta resolução com relevos montanhosos ao entardecer dourado e Bíblia aberta sobre a rocha.
- Degradê lateral escuro para legibilidade tipográfica absoluta.
- Tag `ESTUDO EXPOSITIVO ——` com espaçamento generoso e título monumental com palavra-chave em destaque dourado quente (`.hero-word-accent`).
- Bloco canônico com ícone de livro e referência de Escritura.

### 4. Grade Editorial 70% Leitura / 30% Sidebar (4 Cards)
- **Coluna de Leitura (70%):** Capítulos romanos (`CAPÍTULO I ——`, `CAPÍTULO II ——`, etc.), parágrafos justificados fluidos e card callout monumental de Escritura (`.scripture-callout-card`) com aspas douradas `“`.
- **Sidebar Editorial (30%):**
  1. *Sobre Este Estudo:* Metadados (Livro, Tema, Tipo, Duração de leitura) com ícones vetoriais finos.
  2. *Aplicação Prática:* Card escuro contrastante com ícone de montanha e botão dourado de reflexão (`.btn-practical-action`).
  3. *Outros Estudos sobre Salmos:* Lista com mini-thumbnails de paisagens para Salmo 23, Salmo 91 e Salmo 121.
  4. *Citação Teológica:* Card com aspas douradas no topo e filete decorativo na base.

### 5. Faixa Inferior de Fechamento Editorial
- Faixa escura inferior com citação em itálico de 2 Timóteo 3:16 e selo da Reforma *Verbum Domini Manet in Aeternum*.

---

## Do's and Don'ts

### ✅ DO
- Usar ícones SVG autorais desenhados com o mesmo traço e cor.
- Manter a medida de leitura em `65–75ch`.
- Preservar mais espaçamento acima dos títulos do que abaixo deles.
- Dar feedback visual caloroso e respeitoso para ações do usuário (salvar, copiar).
- Harmonizar os modos Claro (papiro editorial) e Escuro (códice noturno) mantendo o contraste nobre.

### ❌ DON'T
- Nunca usar caixas bento grid avulsas para quebrar a leitura.
- Nunca usar cores neon ou brilhos fluorescentes.
- Nunca usar emojis genéricos de sistema (`⏱️`, `📱`, `📖`) como ícones de botões e navegação.
- Nunca usar cantos vivos sem chanfro em elementos clássicos de códice.
