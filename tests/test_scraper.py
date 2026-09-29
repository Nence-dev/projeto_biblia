"""Testes unitários para o módulo de scraping do YouVersion (src/scraper.py)."""

import pytest
from bs4 import BeautifulSoup
from src.scraper import (
    extrair_referencia_e_texto,
    obter_versiculo_do_dia,
    ScraperError,
)


def test_extrair_referencia_e_texto_formato_padrao():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Versículo do Dia - Provérbios 4:23 — App da Bíblia</title>
        <meta property="og:description" content="Provérbios 4:23 Tenha cuidado com o que você pensa, pois a sua vida é dirigida pelos seus pensamentos." />
    </head>
    <body></body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    ref, texto = extrair_referencia_e_texto(soup)

    assert ref == "Provérbios 4:23"
    assert texto == "Tenha cuidado com o que você pensa, pois a sua vida é dirigida pelos seus pensamentos."


def test_extrair_referencia_e_texto_regex_fallback():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>App da Bíblia</title>
        <meta name="twitter:description" content="Romanos 8:1 Portanto, agora já não há condenação para os que estão em Cristo Jesus." />
    </head>
    <body></body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    ref, texto = extrair_referencia_e_texto(soup)

    assert ref == "Romanos 8:1"
    assert "Portanto, agora já não há condenação" in texto


def test_extrair_referencia_invalida_lanca_erro():
    html = "<html><head><title>Página Sem Versículo</title></head><body>Vazio</body></html>"
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(ScraperError):
        extrair_referencia_e_texto(soup)


def test_obter_versiculo_manual():
    resultado = obter_versiculo_do_dia(
        versao="nvi",
        versiculo_manual="1 Coríntios 13:13",
        texto_manual="Assim, permanecem agora estes três: a fé, a esperança e o amor.",
    )

    assert resultado.referencia == "1 Coríntios 13:13"
    assert resultado.texto == "Assim, permanecem agora estes três: a fé, a esperança e o amor."
    assert resultado.versao == "NVI"
    assert resultado.url_fonte == "Entrada manual"


def test_eh_pagina_de_desafio_bot():
    from src.scraper import eh_pagina_de_desafio_bot

    html_desafio = "<html><head><title>Client Challenge</title></head><body>JavaScript is disabled in your browser.</body></html>"
    assert eh_pagina_de_desafio_bot(html_desafio) is True

    html_valido = "<html><head><title>Versículo do Dia</title></head><body>Conteúdo Bíblico</body></html>"
    assert eh_pagina_de_desafio_bot(html_valido) is False


def test_extrair_versiculo_bibliaon_card():
    from src.scraper import extrair_versiculo_bibliaon

    html_bibliaon = """
    <html>
    <body>
        <div class="versiculo-card">
            <p><a href="/filipenses_4_13/">Filipenses 4:13</a></p>
            <p class="destaque">Tudo posso naquele que me fortalece.</p>
        </div>
    </body>
    </html>
    """
    res = extrair_versiculo_bibliaon(html_bibliaon)
    assert res is not None
    ref, texto = res
    assert ref == "Filipenses 4:13"
    assert "Tudo posso naquele que me fortalece" in texto
