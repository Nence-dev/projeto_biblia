# Plano de Limpeza e Unificação: Foco Exclusivo em `projeto_limpo_git`

> **Objetivo:** Eliminar todas as duplicações de código, estudos e frontend que residem na pasta raiz, consolidando `projeto_limpo_git` como a **única fonte da verdade** do projeto, preservando estritamente os agentes de IA (`.agents/`).

---

## 1. Diagnóstico do Estado Atual

### 1.1 Por que tudo estava sendo duplicado?
- Inicialmente, o projeto rodava na raiz `E:\Desktop\estudo\Python\Projeto_Biblia` com um repositório `.git` apontando para um repositório antigo (`projeto_bliblia.git` com erro de digitação no nome).
- Posteriormente, foi criada a pasta `projeto_limpo_git` conectada ao GitHub oficial (`https://github.com/Nence-dev/projeto_biblia.git`) onde rodam o **GitHub Actions** e o **GitHub Pages**.
- Como existiam duas pastas com a mesma estrutura (`src`, `web`, `estudos`, `tests`, `main.py`), alterações e gerações diárias estavam sendo salvas tanto na raiz quanto em `projeto_limpo_git`, gerando inconsistências (por exemplo: o estudo de Tiago 5:16 havia sido gerado na raiz e faltava no git).

---

## 2. Inventário de Arquivos e Decisões de Limpeza

### 🟢 O que DEVE ser Preservado (NÃO APAGAR)
| Caminho | Motivo |
|---|---|
| `projeto_limpo_git/` | **Repositório oficial e ativo.** Contém todo o código, automações do GitHub Actions, GitHub Pages, estudos e frontend. |
| `.agents/` | Configurações do Antigravity IDE (regras de workspace, skills, agentes de IA, memória). |
| `.agent/` | Alias/legado dos agentes do IDE. |

---

### 🔴 O que Está Duplicado / Sem Uso na Raiz (Será Removido)
| Item na Raiz | Status / Destino |
|---|---|
| `E:\Desktop\estudo\Python\Projeto_Biblia\src\` | ❌ Duplicata de `projeto_limpo_git/src/` |
| `E:\Desktop\estudo\Python\Projeto_Biblia\web\` | ❌ Duplicata de `projeto_limpo_git/web/` |
| `E:\Desktop\estudo\Python\Projeto_Biblia\estudos\` | ❌ Duplicata de `projeto_limpo_git/estudos/` (Tiago 5:16 já copiado para o oficial) |
| `E:\Desktop\estudo\Python\Projeto_Biblia\tests\` | ❌ Duplicata de `projeto_limpo_git/tests/` |
| `E:\Desktop\estudo\Python\Projeto_Biblia\.github\` | ❌ Duplicata de `projeto_limpo_git/.github/` |
| `E:\Desktop\estudo\Python\Projeto_Biblia\.git\` | ❌ Repositório fantasma/antigo desconectado |
| `E:\Desktop\estudo\Python\Projeto_Biblia\.pytest_cache\` | ❌ Cache antigo |
| `E:\Desktop\estudo\Python\Projeto_Biblia\scratch\` | ❌ Arquivos temporários |
| `E:\Desktop\estudo\Python\Projeto_Biblia\main.py` | ❌ Duplicata de `projeto_limpo_git/main.py` |
| `E:\Desktop\estudo\Python\Projeto_Biblia\requirements.txt`| ❌ Duplicata de `projeto_limpo_git/requirements.txt` |
| `E:\Desktop\estudo\Python\Projeto_Biblia\copy_assets.py` | ❌ Script obsoleto |
| `E:\Desktop\estudo\Python\Projeto_Biblia\debug_youversion.html`| ❌ Resíduo de depuração |
| `E:\Desktop\estudo\Python\Projeto_Biblia\vercel.json` | ❌ Duplicata de `projeto_limpo_git/vercel.json` |
| `E:\Desktop\estudo\Python\Projeto_Biblia\*.md` (planos antigos) | ❌ 30+ arquivos markdown de planos e rascunhos antigos da raiz |

---

## 3. Estado Atual de `projeto_limpo_git` (Pronto para Commit & Push)

Os arquivos em `projeto_limpo_git` já foram 100% atualizados e higienizados:
1. `src/storage.py`:
   - Parser ultra-resiliente com 4 níveis de extração para o texto do versículo (impede texto em branco).
   - Sanitização de aspas na gravação markdown e no JSON do devocional.
2. `src/scraper.py`:
   - Arquitetura de 5 camadas (Direto -> Jina com parse de imagem/Next.js -> IA Gemini do dia -> Bíbliaon -> Calendário).
3. `estudos/2026-10-08_tiago_5_16.md`:
   - Estudo completo de Tiago 5:16 adicionado com sucesso.
4. `web/data.js`:
   - Histórico atualizado com Tiago 5:16 (índice 0) e Colossenses 3:23 (índice 1), sem conflitos de merge.
5. `.github/workflows/estudo_diario.yml`:
   - `JINA_API_KEY: ${{ secrets.JINA_API_KEY }}` adicionado para permitir bypass Cloudflare nos runners do GitHub.

---

## 4. Passos de Execução Recomendados

### Passo A: Finalizar o Git em `projeto_limpo_git`
Na pasta `E:\Desktop\estudo\Python\Projeto_Biblia\projeto_limpo_git`:
```powershell
# 1. Adicionar todas as melhorias e o estudo de hoje
git add .

# 2. Concluir o commit
git commit -m "fix: unificacao projeto limpo, estudo Tiago 5:16 e correcao versiculo e scraper"

# 3. Enviar para o GitHub oficial
git push origin main
```

### Passo B: Executar a Limpeza Segura na Raiz
Executar o comando PowerShell seguro na raiz para apagar apenas o que é duplicado/desnecessário, **protegendo** `.agents` e `projeto_limpo_git`:
```powershell
cd E:\Desktop\estudo\Python\Projeto_Biblia

# Remover pastas duplicadas na raiz
Remove-Item -Recurse -Force src, web, estudos, tests, .github, .git, .pytest_cache, scratch -ErrorAction SilentlyContinue

# Remover arquivos duplicados/resíduos na raiz
Remove-Item -Force main.py, requirements.txt, copy_assets.py, debug_youversion.html, vercel.json -ErrorAction SilentlyContinue

# Opcional: limpar os arquivos .md antigos soltos na raiz (exceto README.md)
Get-ChildItem -Path . -Filter "*.md" -File | Where-Object { $_.Name -ne "README.md" } | Remove-Item -Force
```
