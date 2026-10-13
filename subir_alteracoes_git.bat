@echo off
setlocal
title Subir Alteracoes para o GitHub - Projeto Biblia

cd /d "%~dp0"
echo ====================================================================
echo  Subindo Novo Formato dos Prompts do Gemini para o GitHub
echo ====================================================================
echo.

python subir_alteracoes_git.py
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao enviar para o GitHub. Verifique as mensagens acima.
    goto FIM
)

:FIM
echo.
pause
