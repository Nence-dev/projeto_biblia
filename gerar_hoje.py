#!/usr/bin/env python3
"""Script de geração direta do estudo diário com o versículo oficial da YouVersion."""

import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.scraper import obter_versiculo_do_dia
from src.llm_client import GeminiClient
from src.storage import salvar_estudo, exportar_todos_estudos_para_web_data

def executar():
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    print(f"Iniciando geracao do estudo para {data_hoje}...")
    
    versiculo = obter_versiculo_do_dia(versao="nvi")
    print(f"Passagem obtida: {versiculo.referencia}")
    print(f"Texto: {versiculo.texto}")
    print(f"Fonte: {versiculo.url_fonte}")
    
    client = GeminiClient()
    print("Consultando Gemini...")
    estudo = client.gerar_estudo_completo(
        referencia=versiculo.referencia,
        texto=versiculo.texto,
        versao=versiculo.versao,
        on_status=lambda msg: print(f"  [Status] {msg}"),
    )
    
    print("Gerando sintese WhatsApp...")
    whatsapp = client.gerar_derivacao_whatsapp(
        referencia=versiculo.referencia,
        texto=versiculo.texto,
        versao=versiculo.versao,
        estudo_gerado=estudo,
        on_status=lambda msg: print(f"  [Status] {msg}"),
    )
    
    caminho = salvar_estudo(
        referencia=versiculo.referencia,
        texto_versiculo=versiculo.texto,
        versao=versiculo.versao,
        conteudo_estudo=estudo,
        conteudo_whatsapp=whatsapp,
        data_str=data_hoje,
    )
    print(f"Estudo salvo em: {caminho}")
    
    destino_web = exportar_todos_estudos_para_web_data()
    print(f"Web data exportado para: {destino_web}")

if __name__ == "__main__":
    executar()
