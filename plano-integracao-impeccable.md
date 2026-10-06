# 🏛️ Plano de Orquestração: Integração do Impeccable no Projeto Bíblia

## 1. Diagnóstico do Plugin Impeccable
O plugin **Impeccable** (`v4.5.0`), instalado em `.agent/skills/impeccable/`, é uma suíte avançada de **direção de arte e engenharia de UI/UX para frontend** voltada para criar designs fora da curva ("out-of-distribution craft").

### Principais Pilares do Impeccable Identificados:
1. **Contratos Canônicos de Design (`PRODUCT.md` e `DESIGN.md`):**
   - Estruturação de tokens em YAML (cores, tipografia, espaçamentos, elevação, componentes) e especificação canônica das regras visuais do projeto.
2. **Modo de Superfície: `mode-read` (Superfície de Compreensão e Leitura Sagrada):**
   - Princípios de diagramação editorial, inspirados em manuscritos de referência e tratados acadêmicos.
   - Foco na coluna de leitura com medida áurea de **65–75 caracteres por linha (`measure: 65-75ch`)**, contraste rigoroso e sem ruídos por trás do texto.
3. **Padrão de Qualidade `craft-floor` (Regras Inegociáveis de Bom Design):**
   - **Fim dos containers preguiçosos:** Rejeita cards genéricos repetitivos (bento boxes artificiais).
   - **Ícones Autorais:** Substituição de emojis soltos no texto por SVGs próprios, refinados e consistentes no mesmo traço.
   - **Superfícies Nativas do Navegador:** Theming da seleção de texto (`::selection`), barra de rolagem clássica em latão, e anéis de foco (`:focus-visible`) temáticos.
   - **Eliminação de Halos e Neon:** Sombras suaves com offset e difusão natural em substituição a brilhos falsos.
4. **Comandos Especializados de Refino:**
   - `typeset` (hierarquia de fontes e contraste semântico), `layout` (ritmo vertical e respiração), `delight` (microinterações memoráveis e respeitosas), `adapt` (responsividade repensando a experiência mobile) e `audit` (conformidade WCAG AA/AAA).

---

## 2. Equipe de Agentes Orquestrados (Mínimo de 3 Agentes)

| Agente | Responsabilidade Específica |
| :--- | :--- |
| 🧠 **`@[project-planner]`** | Mapeamento dos artefatos canônicos (`PRODUCT.md` e `DESIGN.md`), definição do escopo em 4 fases e aplicação das diretrizes do `mode-read`. |
| 🎨 **`@[frontend-specialist]`** | Implementação dos tokens em `DESIGN.md`, substituição de emojis por ícones SVG sagrados, estilização de superfícies do navegador (`::selection`, custom scrollbar), e ajuste tipográfico (`measure: 65-75ch`). |
| 🧪 **`@[test-engineer]`** | Auditoria com base no `craft-floor` e `audit.md` (contraste de cor WCAG AA/AAA, responsividade `adapt.md`, usabilidade de teclado e paridade absoluta com `projeto_limpo_git`). |

---

## 3. Roteiro de Implementação em 4 Fases

### Fase 1: Fundação Canônica de Design System (Impeccable Base)
- [ ] **Criar `PRODUCT.md` na raiz:** Registrar a verdade duradoura do produto (público, nicho teológico reformado/expositivo, propósito devocional diário, preservação reverente da Palavra).
- [ ] **Criar `DESIGN.md` na raiz:** Definir a tabela de tokens normativos (YAML) com a paleta sagrada (ouro velho, latão usinado, papiro, velino, couro e carvão), escalas tipográficas (Cinzel, Cormorant Garamond, Georgia, Plus Jakarta Sans) e elevações sem neon.

### Fase 2: Aplicação do `mode-read` & Tipografia Editorial (`typeset`)
- [ ] **Ajuste da Medida de Leitura (`65–75ch`):** Configurar `max-width: 70ch` na prosa do Estudo Expositivo e no texto devocional do Minuto com Deus para conforto visual máximo.
- [ ] **Ritmo Vertical Clássico:** Garantir que o espaçamento superior de títulos seja sempre maior que o inferior (hierarquia natural de leitura).
- [ ] **Substituição de Emojis por Ícones SVG Reais:** Trocar emojis soltos (ex: `⏱️`, `📖`, `📱`, `💡`) no cabeçalho, botões e badges por ícones SVG desenhados no mesmo traço e na cor de latão/ouro velho.

### Fase 3: Detalhes de Alto Nível (`craft-floor` & `delight`)
- [ ] **Superfícies Nativas Temáticas:**
  - `::selection`: fundo em tom ouro velho suave com texto de alto contraste.
  - Scrollbar clássica: trilha e polegar estilizados em harmonia com o tema (modo pergaminho e modo escuro).
  - `:focus-visible`: foco nítido e elegante sem anel azul padrão do navegador.
- [ ] **Microinterações Refinadas (`delight`):**
  - Feedback visual nobre ao copiar versículo ou salvar anotações.
  - Suavização das transições entre a aba de Estudo Expositivo e Minuto com Deus.

### Fase 4: Auditoria Técnica & Adaptação Responsiva (`audit` & `adapt`)
- [ ] **Contraste de Acessibilidade:** Verificar contraste >= 4.5:1 para todo o corpo de texto e >= 3:1 para títulos em ambos os temas.
- [ ] **Adaptação Mobile Impeccable:** Garantir que no celular o relógio e os blocos de leitura não pareçam miniaturas espremidas, mas uma leitura confortável e fluida.
- [ ] **Paridade 100%:** Espelhar todas as melhorias para `projeto_limpo_git/`.

---

## 4. Critérios de Sucesso
- [ ] Existência dos arquivos canônicos `PRODUCT.md` e `DESIGN.md` estruturados conforme a especificação do Impeccable.
- [ ] Tipografia de leitura ajustada para `65-75ch`, proporcionando experiência de códice e livro impresso.
- [ ] Zero emojis genéricos atuando como ícones de interface; 100% de ícones vetoriais SVG consistentes.
- [ ] Superfícies do navegador (`::selection`, scrollbar) totalmente integradas à paleta de arte.
- [ ] Paridade total entre a raiz e `projeto_limpo_git/`.
