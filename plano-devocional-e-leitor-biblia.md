# Plano: Redesign da Aba Devocional (Minuto com Deus) & Leitor Bíblico Completo

> **Documento de Planejamento de Orquestração**
> **Objetivo:** 
> 1. Implementar o novo design da aba Devocionais (antigo Minuto com Deus) fiel à nova imagem de referência (hero com lanterna a óleo e Bíblia antiga, sidebar com bússola e relógio de bolso antigo, anotações pautadas, e coluna principal com drop cap iluminado, callout de Escritura, aplicação prática com ramo dourado, outros estudos em 3 cards horizontais e navegação anterior/próximo).
> 2. Implementar a aba "Bíblia" com um Leitor Bíblico completo e funcional, permitindo escolher testamento, livro e capítulo para leitura confortável e imersiva.

---

## 🏛️ Visão Arquitetural & Componentes

```
┌────────────────────────────────────────────────────────────────────────┐
│ NAVBAR: Sola Scriptura † | Início | Estudos | Devocionais* | Bíblia*   │
└────────────────────────────────────────────────────────────────────────┘
          │                                              │
          ▼ (Aba Devocionais)                            ▼ (Aba Bíblia)
┌───────────────────────────────────┐          ┌───────────────────────────────────┐
│ Hero: Lanterna & Bíblia           │          │ Seletor Canônico: Testamento/Livro│
│ "Sustento Inabalável"             │          │ & Seletor de Capítulos            │
│ "Entregue suas preocupações..."   │          │ Controles de Fonte (A- / A+)      │
├─────────────────┬─────────────────┤          ├───────────────────────────────────┤
│ Sidebar (30%):  │ Leitura (70%):  │          │ Leitor de Texto Bíblico Completo: │
│ 1. Foto Bússola │ 1. Título & Tag │          │ - Versículos numerados            │
│    + Relógio    │ 2. Versículo    │          │ - Cópia rápida com referência     │
│    + Leitura 365│ 3. Drop Cap "T" │          │ - Modo parágrafo e versículo      │
│ 2. Anotações    │ 4. Callout 2Tm3 │          │ - Busca por termo / versículo     │
│    Pautadas     │ 5. Aplicação    │          └───────────────────────────────────┘
│ 3. Minuto diário│ 6. Outros Salmos│
│                 │ 7. Nav Ant/Próx │
└─────────────────┴─────────────────┘
```

---

## 📋 Fases de Execução

### Fase 1: Assets Gráficos & Vetoriais Dedicados
- [ ] Criar vetor cinematográfico `web/assets/hero_devocional_lantern.svg` com a composição da lanterna a óleo clássica acesa sobre mesa de madeira ao lado da Bíblia sagrada encadernada em couro escuro.
- [ ] Criar vetor/composição artística `web/assets/compass_watch.svg` com a bússola dourada antiga e o relógio de bolso clássico lado a lado para o topo da sidebar.
- [ ] Criar ícone de ramo de oliveira / broto para o card de Aplicação Prática.
- [ ] Espelhar todos os assets em `projeto_limpo_git/web/assets/`.

### Fase 2: Estrutura HTML (`web/index.html` e `projeto_limpo_git/web/index.html`)
- [ ] **Aba Devocionais (`#view-cafe` / `#view-devocional`):**
  - Adicionar o Hero acolhedor com lanterna e título monumental *Sustento Inabalável*.
  - Estruturar a coluna esquerda: Card 1 (imagem bússola/relógio + citação + Devocional 365 com barra de progresso + lista de 5 leituras bíblicas), Card 2 (Anotações pautadas de caderno + botão dourado `Salvar Anotação`), Card 3 (Banner *Um minuto diário* com botão seta).
  - Estruturar a coluna direita: Tag `ESTUDO EXPOSITIVO / DEVOCIONAL DIÁRIO`, Versículo com barra dourada à esquerda, Prosa com Drop Cap `T` iluminado, Box callout de 2 Timóteo 3:16 com aspas duplas, Card Aplicação Prática com ícone de ramo e botão `Refletir sobre isso →`, Linha com 3 cards de *Outros Estudos sobre Salmos*, e Botões de navegação inferior (`‹ Estudo Anterior` e `Próximo Estudo ›`).
- [ ] **Aba Bíblia (`#view-biblia`):**
  - Transformar o link `Bíblia` na navbar em botão interativo de aba `#tab-btn-biblia`.
  - Criar o container `#view-biblia` com:
    - Barra de ferramentas do leitor (Seletor de Testamento, Livro, Capítulo, Versão, Controles de zoom tipográfico `A-` e `A+`).
    - Palco de leitura com cabeçalho monumental do Livro/Capítulo e versículos estruturados e interativos.
    - Modal/gaveta de seleção rápida de livros (Pentateuco, Históricos, Poéticos, Profetas, Evangelhos, Epístolas).

### Fase 3: Estilização Visual (`web/style.css` e `projeto_limpo_git/web/style.css`)
- [ ] Estilos do Hero Devocional com iluminação de lanterna e tipografia nobre.
- [ ] Estilos da Sidebar Devocional (foto da bússola/relógio, barra dourada de progresso 279/365, pauta de caderno para anotações).
- [ ] Estilos da Prosa Devocional (Drop Cap monumental clássico, barra dourada vertical no versículo, callout suave, card de aplicação com ramo).
- [ ] Grid de 3 cards horizontais para *Outros Estudos sobre Salmos* e barra de paginação anterior/próximo estudo.
- [ ] Estilos do Leitor Bíblico:
  - Layout limpo, sem ruído visual, focado na leitura da Escritura.
  - Tipografia de leitura `65-75ch`, números de versículo em expoente discreto e ouro velho.
  - Realce de versículo ativo ao clicar e botão flutuante para copiar versículo.
  - Responsividade total para smartphones e tablets.

### Fase 4: Lógica & Dados (`web/app.js`, `web/bible-data.js` e espelhos)
- [ ] Integrar banco de dados bíblico em português (`bible-data.js`) com livros canônicos e capítulos completos para leitura offline instantânea.
- [ ] Implementar a navegação da aba `biblia` no roteador do `app.js` (`trocarAba("biblia")`).
- [ ] Implementar as funções do leitor: `carregarCapituloBiblia(livro, capitulo)`, mudar tamanho de fonte, copiar versículo.
- [ ] Conectar os dados dinâmicos da aba Devocional para atualizar conforme a data selecionada no histórico (título, versículo, leitura complementar, texto e anotação).
- [ ] Conectar os botões `‹ Estudo Anterior` e `Próximo Estudo ›` para navegar entre as datas.

### Fase 5: Validação, Testes e Verificação
- [ ] Validar a renderização local via `read_url_content` no servidor `http://localhost:8000/`.
- [ ] Verificar a alternância fluida entre as 3 abas principais: *Estudos Expositivos*, *Devocionais*, e *Bíblia*.
- [ ] Assegurar 100% de paridade de código entre `web/` e `projeto_limpo_git/web/`.

---

## 👥 Matriz de Especialistas (Orquestração AG Kit)
1. `project-planner`: Elaboração deste plano arquitetural e verificação de dependências.
2. `frontend-specialist`: Implementação da interface visual fiel à imagem de referência e do Leitor Bíblico.
3. `test-engineer`: Verificação da execução no navegador, acessibilidade e integridade funcional.
