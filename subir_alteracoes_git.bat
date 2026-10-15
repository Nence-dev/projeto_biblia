@echo off
setlocal
title Subir Alteracoes NVI para o GitHub - Projeto Biblia

cd /d "%~dp0"
echo ====================================================================
echo  Subindo Atualizacoes Canonicas da NVI para o GitHub
echo ====================================================================
echo.

python subir_alteracoes_git.py
if errorlevel 1 (
    echo.
    echo [AVISO] Tentando rebase direto com o GitHub...
    git pull --rebase origin main -X ours
    git push origin main
)

:FIM
echo.
pause
