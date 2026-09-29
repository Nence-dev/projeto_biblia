"""Testes unitários para o módulo de persistência e cache (src/storage.py)."""

import pytest
from pathlib import Path
from src.storage import (
    normalizar_slug,
    salvar_estudo,
    ler_estudo,
    obter_estudo_hoje,
    estudo_existe_hoje,
    listar_historico,
)


def test_normalizar_slug():
    assert normalizar_slug("Romanos 8:1") == "romanos_8_1"
    assert normalizar_slug("1 Coríntios 13:4-7") == "1_corintios_13_4-7"
    assert normalizar_slug("Provérbios 4:23") == "proverbios_4_23"
    assert normalizar_slug("João 3:16") == "joao_3_16"


def test_salvar_e_ler_estudo(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.ESTUDOS_DIR", tmp_path)

    referencia = "Romanos 8:1"
    texto = "Portanto, agora já não há condenação para os que estão em Cristo Jesus."
    versao = "nvi"
    conteudo_estudo = "## 1. O Contexto Histórico\nPaulo escreve à comunidade em Roma..."
    conteudo_whatsapp = "*Romanos 8:1*\nSem condenação em Cristo Jesus!"
    data_teste = "2026-09-29"

    caminho = salvar_estudo(
        referencia=referencia,
        texto_versiculo=texto,
        versao=versao,
        conteudo_estudo=conteudo_estudo,
        conteudo_whatsapp=conteudo_whatsapp,
        data_str=data_teste,
    )

    assert caminho.exists()
    assert caminho.name == "2026-09-29_romanos_8_1.md"

    conteudo_lido = ler_estudo(caminho)
    assert "referencia: \"Romanos 8:1\"" in conteudo_lido
    assert "Portanto, agora já não há condenação" in conteudo_lido
    assert "Paulo escreve à comunidade em Roma" in conteudo_lido
    assert "Versão para WhatsApp" in conteudo_lido
    assert "Sem condenação em Cristo Jesus!" in conteudo_lido


def test_obter_estudo_hoje_e_existencia(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.ESTUDOS_DIR", tmp_path)

    data_teste = "2026-09-29"
    assert not estudo_existe_hoje(data_teste)
    assert obter_estudo_hoje(data_teste) is None

    salvar_estudo(
        referencia="João 3:16",
        texto_versiculo="Porque Deus tanto amou o mundo...",
        versao="NVI",
        conteudo_estudo="Estudo sobre amor divino.",
        data_str=data_teste,
    )

    assert estudo_existe_hoje(data_teste)
    caminho_hoje = obter_estudo_hoje(data_teste)
    assert caminho_hoje is not None
    assert "2026-09-29_joao_3_16.md" in caminho_hoje.name


def test_listar_historico(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.ESTUDOS_DIR", tmp_path)

    salvar_estudo("Salmos 23:1", "O Senhor é o meu pastor...", "NVI", "Estudo 1", data_str="2026-09-28")
    salvar_estudo("Salmos 91:1", "Aquele que habita no abrigo...", "NVI", "Estudo 2", data_str="2026-09-29")

    historico = listar_historico()
    assert len(historico) == 2
    # Ordem cronológica decrescente
    assert historico[0]["data"] == "2026-09-29"
    assert historico[1]["data"] == "2026-09-28"
