"""Testes unitários para o módulo de scraping do YouVersion (src/scraper.py) e contingência."""

from datetime import datetime
import pytest
from bs4 import BeautifulSoup
from unittest.mock import patch

from src.scraper import (
    extrair_referencia_e_texto,
    obter_versiculo_do_dia,
    normalizar_referencia,
    eh_pagina_de_desafio_bot,
    extrair_versiculo_bibliaon,
    extrair_versiculo_jina,
    ScraperError,
)
from src.versiculos_calendario import obter_versiculo_calendario


def test_normalizar_referencia():
    assert normalizar_referencia("2Coríntios 10:5") == "2 Coríntios 10:5"
    assert normalizar_referencia("1João 1:9") == "1 João 1:9"
    assert normalizar_referencia("3João 1:2") == "3 João 1:2"
    assert normalizar_referencia("Romanos 8:28") == "Romanos 8:28"


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


def test_extrair_referencia_e_texto_numero_junto_youversion():
    """Valida o caso real do YouVersion onde o título vem com '2Coríntios 10:5'."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Versículo do Dia - 2Coríntios 10:5 — App da Bíblia</title>
        <meta property="og:description" content="2Coríntios 10:5 e também todo orgulho humano que não deixa que as pessoas conheçam a Deus. Dominamos todo pensamento humano e fazemos com que ele obedeça a Cristo." />
    </head>
    <body></body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    ref, texto = extrair_referencia_e_texto(soup)

    assert ref == "2 Coríntios 10:5"
    assert texto.startswith("e também todo orgulho humano")
    assert "obedecer" in texto or "obedeça" in texto


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
    html_desafio = "<html><head><title>Client Challenge</title></head><body>JavaScript is disabled in your browser.</body></html>"
    assert eh_pagina_de_desafio_bot(html_desafio) is True

    html_valido = "<html><head><title>Versículo do Dia</title></head><body>Conteúdo Bíblico</body></html>"
    assert eh_pagina_de_desafio_bot(html_valido) is False


def test_extrair_versiculo_bibliaon_card():
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


def test_obter_versiculo_calendario():
    data_outubro_1 = datetime(2026, 10, 1)
    ref, texto = obter_versiculo_calendario(data_outubro_1)
    assert ref == "2 Coríntios 10:5"
    assert "pensamento" in texto or "Cristo" in texto


def test_fallback_calendario_quando_web_indisponivel():
    """Garante que quando todas as fontes web falharem, o Tier de contingência retorna o versículo do dia sem travar o CI."""
    with patch("src.scraper.baixar_html_via_requests", return_value=None), \
         patch("src.scraper.baixar_html_via_curl", return_value=None), \
         patch("src.scraper.baixar_via_jina", return_value=None), \
         patch("src.scraper.extrair_versiculo_bibliaon", return_value=None):
        versiculo = obter_versiculo_do_dia(versao="nvi")
        assert versiculo is not None
        assert versiculo.referencia != ""
        assert versiculo.texto != ""
        assert "Calendário Bíblico" in versiculo.url_fonte


def test_extrair_versiculo_jina_alt_text_image():
    """Valida extração a partir do formato Markdown real retornado pelo Jina Reader para o YouVersion."""
    markdown_jina = """
Title: Versículo do Dia

URL Source: https://www.bible.com/pt/verse-of-the-day

Markdown Content:
[![Image 1: Logotipo do App da Bíblia](https://www.bible.com/_next/image?url=%2Flogo.png&w=384&q=75)](https://www.bible.com/pt)

4 de outubro de 2026

[![Image 2: Salmos 51:10 - Ó Deus, cria em mim um coração puro e dá-me uma vontade nova e firme!](https://imageproxy.youversionapi.com/640x640/image.jpg)](https://www.bible.com/pt/verse-images/PSA.51.10/91886?version=211)

[Ó Deus, cria em mim um coração puro e dá-me uma vontade nova e firme!](https://www.bible.com/pt/bible/211/PSA.51.10.NTLH)

[Salmos 51:10 (NTLH)](https://www.bible.com/pt/bible/211/PSA.51.10.NTLH)
"""
    res = extrair_versiculo_jina(markdown_jina)
    assert res is not None
    ref, texto = res
    assert ref == "Salmos 51:10"
    assert texto == "Ó Deus, cria em mim um coração puro e dá-me uma vontade nova e firme!"


def test_extrair_versiculo_jina_link_pair():
    """Valida extração quando o markdown do Jina não tem Image alt text mas tem os links bíblicos."""
    markdown_jina = """
Title: Versículo do Dia

URL Source: https://www.bible.com/pt/verse-of-the-day

Markdown Content:
[Ó Deus, cria em mim um coração puro e dá-me uma vontade nova e firme!](https://www.bible.com/pt/bible/211/PSA.51.10.NTLH)

[Salmos 51:10 (NTLH)](https://www.bible.com/pt/bible/211/PSA.51.10.NTLH)

[Ler Salmos 51:10](https://www.bible.com/pt/bible/211/PSA.51.10.NTLH)
"""
    res = extrair_versiculo_jina(markdown_jina)
    assert res is not None
    ref, texto = res
    assert ref == "Salmos 51:10"
    assert "coração puro" in texto


def test_extrair_versiculo_jina_title_fallback():
    """Valida extração quando o título do Jina traz a passagem bíblica."""
    markdown_jina = """
Title: Versículo do Dia - Romanos 8:28 - Sabemos que Deus age em todas as coisas | Bible.com

Markdown Content:
Texto do corpo aqui...
"""
    res = extrair_versiculo_jina(markdown_jina)
    assert res is not None
    ref, texto = res
    assert ref == "Romanos 8:28"
    assert "todas as coisas" in texto


def test_obter_versiculo_do_dia_via_jina_sucesso():
    """Garante que quando requests/curl bloquearem por Cloudflare, o Jina Reader obtém com sucesso o YouVersion."""
    markdown_jina = """
Title: Versículo do Dia

[![Image 2: Salmos 51:10 - Ó Deus, cria em mim um coração puro e dá-me uma vontade nova e firme!](https://image.jpg)](https://www.bible.com/pt/verse-images/PSA.51.10/91886)
"""
    with patch("src.scraper.baixar_html_via_requests", return_value=None), \
         patch("src.scraper.baixar_html_via_curl", return_value=None), \
         patch("src.scraper.baixar_via_jina", return_value=markdown_jina):
        resultado = obter_versiculo_do_dia(versao="nvi")
        assert resultado is not None
        assert resultado.referencia == "Salmos 51:10"
        assert "coração puro" in resultado.texto
        assert "Jina Reader" in resultado.url_fonte

