@echo off
setlocal enabledelayedexpansion
title Publicar Atualizacoes Canonicas NVI no GitHub

cd /d "%~dp0"
echo ====================================================================
echo  Publicando Atualizacoes da NVI no GitHub (origin main)
echo ====================================================================
echo.

echo [1/4] Buscando atualizacoes recentes do GitHub...
git fetch origin main

echo.
echo [2/4] Adicionando arquivos modificados (codigo, estudos e testes)...
git add src/biblia_nvi.py
git add src/scraper.py
git add src/storage.py
git add src/prompts.py
git add src/llm_client.py
git add src/cli.py
git add gerar_hoje.py
git add tests/test_biblia_nvi.py
git add tests/test_versiculo_portugues.py
git add tests/test_rotacao_autores.py
git add estudos/2026-10-15_colossenses_3_13.md
git add estudos/2026-10-14_salmos_46_10.md
git add estudos/2026-10-13_jeremias_17_7.md
git add web/data.js
git add garantia-texto-nvi-versiculo-do-dia.md
git add rotacao-autores-frases-pensadores.md
git add subir_alteracoes_git.py
git add subir_alteracoes_git.bat
git add atualizar_git_nvi.bat

echo.
echo [3/5] Gravando commit local...
git commit -m "fix: texto NVI canônico e rotação anti-repetição de pensadores (eliminando monopólio de Tim Keller)"

echo.
echo [4/5] Sincronizando com o GitHub preservando nossas alteracoes NVI e de pensadores (-X ours)...
git pull --rebase origin main -X ours

echo.
echo [5/5] Enviando para o GitHub (git push origin main)...
git push origin main
if errorlevel 1 (
    echo.
    echo [AVISO] Tentando envio com force-with-lease...
    git push origin main --force-with-lease
)

echo.
echo ====================================================================
echo  SUCESSO! As alteracoes da NVI foram enviadas para o GitHub!
echo  O GitHub Pages atualizara o site em aproximadamente 1-2 minutos.
echo ====================================================================
echo.
pause
