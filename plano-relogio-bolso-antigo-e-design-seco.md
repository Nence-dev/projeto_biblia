# 📜 Plano de Orquestração: Relógio de Bolso Antigo Aberto, Alinhamento Superior & Estética Seca (Zero Neon)

## 1. Visão Geral e Necessidade do Usuário
O usuário apontou três pontos essenciais após análise da tela ativa (com base nas imagens fornecidas):
1. **Eliminar todos os brilhos e neons (Deixar "mais seco"):**
   - A interface ainda apresentava saturações e sombras com halos brilhantes (especialmente no modo escuro e no relógio circular).
   - Substituir a estética digital/brilhante por uma estética **seca, fosca e tátil**: papel pergaminho envelhecido, tinta ferrogálica/nanquim, gravura vintage à pena e metal em latão/bronze fosco sem reflexos fluorescentes.
2. **Alinhar o relógio e o card abaixo dele mais para cima:**
   - Na versão anterior, o `.minuto-verse-banner` ficava posicionado acima da grade principal, criando um enorme vão vazio escuro na coluna esquerda antes do relógio começar.
   - O relógio e o card abaixo dele devem iniciar imediatamente no topo da grade editorial, alinhados perfeitamente com a data e com o início do conteúdo da página.
3. **Novo Modelo: Relógio de Bolso Antigo Aberto com Tampa Gravada:**
   - Substituir o mostrador circular genérico por um **relógio de bolso antigo de colecionador (Hunter Case Pocket Watch)** inspirado diretamente na ilustração clássica fornecida:
     - **Corpo do Relógio:** Mostrador com coroa de dar corda e argola no topo, aro trabalhado em metal fosco com hachuras de gravura, mostrador seco com numerais romanos clássicos (I a XII), trilha de minutos e ponteiros ornamentais de época.
     - **Tampa Aberta articulada:** Tampa lateral conectada por dobradiça mecânica, exibindo em entalhe clássico a inscrição gravada:
       ***"MINUTO COM DEUS"*** com moldura de gravura e hachuras de época.

---

## 2. Equipe de Agentes Orquestrados (Mínimo de 3 Agentes)

| Agente | Responsabilidade Específica |
| :--- | :--- |
| 🧠 **`@[project-planner]`** | Estruturação da anatomia vetorial do relógio de bolso aberto e reorganização da grade editorial para eliminar o espaçamento superior ocioso. |
| 🎨 **`@[frontend-specialist]`** | Desenho do SVG do relógio de bolso antigo com tampa gravada *"MINUTO COM DEUS"*, reestruturação do HTML/CSS para mover o relógio para o topo e expurgação de todos os neons e brilhos em prol de tons secos e foscos. |
| 🧪 **`@[test-engineer]`** | Auditoria de layout (desktop e mobile), verificação de ausência de halos luminosos, alinhamento vertical com a coluna de leitura e paridade 100% com `projeto_limpo_git/`. |

---

## 3. Especificações Técnicas e de Design

### A. O Relógio de Bolso Antigo Aberto (Vetor SVG Nobre)
- **Visual:** Baseado no estilo litográfico/gravura à pena da referência clássica ("time hand drawn"):
  - **Argola e Coroa:** No topo do relógio (argola oval de latão com ranhuras de corda).
  - **Mostrador Principal:** Círculo interno em pergaminho/marfim seco com numerais romanos antigos (I, II, III, IV, V, VI, VII, VIII, IX, X, XI, XII), aro entalhado com hachuras manuais e ponteiros trabalhados de época.
  - **Tampa Articulada Aberta:** Tampa do relógio aberta lateralmente em ângulo com chanfro e hachuras internas, trazendo gravado no medalhão central:
    `MINUTO` / `com` / `DEUS` em tipografia nobre entalhada.
  - **Acabamento:** Traços secos em tinta carvão/latão queimado (`#3d2e1e` / `#231a12`), sem gradientes brilhantes de computador nem reflexos falsos.

### B. Alinhamento Superior Imediato (Fim do Vazio no Topo Esquerdo)
- Mover o `.minuto-verse-banner` (versículo do dia em itálico com referência) para o topo da coluna de leitura (`.minuto-story-col`), como abertura direta da meditação.
- A grade editorial (`.minuto-editorial-grid`) passa a começar logo abaixo do cabeçalho da página (`.minuto-page-header`).
- A coluna lateral esquerda (`.minuto-sidebar-col`), contendo o relógio de bolso e o card abaixo dele, passa a iniciar no topo da página, lado a lado com a data e o início do texto.

### C. Estética 100% Seca & Purga do Neon
- Substituir tons amarelos saturados (`#fef08a`, `#f59e0b`) por tons de ouro velho fosco e papiro seco (`#c9ad76`, `#9a7d46`, `#d1c7b7`).
- Eliminar sombras com desfoque sem deslocamento (`0 0 Xpx`).
- Deixar os cards e fundos com textura de papel encadernado fosco e couro curtido.

---

## 4. Plano de Alterações nos Arquivos

1. **`web/index.html` e `projeto_limpo_git/web/index.html`:**
   - Inserir a nova ilustração vetorial SVG do relógio de bolso antigo com tampa aberta gravada *"MINUTO COM DEUS"* no lugar do círculo anterior.
   - Reorganizar a hierarquia: reposicionar o banner do versículo para o topo da coluna de prosa devocional, permitindo que a coluna lateral suba até o alinhamento com a data.
2. **`web/style.css` e `projeto_limpo_git/web/style.css`:**
   - Remover todos os glows e halos (`box-shadow: 0 0 ...`, `text-shadow: 0 0 ...`).
   - Estilizar o relógio de bolso antigo mantendo traço de gravura seco e proporções alinhadas.
   - Ajustar o espaçamento do topo da sidebar para `margin-top: 0` e `padding-top: 0`.
3. **`PRODUCT.md` e `DESIGN.md`:**
   - Atualizar a especificação do componente de relógio para refletir o modelo de relógio de bolso antigo com tampa articulada.

---

## 5. Critérios de Aceite
- [ ] O modelo do relógio é um relógio de bolso antigo clássico aberto com coroa no topo e tampa aberta lateralmente.
- [ ] Na tampa aberta está gravado com nitidez clássica *"MINUTO COM DEUS"*.
- [ ] O relógio e o card abaixo dele estão alinhados bem mais para cima, sem o vão escuro no topo esquerdo.
- [ ] Todos os brilhos neon, halos e saturações artificiais foram eliminados em favor de um acabamento fosco e seco.
- [ ] Paridade rigorosa e absoluta mantida entre a raiz e `projeto_limpo_git/`.
