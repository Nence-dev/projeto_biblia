# Plano: Atualização e Sincronização com o GitHub

> **Documento de Planejamento de Orquestração**
> **Slug:** `atualizacao-github`
> **Projeto:** `Projeto_Biblia / projeto_limpo_git`
> **Data:** 2026-10-09

---

## 1. Overview
Sincronizar as alterações recentes (migração para `gemini-3.6-flash`, refinamento teológico dos devocionais sem `@juniorrostirola` e dados web atualizados) com o repositório remoto no GitHub (`https://github.com/Nence-dev/projeto_biblia.git`). Resolver o estado de rebase pendente no repositório local, garantir que nenhum segredo (`.env`) seja versionado, consolidar os commits semânticos e realizar o push para o GitHub.

---

## 2. Project Type
**DEVOPS / CI/CD (Git & GitHub Automation)**

---

## 3. Success Criteria
1. **Resolução Segura do Git**:
   - Resolver o estado de rebase pausado sem perda de alterações locais.
   - Confirmar que o arquivo `.env` (com API key) continua estritamente ignorado pelo `.gitignore`.
2. **Commit Semântico Estruturado**:
   - `git add` dos arquivos modificados:
     - Configurações e cliente: `src/config.py`, `src/llm_client.py`, `.env.example`
     - Automação e docs: `.github/workflows/estudo_diario.yml`, `README.md`
     - Prompts e teologia: `src/prompts.py`, `src/storage.py`, `tests/test_storage.py`
     - Dados e frontend: `web/app.js`, `web/data.js`
     - Estudos atualizados: `estudos/*.md`
   - Mensagem de commit clara no padrão Conventional Commits (ex: `feat: migra para gemini-3.6-flash e enriquece devocional com teólogos consagrados`).
3. **Publicação no GitHub**:
   - `git push origin main` (ou branch dedicada conforme preferência do usuário).
   - Acionamento ou validação dos workflows do GitHub Actions (`estudo_diario.yml` / GitHub Pages).

---

## 4. Tech Stack & Ferramentas
- **Git** (CLI)
- **GitHub Remote** (`origin`: `https://github.com/Nence-dev/projeto_biblia.git`)
- **CI/CD**: GitHub Actions

---

## 5. File Structure & Arquivos a Sincronizar
```
projeto_limpo_git/
├── .env.example
├── .github/workflows/estudo_diario.yml
├── README.md
├── estudos/
│   ├── 2026-10-06_joao_14_27.md
│   ├── 2026-10-07_colossenses_3_23.md
│   └── 2026-10-08_tiago_5_16.md
├── plano-devocional-vivo-historias-narrativas.md
├── src/
│   ├── config.py
│   ├── llm_client.py
│   ├── prompts.py
│   └── storage.py
├── tests/
│   └── test_storage.py
├── web/
│   ├── app.js
│   └── data.js
└── atualizacao-gemini-teologos.md
```

---

## 6. Task Breakdown

### Tarefa 1: Resolução do Estado de Rebase e Preservação dos Arquivos
- **Agente:** `devops-engineer`
- **Skill:** `@clean-code`, `@bash-linux`, `@powershell-windows`
- **Prioridade:** P0
- **INPUT:** Repositório local em estado de rebase.
- **OUTPUT:** Rebase concluído / consolidado com working directory íntegro.
- **VERIFY:** `git status` limpo ou pronto para novo commit sem conflitos.

### Tarefa 2: Staging e Verificação de Segurança (No-Secrets)
- **Agente:** `devops-engineer`
- **Skill:** `@clean-code`, `@vulnerability-scanner`
- **Prioridade:** P0
- **INPUT:** Arquivos modificados.
- **OUTPUT:** Staging via `git add` dos arquivos necessários. Verificação de que `.env` não está staged.
- **VERIFY:** `git status` mostra apenas arquivos de código, docs e dados previstos.

### Tarefa 3: Commit Semântico e Push para o GitHub
- **Agente:** `devops-engineer`
- **Skill:** `@deployment-procedures`
- **Prioridade:** P1
- **INPUT:** Alterações staged.
- **OUTPUT:** Commit criado e enviado via `git push origin main`.
- **VERIFY:** `git status` retorna "Your branch is up to date with 'origin/main'".

### Tarefa 4: Validação de Testes e Prontidão de CI
- **Agente:** `test-engineer`
- **Skill:** `@testing-patterns`, `@verify-changes`
- **Prioridade:** P2
- **INPUT:** Código sincronizado.
- **OUTPUT:** Suíte de testes `pytest` validada para garantir que o pipeline remoto execute com sucesso.
- **VERIFY:** Exit code 0 em `pytest`.

---

## 7. Phase X: Final Verification
- [ ] Rebase resolvido com sucesso.
- [ ] Commit semântico registrado.
- [ ] `.env` preservado e protegido fora do versionamento.
- [ ] Push executado para o GitHub (`origin/main`).
- [ ] Status final do repositório sincronizado.
