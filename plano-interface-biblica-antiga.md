# 📜 Plano de Orquestração: Interface Bíblica Antiga & Redesenho do "Minuto com Deus"

## 1. Visão Geral e Objetivos do Usuário
O usuário solicitou uma mudança fundamental de ambientação e arquitetura visual:
1. **Eliminar brilhos e efeitos neon:** Substituir cores fluorescentes e cianos modernos por uma identidade visual clássica de Bíblia antiga (tons de papiro, pergaminho envelhecido, couro nobre, ouro fosco envelhecido e tinta ferrogálica).
2. **Círculo do "Minuto com Deus" significativamente maior:** O selo circular atual (92px) está pequeno e discreto; deve se tornar um medalhão/selo imponente (140px a 160px), com anéis concêntricos clássicos e forte presença de encadernação histórica.
3. **Botões de alternância ao lado do botão de Histórico:** Mover os controles de troca entre "Estudo Expositivo" e "Minuto com Deus" da área intermediária para o cabeçalho superior (navbar), posicionando-os diretamente ao lado do botão de Histórico.
4. **Transformação total da interface no Minuto com Deus:** Ao clicar em "Minuto com Deus", toda a tela deve assumir a atmosfera devocional (ocultando o hero com o versículo duplo e cards exegéticos que pertencem exclusivamente ao Estudo Expositivo), oferecendo uma experiência imersiva de página de livro aberta.

---

## 2. Equipe de Agentes Orquestrados (Mínimo de 3 Agentes)

| Agente | Responsabilidade Específica |
| :--- | :--- |
| 🧠 **`@[project-planner]`** | Estruturação dos fluxos de navegação, tokens de design antigo e checklist de transição. |
| 🎨 **`@[frontend-specialist]`** | Implementação dos novos componentes de navegação na navbar, estilização sem neon no CSS, ampliação do selo circular e transição imersiva de layout via classes dinâmicas. |
| 🧪 **`@[test-engineer]`** | Validação da usabilidade responsiva (desktop e mobile), contraste WCAG para leitura em pergaminho/couro, ausência de efeitos neon e paridade entre raiz e `projeto_limpo_git/`. |

---

## 3. Especificação Detalhada da Mudança

### A. Paleta Clássica de Bíblia Antiga (Banimento do Neon)
* **Substituição de Tokens:**
  - Remover referências a ciano neon (`#38bdf8`, `rgba(56, 189, 248, ...)`) e glows fluorescentes.
  - Paleta Modo Pergaminho (Clássico Claro):
    - Fundo base: Papiro/pergaminho suave (`#f5efe6` e `#ebdcc9`).
    - Cartões e folhas: Velino natural (`#fbf8f2` com bordas sutis em tom de linho e couro `#c4b196`).
    - Tipografia: Tinta ferrogálica / carvão nobre (`#261e19` e `#4a3828`).
    - Destaques sacros: Ouro envelhecido (`#b8860b` / `#966f1e`) e rubi bíblico suave (`#8b2626`).
  - Paleta Modo Escuro (Códice Noturno / Biblioteca Antiga):
    - Fundo base: Carvalho escuro / couro encadernado envelhecido (`#14110e` e `#1c1713`).
    - Superfícies: Pergaminho escurecido pelo tempo (`#241e19` com bordas em latão escovado `rgba(184, 134, 11, 0.25)`).
    - Tipografia: Marfim antigo suave (`#e8dfcf` e `#c2b5a0`), sem qualquer reflexo azulado.
    - Destaques: Folha de ouro fosco (`#d4af37`), sem sombras de néon expansivas.

### B. Posicionamento dos Botões de Alternância na Navbar
* **Nova Organização da Barra Superior (`.navbar-actions`):**
  - Ao lado de `#btn-historico`, criar o grupo segmentado clássico:
    - Botão 1: `📜 Estudo Expositivo`
    - Botão 2: `⏱️ Minuto com Deus`
  - Estilização refinada: botões com acabamento em couro/pergaminho, cantos suavizados e indicação ativa em ouro antigo gravado, perfeitamente integrados com o botão de Histórico e de Áudio.
  - Remover a barra intermediária redundante (`.mode-navigation-bar`) que ficava abaixo do Hero, liberando o topo da página para maior clareza visual.

### C. Transição Completa da Interface (Modo Imersivo "Minuto com Deus")
* **Ocultação do Hero no Modo Minuto:**
  - O bloco `#hero-header` (com badges teológicos "Literatura de Sabedoria" e caixa iluminada) pertence ao Estudo Expositivo.
  - Ao alternar para "Minuto com Deus", o `#hero-header` e o `#view-estudo` são recolhidos, dando lugar exclusivo à folha de livro sagrado do devocional com seu próprio cabeçalho nobre (`06 | OUT` à esquerda e `SUSTENTO INABALÁVEL` à direita), versículo em destaque, moldura de citações e texto com letra capitular.
  - Adição de classe `is-mode-minuto` no `<body>` ou `.layout-wrapper` para harmonizar as margens e a textura de fundo.

### D. Selo Circular do "Minuto com Deus" Imponente e Ampliado
* **Aumento substancial do medalhão:**
  - Redimensionar de **92px** para **145px** a **155px**.
  - Ajustar a coluna lateral esquerda (`.minuto-sidebar-col`) de 215px para ~260px (com adaptação fluida em telas menores).
  - Design visual do selo:
    - Borda dupla em latão antigo / gravação de encadernação.
    - Círculo interno pontilhado em ouro antigo com ornamentação clássica.
    - Texto *"minuto com DEUS"* em tipografia Cinzel/serifada com kerning nobre e hierarquia nítida.

---

## 4. Plano de Execução em Arquivos

1. **`web/index.html` e `projeto_limpo_git/web/index.html`:**
   - Mover os botões `#tab-btn-estudo` e `#tab-btn-cafe` para dentro de `.navbar-actions` (ao lado de `#btn-historico`).
   - Remover a antiga tag `<nav class="mode-navigation-bar">`.
2. **`web/app.js` e `projeto_limpo_git/web/app.js`:**
   - Atualizar a função `alternarModoVisualizacao(modo)` para:
     - Gerenciar a visibilidade do `#hero-header` (exibir no estudo, ocultar no Minuto com Deus).
     - Adicionar/remover a classe `is-mode-minuto` no body.
     - Atualizar o estado visual ativo dos botões localizados na navbar.
3. **`web/style.css` e `projeto_limpo_git/web/style.css`:**
   - Eliminar tokens e regras de neon/ciano (`--accent-cyan`, glows exagerados).
   - Estilizar os novos botões de navegação na navbar com visual clássico.
   - Ajustar as dimensões do selo circular (`.minuto-badge-seal`) para 150px e estilizar seu interior.
   - Ajustar a largura da sidebar do devocional e a transição imersiva da página.

---

## 5. Critérios de Aceite
- [ ] Nenhum elemento da interface utiliza brilho neon ou ciano saturado; todas as cores remetem a pergaminho, couro, tinta e ouro envelhecido.
- [ ] Os botões de alternância ("Estudo Expositivo" e "Minuto com Deus") residem diretamente ao lado do botão de Histórico na barra superior.
- [ ] Ao clicar em "Minuto com Deus", o hero do estudo expositivo desaparece e a folha devocional assume o destaque absoluto da tela.
- [ ] O selo circular do Minuto com Deus é amplo (145-155px), nítido e visualmente imponente.
- [ ] 100% de paridade mantida entre o diretório raiz e `projeto_limpo_git/`.
