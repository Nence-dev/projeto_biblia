# 📖 Versículo do Dia & Teologia Expositiva (Web Platform)

Plataforma completa em Python que realiza a coleta diária automatizada do **Versículo do Dia** no YouVersion (`bible.com`), gera uma reflexão teológica expositiva profunda, cristocêntrica e da graça utilizando a **Google Gemini API**, armazena o histórico em **Markdown** e disponibiliza uma **interface Web moderna, responsiva e interativa** com suporte a **GitHub Pages**.

---

## ✨ Funcionalidades Principais

- **🌐 Interface Web Moderna & Responsiva**: Visual limpo, tipografia editorial de alta legibilidade, modo claro/escuro com preservação de preferências e leitura fluida sem caracteres de controle desnecessários.
- **📚 Histórico Completo de Estudos**: Navegue pelos estudos bíblicos dos dias anteriores diretamente pelo menu lateral ou seletor de datas, permitindo revisitar o acervo a qualquer momento.
- **☁️ Automação Diária na Nuvem (GitHub Actions)**: Todos os dias às 06:00 BRT, o GitHub executa a rotina automaticamente sem precisar do seu computador ligado, gerando o novo estudo, atualizando o histórico e publicando no GitHub Pages.
- **📖 Coleta Automatizada no YouVersion**: Raspagem em tempo real de `https://www.bible.com/pt/verse-of-the-day` com suporte a múltiplas versões bíblicas (NVI, ARA, NAA, NVT, ARC).
- **✝️ Teologia Expositiva Cristocêntrica**: Fundamentada na tradição **reformada e da graça**, combatendo desvios de consumo, moralismo e teologia da prosperidade.
- **🏛️ Estrutura em 5 Etapas Expositivas**:
  1. *Contexto Histórico & Narrativo*
  2. *Anatomia do Texto & Termos Originais (Hebraico / Grego)*
  3. *O que tirar disso para a prática de hoje?*
  4. *Conexões Canônicas & Teólogos Históricos* (C.S. Lewis, Tim Keller, John Stott, Martyn Lloyd-Jones)
  5. *A Pergunta Central Desestabilizadora*
- **📱 Síntese para Compartilhamento**: Versão pronta com botão de cópia de um clique para WhatsApp e redes sociais.
- **💾 Gestão Inteligente de Cache**: Detecta se o estudo de hoje já foi gerado para evitar consumo desnecessário de tokens da API.

---

## 🏗️ Arquitetura do Projeto

```text
Projeto_Biblia/
├── .github/
│   └── workflows/
│       └── estudo_diario.yml      # Automação diária e deploy no GitHub Pages
├── estudos/                       # Acervo perpétuo dos estudos em Markdown
│   └── 2026-09-29_proverbios_4_23.md
├── src/
│   ├── cli.py                     # Linha de comando interativa (Terminal e inicializador Web)
│   ├── config.py                  # Configurações globais e carregamento seguro do .env
│   ├── llm_client.py              # Integração com o Google Gemini Oficial
│   ├── scraper.py                 # Coletor YouVersion (bible.com)
│   └── storage.py                 # Persistência Markdown e compilador web/data.js
├── tests/                         # Suíte de testes automatizados com pytest
│   ├── test_cli_and_web.py
│   ├── test_llm_client.py
│   ├── test_scraper.py
│   └── test_storage.py
├── web/                           # Aplicação Web Estática (PWA-ready)
│   ├── css/
│   │   └── style.css              # Sistema de design responsivo com dark mode
│   ├── js/
│   │   └── app.js                 # Lógica da interface, alternância de estudos e cópia
│   ├── data.js                    # Base de dados sincronizada automaticamente
│   └── index.html                 # Página principal
├── main.py                        # Ponto de entrada da aplicação
├── requirements.txt               # Dependências Python enxutas
└── README.md                      # Documentação do projeto
```

---

## 🚀 Instalação e Uso Local

### 1. Clonar ou Acessar a Pasta do Projeto
```bash
cd Projeto_Biblia
```

### 2. Criar e Ativar o Ambiente Virtual
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar a Chave da API Gemini
Copie o template de ambiente:
```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```
Edite o arquivo `.env` e insira sua chave gratuita obtida no [Google AI Studio](https://aistudio.google.com/):
```env
GEMINI_API_KEY=sua_chave_gemini_aqui
GEMINI_MODEL=gemini-3.5-flash
BIBLIA_VERSAO=nvi
```

---

## 💻 Comandos da Linha de Comando (CLI)

### Gerar o Estudo de Hoje e Sincronizar o Site Web
```bash
python main.py
```

### Abrir Diretamente a Interface Web no Navegador
```bash
python main.py --web
```

### Forçar Nova Geração (Ignorando o Cache do Dia)
```bash
python main.py --force
```

### Consultar o Histórico de Estudos Salvos no Terminal
```bash
python main.py --historico
```

### Gerar para uma Passagem Específica
```bash
python main.py -v "Romanos 8:1"
```

---

## 🌐 Publicando no GitHub & Ativando o Site Online Grátis

Para ter seu site no ar e funcionando mesmo sem o seu computador ligado:

### Passo 1: Inicializar o Git e Subir o Código
No terminal (PowerShell), execute:
```powershell
git init
git add .
git commit -m "feat: plataforma web versiculo do dia e teologia expositiva"
git branch -M main
git remote add origin https://github.com/<seu-usuario>/<nome-do-repositorio>.git
git push -u origin main
```

### Passo 2: Configurar o Secret da API no GitHub
1. Acesse o seu repositório no GitHub.
2. Vá em **Settings** > **Secrets and variables** > **Actions**.
3. Clique em **New repository secret**.
4. Crie o segredo:
   - **Name**: `GEMINI_API_KEY`
   - **Secret**: cole a sua chave da Google Gemini API.

### Passo 3: Ativar o GitHub Pages
1. No menu do repositório, vá em **Settings** > **Pages**.
2. Em **Build and deployment** > **Source**, selecione:
   - **GitHub Actions**
3. Pronto! O workflow `.github/workflows/estudo_diario.yml` publicará o site automaticamente e fornecerá a URL pública (ex.: `https://<seu-usuario>.github.io/<nome-do-repositorio>/`).

---

## 🧪 Testes Automatizados

Para rodar a suíte de testes unitários:
```bash
pytest
```
