# 📜 Plano de Orquestração: Mostrador Relógio no "Minuto com Deus" & Formato de Tratado Bíblico Contínuo (Fim do Bento Grid)

## 1. Visão Geral e Necessidade do Usuário
O usuário trouxe duas solicitações essenciais de design e usabilidade:
1. **Selo "Minuto com Deus" em formato de Relógio & Largura Total do Card Abaixo:**
   - O círculo deve crescer para ter **exatamente a mesma largura do card que fica abaixo dele** (largura de 100% da coluna lateral, ~265px a 270px).
   - Aplicar o conceito e a metáfora de **relógio clássico/antigo**: mostrador circular com marcadores de minutos/horas, numerais romanos clássicos (XII, III, VI, IX), ponteiros elegantes de latão/ferro forjado e o monograma/inscrição *"MINUTO COM DEUS"* no coração do mostrador.
2. **Substituição dos Cards em formato Bento Grid por Outro Formato:**
   - Eliminar a estrutura de "cards modulares soltos" (estilo Bento Box de dashboard tech moderno).
   - Adotar o formato de **Tratado Bíblico Contínuo / Códice Clássico de Estudo**:
     - O estudo expositivo passa a fluir como uma **obra encadernada contínua** (estilo Bíblia de Estudo clássica / Comentário Teológico de Genebra).
     - As seções deixam de ser caixas isoladas e tornam-se divisões textuais orgânicas unificadas em uma única folha/livro nobre, com elegantes linhas duplas de divisão, florões sacros (`— ❖ —`), capitulares e caixas de anotação integradas naturalmente à prosa.

---

## 2. Equipe de Agentes Orquestrados (Mínimo de 3 Agentes)

| Agente | Responsabilidade Específica |
| :--- | :--- |
| 🧠 **`@[project-planner]`** | Estruturação da arquitetura visual do relógio sagrado e definição do fluxo editorial contínuo (fim do bento grid). |
| 🎨 **`@[frontend-specialist]`** | Implementação do mostrador de relógio SVG/CSS responsivo (mesma largura do card abaixo) e reestruturação do Estudo Expositivo em formato de Tratado Contínuo no HTML e CSS. |
| 🧪 **`@[test-engineer]`** | Auditoria de responsividade (desktop, tablet, mobile), verificação de alinhamento entre o relógio e o card inferior, e paridade 100% entre a raiz e `projeto_limpo_git/`. |

---

## 3. Especificações Técnicas e de Design

### A. O Relógio Clássico "Minuto com Deus"
* **Dimensões & Alinhamento:**
  - O elemento `.minuto-badge-seal` passará a ter `width: 100%; aspect-ratio: 1; max-width: 265px; margin: 0 auto 1.5rem auto;`.
  - Terá rigorosamente a **mesma largura do card abaixo dele** (`.minuto-arched-card`), criando uma coluna perfeitamente alinhada e harmônica.
* **Componentes do Mostrador de Relógio:**
  - **Aro Externo:** Relevo em latão envelhecido / ouro velho fosco com borda usinada clássica.
  - **Trilha de Minutos & Horas:** Anel interno com 12 marcações (traços ou numerais romanos XII, III, VI, IX) e pequenos pontos para os minutos.
  - **Ponteiros Ornamentais:** Ponteiro de horas e ponteiro de minutos clássicos apontando para a hora sagrada da meditação.
  - **Centro do Mostrador:** O texto *"minuto COM DEUS"* gravado em tipografia nobre (Cinzel), com suave relevo seco.

### B. Novo Formato Editorial: Tratado Teológico Contínuo (Adeus Bento Grid)
* **Conceito Visual:**
  - Em vez de múltiplos retângulos flutuantes recortados (estilo Bento/Dashboard), a visualização de Estudo Expositivo será apresentada como um **Volume Contínuo / Livro de Teologia Aberto**.
* **Estrutura Unificada:**
  - Um único e imponente pergaminho/fólio contínuo (`.study-codex-volume`) que abriga a progressão do estudo:
    1. **Prólogo:** Contexto Histórico e Autoria.
    2. **Divisor Sacro:** Filete clássico com florão `— ❖ —`.
    3. **Exegese:** Anatomia do Texto & Termos Originais integrados no corpo do artigo.
    4. **Divisor Sacro:** `— ❖ —`.
    5. **Aplicação Prática:** Conexão com o cotidiano e a vida cristã.
    6. **Conexões Canônicas & Cristo:** Citações teológicas históricas e versículos correlacionados dispostos como notas de rodapé / cânon integrado.
    7. **Meditação & Diário:** Epílogo de reflexão pessoal com o diário espiritual incorporado ao fechamento da página.
  - A coluna lateral de Devocional Rápido e Sobre o Projeto acompanha a leitura como uma barra marginal de iluminura clássica.

---

## 4. Plano de Implementação nos Arquivos

1. **`web/index.html` e `projeto_limpo_git/web/index.html`:**
   - Atualizar o elemento `.minuto-badge-seal` com a marcação semântica do relógio (mostrador com marcas romanas, ponteiros clássicos e inscrição central).
   - Reestruturar o `#view-estudo`: substituir os cards bento isolados por um fólio contínuo com divisores sacros (`.study-codex-volume`).
2. **`web/style.css` e `projeto_limpo_git/web/style.css`:**
   - Adicionar estilos vetoriais e puramente CSS para o relógio antigo (aro em relevo, mostrador, marcadores, ponteiros, sem brilhos neon).
   - Fazer o relógio ocupar rigorosamente a largura total da coluna (idêntica ao card inferior).
   - Estilizar a leitura contínua de códice bíblico, eliminando o visual de bento grid modular.
3. **`web/app.js` e `projeto_limpo_git/web/app.js`:**
   - Garantir que as funções de renderização (`renderizarEstudoAtivo` e `renderizarConteudoMinuto`) injetem o conteúdo nas novas seções contínuas de forma transparente e responsiva.

---

## 5. Critérios de Aceite
- [ ] O círculo do Minuto com Deus possui exatamente a mesma largura do card arqueado abaixo dele.
- [ ] O círculo incorpora a metáfora visual de um relógio antigo clássico com ponteiros e marcadores.
- [ ] O Estudo Expositivo abandona o formato de cartões bento grid e adota o formato de tratado teológico contínuo com divisores clássicos.
- [ ] Nenhuma estética neon é utilizada; predomínio de tons de papiro, velino, couro e latão antigo.
- [ ] Paridade rigorosa entre o repositório raiz e `projeto_limpo_git/`.
