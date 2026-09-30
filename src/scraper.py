"""Módulo resiliente de coleta e parsing do Versículo do Dia no YouVersion (bible.com) com fallback."""

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


HEADERS_NAVEGADOR = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/129.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}


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
    Exemplo: 'Provérbios 4:23 Tenha cuidado com o que você pensa, pois a sua vida é dirigida pelos seus pensamentos.'
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

    if referencia_do_titulo and og_desc.lower().startswith(referencia_do_titulo.lower()):
        texto = og_desc[len(referencia_do_titulo):].strip(" -–:\"'“”\t\n")
        if texto:
            return referencia_do_titulo, texto

    # 2. Estratégia Regex Universal em og_desc
    # Padrão: "Provérbios 4:23 Tenha cuidado..." ou "1 João 1:9 Se confessarmos..."
    match_desc = re.match(
        r"^([0-9]?\s?[^\d\n]+?\s+\d+:\d+(?:-\d+)?)\s+(.+)$",
        og_desc,
        re.DOTALL,
    )
    if match_desc:
        referencia = match_desc.group(1).strip()
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

    # Estratégia 3: Extração via Título + Corpo
    if title_text:
        match_title_only = re.search(
            r"Vers[íi]culo do Dia\s*[-–—]\s*([^—–-]+?)\s*[-–—]",
            title_text,
            re.IGNORECASE,
        )
        if match_title_only:
            ref_encontrada = match_title_only.group(1).strip()
            for p in soup.find_all(["p", "blockquote", "h2", "h3"]):
                p_text = p.get_text(separator=" ", strip=True)
                if len(p_text) > 20 and not p_text.startswith("Leia um inspirador"):
                    return ref_encontrada, p_text

    raise ScraperError(
        "Não foi possível extrair a referência e o texto bíblico do YouVersion."
    )


def extrair_versiculo_bibliaon(html_content: str | bytes | BeautifulSoup) -> Optional[tuple[str, str]]:
    """Extrai a referência e o texto bíblico da página do Bíbliaon (serviço alternativo de fallback)."""
    if isinstance(html_content, BeautifulSoup):
        soup = html_content
        raw_html = str(soup)
    else:
        soup = BeautifulSoup(html_content, "html.parser")
        raw_html = html_content if isinstance(html_content, str) else html_content.decode("utf-8", errors="ignore")

    # 1. Procura por container específico com classe versiculo ou v_dia
    cards = soup.find_all("div", class_=lambda c: c and any(k in str(c) for k in ["versiculo", "v_dia"]))
    for card in cards:
        for el in card.find_all(["a", "span", "strong", "p"]):
            txt = el.get_text(strip=True)
            match_ref = re.search(
                r"^([1-3]?\s?[A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+)?\s+\d+:\d+(?:-\d+)?)$",
                txt,
            )
            if match_ref:
                referencia = match_ref.group(1).strip()
                card_text = card.get_text(separator=" ", strip=True)
                texto = card_text.replace(referencia, "").strip(" -–:\"'“”\t\n")
                # Remove cabeçalhos de data do card (ex: "Versiculo de Hoje Quarta, 30 de setembro de 2026")
                texto = re.sub(
                    r"^Vers[íi]culo\s+de\s+Hoje[^\n\r]*?(?:\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4}|\d{4})\s*",
                    "",
                    texto,
                    flags=re.IGNORECASE,
                ).strip()
                # Remove botões de ação e rodapés ("Compartilhar", "Gostou?", etc.)
                texto = re.sub(
                    r"(Compartilhar|Copiar|WhatsApp|Facebook|Twitter|Salvar|Gostou\?).*",
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
                    ref = match_ref.group(1).strip()
                    texto_limpo = texto.replace(ref, "").strip(" -–:\"'“”\t\n")
                    if texto_limpo:
                        return ref, texto_limpo

    # 3. Regex em links bíblicos do Bíbliaon
    match_link = re.search(
        r'<a[^>]+href=["\'](?:https?://www\.bibliaon\.com)?/([a-z0-9_]+)/["\'][^>]*>([1-3]?\s?[A-Za-zÀ-ÿ]+\s+\d+:\d+(?:-\d+)?)</a>',
        raw_html,
        re.IGNORECASE,
    )
    if match_link:
        referencia = match_link.group(2).strip()
        idx = raw_html.find(match_link.group(0))
        snippet = raw_html[max(0, idx - 600) : min(len(raw_html), idx + 600)]
        soup_snippet = BeautifulSoup(snippet, "html.parser")
        for p in soup_snippet.find_all(["p", "blockquote"]):
            p_txt = p.get_text(strip=True)
            if (
                len(p_txt) > 20
                and not p_txt.startswith("Leia")
                and referencia.lower() not in p_txt.lower()
            ):
                return referencia, p_txt

    return None


def baixar_html_via_requests(url: str) -> Optional[str]:
    """Baixa o HTML da URL utilizando requests com sessão e headers realistas."""
    try:
        session = requests.Session()
        session.headers.update(HEADERS_NAVEGADOR)
        response = session.get(url, timeout=12)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
    except Exception:
        return None


def baixar_html_via_curl(url: str) -> Optional[str]:
    """Baixa o HTML utilizando o curl nativo do sistema operacional (Windows/Linux)."""
    curl_path = shutil.which("curl") or "C:\\Windows\\System32\\curl.exe"
    try:
        res = subprocess.run(
            [
                curl_path,
                "-sL",
                "--max-time", "15",
                "-H", f"User-Agent: {HEADERS_NAVEGADOR['User-Agent']}",
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
            return res.stdout
    except Exception:
        pass
    return None


def baixar_html_via_powershell(url: str) -> Optional[str]:
    """Baixa o HTML utilizando PowerShell Invoke-WebRequest nativo do Windows."""
    try:
        cmd = (
            f"[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; "
            f"$headers = @{{'User-Agent'='{HEADERS_NAVEGADOR['User-Agent']}'; 'Accept-Language'='pt-BR,pt;q=0.9'}}; "
            f"(Invoke-WebRequest -Uri '{url}' -UseBasicParsing -Headers $headers -TimeoutSec 15).Content"
        )
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=False,
        )
        if res.returncode == 0 and res.stdout and "<html" in res.stdout.lower():
            return res.stdout
    except Exception:
        pass
    return None


def obter_versiculo_do_dia(
    versao: Optional[str] = None,
    versiculo_manual: Optional[str] = None,
    texto_manual: Optional[str] = None,
) -> VersiculoDoDia:
    """
    Obtém o Versículo do Dia com resiliência em múltiplas etapas:
    1. Entrada manual se fornecida via flag CLI (--versiculo).
    2. Raspagem no YouVersion (bible.com) com múltiplos métodos de download.
    3. Fallback automático para Bíbliaon caso o YouVersion apresente bloqueio antibot (Client Challenge).
    4. Mensagem instrucional clara com comando de fallback manual caso todas as fontes web falhem.
    """
    versao_escolhida = (versao or BIBLIA_VERSAO).lower()
    data_hoje = datetime.now().strftime("%Y-%m-%d")

    # 1. Fallback manual direto
    if versiculo_manual:
        referencia = versiculo_manual.strip()
        texto = texto_manual.strip() if texto_manual else f"(Passagem selecionada para reflexão: {referencia})"
        return VersiculoDoDia(
            referencia=referencia,
            texto=texto,
            versao=versao_escolhida.upper(),
            url_fonte="Entrada manual",
            coletado_em=data_hoje,
        )

    # Métodos de download em ordem de prioridade (requests -> curl nativo -> powershell)
    metodos_download = [
        ("requests", baixar_html_via_requests),
        ("curl", baixar_html_via_curl),
        ("powershell", baixar_html_via_powershell),
    ]

    # 2. URLs YouVersion a tentar
    urls_youversion = []
    version_id = YOUVERSION_VERSION_IDS.get(versao_escolhida)
    if version_id:
        urls_youversion.append(f"{YOUVERSION_VOTD_URL}?version={version_id}")
    urls_youversion.append(YOUVERSION_VOTD_URL)

    for url in urls_youversion:
        for nome_metodo, fn_download in metodos_download:
            try:
                html = fn_download(url)
                if not html or eh_pagina_de_desafio_bot(html):
                    continue

                referencia, texto = extrair_referencia_e_texto(html)
                return VersiculoDoDia(
                    referencia=referencia,
                    texto=texto,
                    versao=versao_escolhida.upper(),
                    url_fonte=f"{url} (via {nome_metodo})",
                    coletado_em=data_hoje,
                )
            except Exception:
                continue

    # 3. Fallback automático no Bíbliaon
    for nome_metodo, fn_download in metodos_download:
        try:
            html = fn_download(BIBLIAON_VOTD_URL)
            if not html or eh_pagina_de_desafio_bot(html):
                continue

            resultado_bibliaon = extrair_versiculo_bibliaon(html)
            if resultado_bibliaon:
                referencia, texto = resultado_bibliaon
                return VersiculoDoDia(
                    referencia=referencia,
                    texto=texto,
                    versao=versao_escolhida.upper(),
                    url_fonte=f"{BIBLIAON_VOTD_URL} (fallback via {nome_metodo})",
                    coletado_em=data_hoje,
                )
        except Exception:
            continue

    # 4. Falha geral amigável
    raise ScraperError(
        "Não foi possível extrair o Versículo do Dia automaticamente "
        "(o YouVersion exige desafio interativo em navegador e as fontes alternativas estão indisponíveis no momento).\n"
        "Você pode executar imediatamente informando o versículo desejado:\n"
        "  python main.py -v 'Provérbios 4:23'\n"
        "  python main.py -v 'Filipenses 4:13' -t 'Tudo posso naquele que me fortalece.'"
    )
