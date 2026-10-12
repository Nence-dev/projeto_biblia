"""Módulo de mapeamento canônico bilíngue e normalização de referências bíblicas (Inglês -> Português)."""

from __future__ import annotations

import re
from typing import Optional

# Mapeamento Canônico completo dos 66 Livros da Bíblia (Inglês -> Português)
MAPA_LIVROS_EN_PARA_PT: dict[str, str] = {
    # Antigo Testamento
    "genesis": "Gênesis",
    "exodus": "Êxodo",
    "leviticus": "Levítico",
    "numbers": "Números",
    "deuteronomy": "Deuteronômio",
    "joshua": "Josué",
    "judges": "Juízes",
    "ruth": "Rute",
    "1 samuel": "1 Samuel",
    "2 samuel": "2 Samuel",
    "1 kings": "1 Reis",
    "2 kings": "2 Reis",
    "1 chronicles": "1 Crônicas",
    "2 chronicles": "2 Crônicas",
    "ezra": "Esdras",
    "nehemiah": "Neemias",
    "esther": "Ester",
    "job": "Jó",
    "psalm": "Salmos",
    "psalms": "Salmos",
    "proverb": "Provérbios",
    "proverbs": "Provérbios",
    "ecclesiastes": "Eclesiastes",
    "song of solomon": "Cânticos",
    "song of songs": "Cânticos",
    "canticles": "Cânticos",
    "isaiah": "Isaías",
    "jeremiah": "Jeremias",
    "lamentations": "Lamentações",
    "ezekiel": "Ezequiel",
    "daniel": "Daniel",
    "hosea": "Oséias",
    "joel": "Joel",
    "amos": "Amós",
    "obadiah": "Obadias",
    "jonah": "Jonas",
    "micah": "Miqueias",
    "nahum": "Naum",
    "habakkuk": "Habacuque",
    "zephaniah": "Sofonias",
    "haggai": "Ageu",
    "zechariah": "Zacarias",
    "malachi": "Malaquias",

    # Novo Testamento
    "matthew": "Mateus",
    "mark": "Marcos",
    "luke": "Lucas",
    "john": "João",
    "acts": "Atos",
    "acts of the apostles": "Atos",
    "romans": "Romanos",
    "1 corinthians": "1 Coríntios",
    "2 corinthians": "2 Coríntios",
    "galatians": "Gálatas",
    "ephesians": "Efésios",
    "philippians": "Filipenses",
    "colossians": "Colossenses",
    "1 thessalonians": "1 Tessalonicenses",
    "2 thessalonians": "2 Tessalonicenses",
    "1 timothy": "1 Timóteo",
    "2 timothy": "2 Timóteo",
    "titus": "Tito",
    "philemon": "Filemom",
    "hebrews": "Hebreus",
    "james": "Tiago",
    "1 peter": "1 Pedro",
    "2 peter": "2 Pedro",
    "1 john": "1 João",
    "2 john": "2 João",
    "3 john": "3 João",
    "jude": "Judas",
    "revelation": "Apocalipse",
    "revelations": "Apocalipse",
    "apocalypse": "Apocalipse",
}

# Variações sem espaço (ex.: "1Corinthians", "2Corinthians", "1Samuel")
for _k, _v in list(MAPA_LIVROS_EN_PARA_PT.items()):
    if " " in _k:
        MAPA_LIVROS_EN_PARA_PT[_k.replace(" ", "")] = _v
        # Formas romanas: I Corinthians, II Corinthians
        if _k.startswith("1 "):
            MAPA_LIVROS_EN_PARA_PT["i " + _k[2:]] = _v
            MAPA_LIVROS_EN_PARA_PT["i" + _k[2:]] = _v
        elif _k.startswith("2 "):
            MAPA_LIVROS_EN_PARA_PT["ii " + _k[2:]] = _v
            MAPA_LIVROS_EN_PARA_PT["ii" + _k[2:]] = _v
        elif _k.startswith("3 "):
            MAPA_LIVROS_EN_PARA_PT["iii " + _k[2:]] = _v
            MAPA_LIVROS_EN_PARA_PT["iii" + _k[2:]] = _v

# Abreviações do YouVersion (ex.: PRO.22.6 -> Provérbios)
SIGLAS_YOUVERSION_PARA_PT: dict[str, str] = {
    "GEN": "Gênesis", "EXO": "Êxodo", "LEV": "Levítico", "NUM": "Números", "DEU": "Deuteronômio",
    "JOS": "Josué", "JDG": "Juízes", "RUT": "Rute", "1SA": "1 Samuel", "2SA": "2 Samuel",
    "1KI": "1 Reis", "2KI": "2 Reis", "1CH": "1 Crônicas", "2CH": "2 Crônicas", "EZR": "Esdras",
    "NEH": "Neemias", "EST": "Ester", "JOB": "Jó", "PSA": "Salmos", "PRO": "Provérbios",
    "ECC": "Eclesiastes", "SNG": "Cânticos", "ISA": "Isaías", "JER": "Jeremias", "LAM": "Lamentações",
    "EZK": "Ezequiel", "DAN": "Daniel", "HOS": "Oséias", "JOL": "Joel", "AMO": "Amós",
    "OBA": "Obadias", "JON": "Jonas", "MIC": "Miqueias", "NAM": "Naum", "HAB": "Habacuque",
    "ZEP": "Sofonias", "HAG": "Ageu", "ZEC": "Zacarias", "MAL": "Malaquias", "MAT": "Mateus",
    "MRK": "Marcos", "LUK": "Lucas", "JHN": "João", "ACT": "Atos", "ROM": "Romanos",
    "1CO": "1 Coríntios", "2CO": "2 Coríntios", "GAL": "Gálatas", "EPH": "Efésios", "PHP": "Filipenses",
    "COL": "Colossenses", "1TH": "1 Tessalonicenses", "2TH": "2 Tessalonicenses", "1TI": "1 Timóteo",
    "2TI": "2 Timóteo", "TIT": "Tito", "PHM": "Filemom", "HEB": "Hebreus", "JAS": "Tiago",
    "1PE": "1 Pedro", "2PE": "2 Pedro", "1JN": "1 João", "2JN": "2 João", "3JN": "3 João",
    "JUD": "Judas", "REV": "Apocalipse",
}

# Mapeamento inverso (Português -> Sigla YouVersion)
MAPA_PT_PARA_SIGLA_YOUVERSION: dict[str, str] = {v: k for k, v in SIGLAS_YOUVERSION_PARA_PT.items()}


def normalizar_nome_livro(nome: str) -> str:
    """Normaliza o nome de um livro bíblico (em inglês ou português) para o padrão canônico em português."""
    if not nome:
        return ""
    nome_limpo = nome.strip()
    chave = nome_limpo.lower()

    if chave in MAPA_LIVROS_EN_PARA_PT:
        return MAPA_LIVROS_EN_PARA_PT[chave]

    chave_upper = nome_limpo.upper()
    if chave_upper in SIGLAS_YOUVERSION_PARA_PT:
        return SIGLAS_YOUVERSION_PARA_PT[chave_upper]

    return nome_limpo


def traduzir_referencia_en_para_pt(referencia: str) -> str:
    """
    Traduz uma referência bíblica com nome de livro em inglês para português.
    Exemplos:
      'Proverbs 22:6' -> 'Provérbios 22:6'
      'James 5:16' -> 'Tiago 5:16'
      '1 Corinthians 13:4-7' -> '1 Coríntios 13:4-7'
      'PRO.22.6' -> 'Provérbios 22:6'
    """
    if not referencia:
        return ""

    ref = referencia.strip()

    # Formato sigla YouVersion (ex: PRO.22.6 ou PRO 22:6)
    match_sigla = re.match(r"^([A-Z0-9]{3})[\.:](\d+)[\.:](\d+(?:-\d+)?)$", ref, re.IGNORECASE)
    if match_sigla:
        sigla = match_sigla.group(1).upper()
        cap = match_sigla.group(2)
        vers = match_sigla.group(3)
        livro_pt = SIGLAS_YOUVERSION_PARA_PT.get(sigla, sigla)
        return f"{livro_pt} {cap}:{vers}"

    # Padrão convencional: [Número opcional] [Nome do livro] [capítulo:versículo(s)]
    match_padrao = re.match(
        r"^([1-3]?\s?[A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+)?)\s+(\d+:\d+(?:-\d+)?)$",
        ref,
    )
    if match_padrao:
        livro_raw = match_padrao.group(1).strip()
        cap_vers = match_padrao.group(2).strip()

        livro_pt = normalizar_nome_livro(livro_raw)
        return f"{livro_pt} {cap_vers}"

    return ref


def eh_referencia_em_ingles(referencia: str) -> bool:
    """Verifica se a referência contém livro bíblico com nomenclatura em inglês."""
    if not referencia:
        return False
    ref_lower = referencia.strip().lower()
    for livro_en in MAPA_LIVROS_EN_PARA_PT:
        if ref_lower.startswith(livro_en):
            # Garante que não é falso positivo de nomes idênticos em PT e EN (ex: Daniel, Joel)
            traducao = MAPA_LIVROS_EN_PARA_PT[livro_en]
            if traducao.lower() != livro_en:
                return True
    return False


def eh_texto_em_ingles(texto: str) -> bool:
    """
    Detecta se o texto bíblico está em língua inglesa.
    Baseado em marcadores lexicais comuns em traduções inglesas (NIV, KJV, ESV, NLT).
    """
    if not texto:
        return False
    
    t_lower = f" {texto.lower()} "

    # Palavras funcionais inglesas de alta frequência que não existem em português
    palavras_en = [
        " the ", " and ", " shall ", " unto ", " lord ", " with ", " that ",
        " from ", " their ", " them ", " will ", " your ", " when ", " children ",
        " start ", " they ", " not ", " turn ", " which ", " who ", " his ", " her ",
        " but ", " for ", " god ", " jesus ", " christ ", " have ", " hath "
    ]
    
    contagem_en = sum(1 for p in palavras_en if p in t_lower)
    
    # Marcadores estritos de português
    palavras_pt = [
        " o ", " a ", " os ", " as ", " de ", " do ", " da ", " dos ", " das ",
        " em ", " no ", " na ", " nos ", " nas ", " que ", " para ", " com ",
        " senhor ", " deus ", " cristo ", " jesus ", " se ", " por ", " como "
    ]
    contagem_pt = sum(1 for p in palavras_pt if p in t_lower)

    # Contagem de acentos típicos de português
    acentos_pt = len(re.findall(r"[áàãâéêíóõôúç]", t_lower))

    # Se tiver múltiplos marcadores ingleses e quase nenhum de português/acentos
    if contagem_en >= 3 and contagem_pt <= 1 and acentos_pt == 0:
        return True

    return False


def eh_texto_ou_referencia_em_ingles(texto: str, referencia: str = "") -> bool:
    """Retorna True se a referência ou o texto bíblico capturado estiver em inglês."""
    if eh_referencia_em_ingles(referencia):
        return True
    if eh_texto_em_ingles(texto):
        return True
    return False
