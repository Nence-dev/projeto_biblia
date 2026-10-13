@echo off
setlocal
title Teste Local de Prompts do Gemini - Projeto Biblia

cd /d "%~dp0"
echo ====================================================================
echo  Executando Teste Local com os Novos Prompts do Gemini
echo ====================================================================
echo.

python testar_novo_prompt.py
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao executar o teste local. Verifique as mensagens acima.
    goto FIM
)

echo.
echo ====================================================================
echo  Teste concluido com sucesso! Abrindo web/index.html no navegador...
echo ====================================================================
start "" "web\index.html"

:FIM
echo.
pause
