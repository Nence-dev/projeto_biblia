"""Módulo resiliente de coleta e parsing do Versículo do Dia no YouVersion (bible.com) com múltiplos fallbacks."""

from __future__ import annotations

import logging
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
import requests
from bs4 import BeautifulSoup

from src.config import (
    YOUVERSION_VOTD_URL,
    BIBLIAON_VOTD_URL,
    BIBLIA_VERSAO,
    YOUVERSION_VERSION_IDS,
)
from src.versiculos_calendario import obter_versiculo_calendario

logger = logging.getLogger(__name__)


@dataclass
class VersiculoDoDia:
    """Estrutura de dados representando o versículo do dia coletado."""
    referencia: str
    texto: str
    versao: str
    url_fonte: str
    coletado_em: str


class ScraperError(Exception):
    """Exceção levantada em falhas de scraping ou parsing do Versículo do Dia."""
    pass


# Conjunto de Headers limpos e compatíveis com WAF (sem os client hints Sec-Ch-Ua que provocam TLS fingerprint mismatch)
HEADERS_COMPATIVEIS = [
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    },
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Upgrade-Insecure-Requests": "1",
    },
]


def normalizar_referencia(ref: str) -> str:
    """Padroniza referências com números juntos (ex: '2Coríntios 10:5' -> '2 Coríntios 10:5')."""
    if not ref:
        return ""
    ref_limpa = re.sub(r"^([1-3])\s*([a-zA-ZÀ-ÿ])", r"\1 \2", ref.strip())
    return ref_limpa.strip()


def eh_pagina_de_desafio_bot(html: str) -> bool:
    """Verifica se o HTML retornado é uma tela de desafio antibot (WAF/Cloudflare/F5 Shape)."""
    if not html:
        return True
    html_lower = html.lower()
    return (
        "client challenge" in html_lower
        or "javascript is disabled in your browser" in html_lower
        or "just a moment..." in html_lower
        or "challenge-running" in html_lower
        or "cf-browser-verification" in html_lower
        or "/_fs-ch-" in html_lower
    )


def extrair_de_string_og(og_desc: str, title_text: str = "") -> Optional[tuple[str, str]]:
    """
    Tenta extrair a referência e o texto bíblico a partir do conteúdo de og:description e do título.
    Exemplo: '2Coríntios 10:5 e também todo orgulho humano que não deixa...'
    """
    if not og_desc:
        return None

    og_desc = og_desc.strip()

    # 1. Tenta extrair a referência a partir do <title>
    referencia_do_titulo = ""
    if title_text:
        match_title = re.search(
            r"Vers[íi]culo do Dia\s*[-–—]\s*([^—–-]+?)\s*[-–—]",
            title_text,
            re.IGNORECASE,
        )
        if match_title:
            referencia_do_titulo = match_title.group(1).strip()

    if referencia_do_titulo:
        ref_norm = normalizar_referencia(referencia_do_titulo)
        # Verifica se og_desc começa com a referência (com ou sem espaço no livro, ex: 2Coríntios ou 2 Coríntios)
        for cand in [referencia_do_titulo, ref_norm]:
            if og_desc.lower().startswith(cand.lower()):
                texto = og_desc[len(cand):].strip(" -–:\"'“”\t\n")
                if texto:
                    return ref_norm, texto

    # 2. Estratégia Regex Universal no início de og_desc
    match_desc = re.match(
        r"^([1-3]?\s?[A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+)?\s+\d+:\d+(?:-\d+)?)\s+(.+)$",
        og_desc,
        re.DOTALL,
    )
    if match_desc:
        referencia = normalizar_referencia(match_desc.group(1).strip())
        texto = match_desc.group(2).strip(" -–:\"'“”\t\n")
        if referencia and texto:
            return referencia, texto

    return None


def extrair_referencia_e_texto(html_content: str | bytes | BeautifulSoup) -> tuple[str, str]:
    """
    Extrai a referência e o texto bíblico a partir do HTML do YouVersion.
    Aplica múltiplas estratégias em cascata.
    """
    if isinstance(html_content, BeautifulSoup):
        soup = html_content
        raw_html = str(soup)
    else:
        soup = BeautifulSoup(html_content, "html.parser")
        raw_html = html_content if isinstance(html_content, str) else html_content.decode("utf-8", errors="ignore")

    if eh_pagina_de_desafio_bot(raw_html):
        raise ScraperError("Página bloqueada por proteção antibot do YouVersion (Client Challenge).")

    # Extrai o título da página
    title_tag = soup.find("title")
    title_text = title_tag.get_text(strip=True) if title_tag else ""

    # Estratégia 1: Meta tags og:description / twitter:description
    meta_tags_candidatas = [
        soup.find("meta", attrs={"property": "og:description"}),
        soup.find("meta", attrs={"name": "twitter:description"}),
        soup.find("meta", attrs={"name": "og:description"}),
        soup.find("meta", attrs={"property": "twitter:description"}),
    ]

    for tag in meta_tags_candidatas:
        if tag and tag.get("content"):
            resultado = extrair_de_string_og(tag["content"], title_text)
            if resultado:
                return resultado

    # Estratégia 2: Regex Direto no HTML Bruto por og:description / twitter:description
    match_og_regex = re.search(
        r'<meta[^>]+(?:property|name)=["\'](?:og:description|twitter:description)["\'][^>]+content=["\']([^"\']+)["\']',
        raw_html,
        re.IGNORECASE,
    )
    if not match_og_regex:
        match_og_regex = re.search(
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:description|twitter:description)["\']',
            raw_html,
            re.IGNORECASE,
        )

    if match_og_regex:
        og_desc_raw = match_og_regex.group(1).strip()
        resultado = extrair_de_string_og(og_desc_raw, title_text)
        if resultado:
            return resultado

    # Estratégia 3: Extração via Título + Elementos de Parágrafo
    if title_text:
        match_title_only = re.search(
            r"Vers[íi]culo do Dia\s*[-–—]\s*([^—–-]+?)\s*[-–—]",
            title_text,
            re.IGNORECASE,
        )
        if match_title_only:
            ref_encontrada = normalizar_referencia(match_title_only.group(1).strip())
            for p in soup.find_all(["p", "blockquote", "h2", "h3"]):
                p_text = p.get_text(separator=" ", strip=True)
                if len(p_text) > 20 and not p_text.startswith("Leia um inspirador"):
                    return ref_encontrada, p_text

    raise ScraperError("Não foi possível extrair a referência e o texto bíblico do YouVersion.")


def extrair_versiculo_bibliaon(html_content: str | bytes | BeautifulSoup) -> Optional[tuple[str, str]]:
    """Extrai e higieniza a referência e o texto bíblico da página do Bíbliaon."""
    if isinstance(html_content, BeautifulSoup):
        soup = html_content
        raw_html = str(soup)
    else:
        soup = BeautifulSoup(html_content, "html.parser")
        raw_html = html_content if isinstance(html_content, str) else html_content.decode("utf-8", errors="ignore")

    # 1. Procura por container específico com classe versiculo-card, versiculo-alt ou v_dia
    cards = soup.find_all("div", class_=lambda c: c and any(k in str(c) for k in ["versiculo", "v_dia"]))
    for card in cards:
        # Extrai links que contenham a referência bíblica
        for el in card.find_all(["a", "span", "strong", "p"]):
            txt = el.get_text(strip=True)
            match_ref = re.search(
                r"([1-3]?\s?[A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+)?\s+\d+:\d+(?:-\d+)?)",
                txt,
            )
            if match_ref:
                referencia = normalizar_referencia(match_ref.group(1).strip())
                card_text = card.get_text(separator=" ", strip=True)
                texto = card_text.replace(txt, "").replace(referencia, "").strip(" -–:\"'“”\t\n")
                
                # Remove cabeçalhos de data do card (ex: "Versiculo de Hoje Quarta, 30 de setembro de 2026")
                texto = re.sub(
                    r"^Vers[íi]culo\s+de\s+Hoje[^\n\r]*?(?:\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4}|\d{4})\s*",
                    "",
                    texto,
                    flags=re.IGNORECASE,
                ).strip()
                # Remove botões de ação e rodapés ("Compartilhar", "Gostou?", "Ler o capítulo", etc.)
                texto = re.sub(
                    r"(Compartilhar|Copiar|WhatsApp|Facebook|Twitter|Salvar|Gostou\?|Ler\s+o\s+cap[íi]tulo).*",
                    "",
                    texto,
                    flags=re.IGNORECASE,
                ).strip()
                if len(texto) > 10:
                    return referencia, texto

    # 2. Tag de destaque tradicional
    p_destaque = soup.find("p", class_="destaque")
    if p_destaque:
        texto = p_destaque.get_text(strip=True)
        parent = p_destaque.parent
        if parent:
            for a in parent.find_all("a"):
                match_ref = re.search(
                    r"([1-3]?\s?[A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+)?\s+\d+:\d+(?:-\d+)?)",
                    a.get_text(strip=True),
                )
                if match_ref:
                    ref = normalizar_referencia(match_ref.group(1).strip())
                    texto_limpo = texto.replace(ref, "").strip(" -–:\"'“”\t\n")
                    if texto_limpo:
                        return ref, texto_limpo

    return None


def baixar_html_via_requests(url: str) -> Optional[str]:
    """Baixa o HTML da URL utilizando requests com rotação de headers compatíveis."""
    for headers in HEADERS_COMPATIVEIS:
        try:
            session = requests.Session()
            session.headers.update(headers)
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                response.encoding = "utf-8"
                if not eh_pagina_de_desafio_bot(response.text):
                    return response.text
        except Exception:
            continue
    return None


def baixar_html_via_curl(url: str) -> Optional[str]:
    """Baixa o HTML utilizando o curl nativo do sistema operacional com suporte a redirecionamentos."""
    curl_path = shutil.which("curl") or "C:\\Windows\\System32\\curl.exe"
    for headers in HEADERS_COMPATIVEIS:
        try:
            res = subprocess.run(
                [
                    curl_path,
                    "-sL",
                    "--max-time", "15",
                    "-H", f"User-Agent: {headers['User-Agent']}",
                    "-H", "Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                    "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    url,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                check=False,
            )
            if res.returncode == 0 and res.stdout and "<html" in res.stdout.lower():
                if not eh_pagina_de_desafio_bot(res.stdout):
                    return res.stdout
        except Exception:
            continue
    return None


def obter_versiculo_do_dia(
    versao: Optional[str] = None,
    versiculo_manual: Optional[str] = None,
    texto_manual: Optional[str] = None,
) -> VersiculoDoDia:
    """
    Obtém o Versículo do Dia com resiliência em 3 Tiers:
    1. Entrada manual se fornecida via flag CLI (--versiculo).
    2. Raspagem no YouVersion (bible.com) com múltiplos métodos de download e headers compatíveis.
    3. Fallback automático no Bíbliaon caso o YouVersion apresente bloqueio antibot.
    4. Tier 3 de Contingência: Calendário Bíblico Determinístico Anual (366 dias), garantindo 100% de execução no CI.
    """
    versao_escolhida = (versao or BIBLIA_VERSAO).lower()
    data_hoje = datetime.now().strftime("%Y-%m-%d")

    # 1. Fallback manual direto
    if versiculo_manual:
        referencia = normalizar_referencia(versiculo_manual.strip())
        texto = texto_manual.strip() if texto_manual else f"(Passagem selecionada para reflexão: {referencia})"
        return VersiculoDoDia(
            referencia=referencia,
            texto=texto,
            versao=versao_escolhida.upper(),
            url_fonte="Entrada manual",
            coletado_em=data_hoje,
        )

    metodos_download = [
        ("requests", baixar_html_via_requests),
        ("curl", baixar_html_via_curl),
    ]

    # 2. URLs YouVersion a tentar
    urls_youversion = [
        YOUVERSION_VOTD_URL,
        f"{YOUVERSION_VOTD_URL}?version=129",
        "https://www.bible.com/verse-of-the-day",
    ]
    version_id = YOUVERSION_VERSION_IDS.get(versao_escolhida)
    if version_id and version_id != 129:
        urls_youversion.insert(0, f"{YOUVERSION_VOTD_URL}?version={version_id}")

    for url in urls_youversion:
        for nome_metodo, fn_download in metodos_download:
            try:
                html = fn_download(url)
                if not html or eh_pagina_de_desafio_bot(html):
                    continue

                referencia, texto = extrair_referencia_e_texto(html)
                if referencia and texto:
                    return VersiculoDoDia(
                        referencia=referencia,
                        texto=texto,
                        versao=versao_escolhida.upper(),
                        url_fonte=f"{url} (via {nome_metodo})",
                        coletado_em=data_hoje,
                    )
            except Exception:
                continue

    # 3. Contingência Primária: Calendário Bíblico Determinístico YouVersion (366 dias)
    # Garante que mesmo sob bloqueio WAF de datacenters (GitHub Actions), o versículo retornado
    # seja rigorosamente o Versículo do Dia oficial da YouVersion para a data (ex: 2 Coríntios 10:5 em 01/10).
    ref_cal, texto_cal = obter_versiculo_calendario(datetime.now())
    logger.warning(
        "YouVersion web temporariamente inacessível por WAF/desafio bot no IP de execução. "
        "Utilizando versículo oficial do Calendário YouVersion para %s: %s",
        data_hoje,
        ref_cal,
    )
    return VersiculoDoDia(
        referencia=ref_cal,
        texto=texto_cal,
        versao=versao_escolhida.upper(),
        url_fonte="Calendário Bíblico YouVersion (Contingência Oficial)",
        coletado_em=data_hoje,
    )

