"""Testes unitários para validação de tradução de referências bíblicas e garantia de texto em português."""

import pytest
from unittest.mock import patch, MagicMock

from src.bible_books import (
    traduzir_referencia_en_para_pt,
    eh_referencia_em_ingles,
    eh_texto_em_ingles,
    eh_texto_ou_referencia_em_ingles,
    normalizar_nome_livro,
    MAPA_LIVROS_EN_PARA_PT,
)
from src.scraper import (
    normalizar_referencia,
    assegurar_versiculo_em_portugues,
    recuperar_texto_versiculo_em_portugues,
    VersiculoDoDia,
)


def test_traduzir_referencias_en_para_pt():
    casos = [
        ("Proverbs 22:6", "Provérbios 22:6"),
        ("James 5:16", "Tiago 5:16"),
        ("1 Corinthians 13:4", "1 Coríntios 13:4"),
        ("1Corinthians 13:4", "1 Coríntios 13:4"),
        ("2 Corinthians 10:5", "2 Coríntios 10:5"),
        ("Psalms 23:1", "Salmos 23:1"),
        ("Psalm 23:1", "Salmos 23:1"),
        ("Matthew 4:4", "Mateus 4:4"),
        ("John 3:16", "João 3:16"),
        ("Romans 8:28", "Romanos 8:28"),
        ("Genesis 1:1", "Gênesis 1:1"),
        ("Revelation 21:4", "Apocalipse 21:4"),
        ("Song of Solomon 2:4", "Cânticos 2:4"),
        ("PRO.22.6", "Provérbios 22:6"),
        ("JAS.5.16", "Tiago 5:16"),
        ("MAT.4.4", "Mateus 4:4"),
    ]
    for entrada_en, esperado_pt in casos:
        assert traduzir_referencia_en_para_pt(entrada_en) == esperado_pt, f"Falha para {entrada_en}"
        assert normalizar_referencia(entrada_en) == esperado_pt, f"Falha em normalizar_referencia para {entrada_en}"


def test_manutencao_referencias_em_portugues():
    casos_pt = [
        "Provérbios 22:6",
        "Tiago 5:16",
        "1 Coríntios 13:4",
        "2 Coríntios 10:5",
        "Salmos 23:1",
        "Mateus 4:4",
        "João 3:16",
        "Romanos 8:28",
        "Gênesis 1:1",
        "Apocalipse 21:4",
    ]
    for ref in casos_pt:
        assert traduzir_referencia_en_para_pt(ref) == ref
        assert normalizar_referencia(ref) == ref
        assert eh_referencia_em_ingles(ref) is False


def test_eh_referencia_em_ingles():
    assert eh_referencia_em_ingles("Proverbs 22:6") is True
    assert eh_referencia_em_ingles("James 5:16") is True
    assert eh_referencia_em_ingles("1 Corinthians 13:4") is True
    assert eh_referencia_em_ingles("Matthew 4:4") is True
    assert eh_referencia_em_ingles("Provérbios 22:6") is False
    assert eh_referencia_em_ingles("Tiago 5:16") is False
    assert eh_referencia_em_ingles("1 Coríntios 13:4") is False


def test_eh_texto_em_ingles():
    texto_ingles = "Start children off on the way they should go, and even when they are old they will not turn from it."
    texto_portugues = "Eduque a criança no caminho em que deve andar, e até o fim da vida não se desviará dele."

    assert eh_texto_em_ingles(texto_ingles) is True
    assert eh_texto_em_ingles(texto_portugues) is False
    assert eh_texto_ou_referencia_em_ingles(texto_ingles, "Proverbs 22:6") is True
    assert eh_texto_ou_referencia_em_ingles(texto_portugues, "Provérbios 22:6") is False


def test_assegurar_versiculo_em_portugues_quando_ja_esta_em_pt():
    texto_nvi_oficial = "Instrua a criança segundo os objetivos que você tem para ela, e mesmo com o passar dos anos não se desviará deles."
    v = VersiculoDoDia(
        referencia="Provérbios 22:6",
        texto=texto_nvi_oficial,
        versao="NVI",
        url_fonte="https://www.bible.com/pt/verse-of-the-day",
        coletado_em="2026-10-12",
    )
    v_seguro = assegurar_versiculo_em_portugues(v, "NVI")
    assert v_seguro.referencia == "Provérbios 22:6"
    assert v_seguro.texto == texto_nvi_oficial
    assert "Normalizado" not in v_seguro.url_fonte


def test_assegurar_versiculo_em_portugues_com_referencia_ingles():
    texto_nvi_oficial = "Instrua a criança segundo os objetivos que você tem para ela, e mesmo com o passar dos anos não se desviará deles."
    v = VersiculoDoDia(
        referencia="Proverbs 22:6",
        texto=texto_nvi_oficial,
        versao="NVI",
        url_fonte="https://www.bible.com/pt/verse-of-the-day",
        coletado_em="2026-10-12",
    )
    v_seguro = assegurar_versiculo_em_portugues(v, "NVI")
    assert v_seguro.referencia == "Provérbios 22:6"
    assert v_seguro.texto == texto_nvi_oficial
    assert "[Normalizado para Português]" in v_seguro.url_fonte


@patch("src.scraper.recuperar_texto_versiculo_em_portugues")
def test_assegurar_versiculo_em_portugues_resgata_texto(mock_recuperar):
    mock_recuperar.return_value = "Instrua a criança no caminho em que deve andar, e, mesmo com o passar dos anos, não se desviará dele."

    v_ingles = VersiculoDoDia(
        referencia="Proverbs 22:6",
        texto="Start children off on the way they should go, and even when they are old they will not turn from it.",
        versao="NVI",
        url_fonte="https://www.bible.com/verse-of-the-day",
        coletado_em="2026-10-12",
    )

    v_seguro = assegurar_versiculo_em_portugues(v_ingles, "NVI")
    assert v_seguro.referencia == "Provérbios 22:6"
    assert v_seguro.texto == "Instrua a criança no caminho em que deve andar, e, mesmo com o passar dos anos, não se desviará dele."
    assert "[Normalizado para Português]" in v_seguro.url_fonte
    mock_recuperar.assert_called_once_with("Provérbios 22:6", versao="NVI")
