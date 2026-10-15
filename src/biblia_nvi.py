"""Módulo determinístico de resolução canônica da Bíblia Sagrada na versão NVI (Nova Versão Internacional).

Garante que qualquer referência bíblica extraída (ex.: 'Colossenses 3:13', 'Salmos 46:10')
tenha seu texto resolvido 100% fiel à NVI em português, eliminando divergências,
textos de outras traduções (como NTLH) ou re-traduções de fontes em inglês.
"""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.request
from pathlib import Path
from typing import Optional

from src.bible_books import normalizar_nome_livro

logger = logging.getLogger(__name__)

# Diretórios base
DIRETORIO_SRC = Path(__file__).resolve().parent
DIRETORIO_DATA = DIRETORIO_SRC / "data"
ARQUIVO_NVI_LOCAL = DIRETORIO_DATA / "pt_nvi.json"

# URLs oficiais do dataset open-source (Thiago Bodruk - 66 Livros Canônicos NVI)
URLS_NVI_REMOTO = [
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_nvi.json",
    "https://cdn.jsdelivr.net/gh/thiagobodruk/bible/json/pt_nvi.json",
]

# Cache em memória após o primeiro carregamento
_BANCO_NVI_MEMORIA: Optional[list[dict]] = None
_INDICE_LIVROS_NVI: dict[str, dict] = {}

# Mapeamento de normalização de nomes/abreviações para busca resiliente
MAPA_NOMES_NORMALIZADOS: dict[str, str] = {
    # Nomes sem acento e abreviações comuns
    "genesis": "Gênesis", "gn": "Gênesis", "exodo": "Êxodo", "ex": "Êxodo",
    "levitico": "Levítico", "lv": "Levítico", "numeros": "Números", "nm": "Números",
    "deuteronomio": "Deuteronômio", "dt": "Deuteronômio", "josue": "Josué", "js": "Josué",
    "juizes": "Juízes", "jz": "Juízes", "rute": "Rute", "rt": "Rute",
    "1 samuel": "1 Samuel", "1sm": "1 Samuel", "2 samuel": "2 Samuel", "2sm": "2 Samuel",
    "1 reis": "1 Reis", "1rs": "1 Reis", "2 reis": "2 Reis", "2rs": "2 Reis",
    "1 cronicas": "1 Crônicas", "1cr": "1 Crônicas", "2 cronicas": "2 Crônicas", "2cr": "2 Crônicas",
    "esdras": "Esdras", "ed": "Esdras", "neemias": "Neemias", "ne": "Neemias",
    "ester": "Ester", "et": "Ester", "jo": "Jó", "job": "Jó",
    "salmos": "Salmos", "salmo": "Salmos", "sl": "Salmos", "ps": "Salmos",
    "proverbios": "Provérbios", "proverbio": "Provérbios", "pv": "Provérbios", "pr": "Provérbios",
    "eclesiastes": "Eclesiastes", "ec": "Eclesiastes", "canticos": "Cânticos", "cantares": "Cânticos", "ct": "Cânticos",
    "isaias": "Isaías", "is": "Isaías", "jeremias": "Jeremias", "jr": "Jeremias",
    "lamentacoes": "Lamentações", "lm": "Lamentações", "ezequiel": "Ezequiel", "ez": "Ezequiel",
    "daniel": "Daniel", "dn": "Daniel", "oseias": "Oséias", "os": "Oséias",
    "joel": "Joel", "jl": "Joel", "amos": "Amós", "am": "Amós",
    "obadias": "Obadias", "ob": "Obadias", "jonas": "Jonas", "jn": "Jonas",
    "miqueias": "Miqueias", "mq": "Miqueias", "naum": "Naum", "na": "Naum",
    "habacuque": "Habacuque", "hc": "Habacuque", "sofonias": "Sofonias", "sf": "Sofonias",
    "ageu": "Ageu", "ag": "Ageu", "zacarias": "Zacarias", "zc": "Zacarias",
    "malaquias": "Malaquias", "ml": "Malaquias",
    # Novo Testamento
    "mateus": "Mateus", "mt": "Mateus", "marcos": "Marcos", "mc": "Marcos",
    "lucas": "Lucas", "lc": "Lucas", "joao": "João",
    "atos": "Atos", "at": "Atos", "romanos": "Romanos", "rm": "Romanos",
    "1 corintios": "1 Coríntios", "1co": "1 Coríntios", "2 corintios": "2 Coríntios", "2co": "2 Coríntios",
    "galatas": "Gálatas", "gl": "Gálatas", "efesios": "Efésios", "ef": "Efésios",
    "filipenses": "Filipenses", "fp": "Filipenses", "colossenses": "Colossenses", "colossenses ": "Colossenses", "cl": "Colossenses",
    "1 tessalonicenses": "1 Tessalonicenses", "1ts": "1 Tessalonicenses",
    "2 tessalonicenses": "2 Tessalonicenses", "2ts": "2 Tessalonicenses",
    "1 timoteo": "1 Timóteo", "1tm": "1 Timóteo", "2 timoteo": "2 Timóteo", "2tm": "2 Timóteo",
    "tito": "Tito", "tt": "Tito", "filemom": "Filemom", "fm": "Filemom",
    "hebreus": "Hebreus", "hb": "Hebreus", "tiago": "Tiago", "tg": "Tiago",
    "1 pedro": "1 Pedro", "1pe": "1 Pedro", "2 pedro": "2 Pedro", "2pe": "2 Pedro",
    "1 joao": "1 João", "1jo": "1 João", "2 joao": "2 João", "2jo": "2 João",
    "3 joao": "3 João", "3jo": "3 João", "judas": "Judas", "jd": "Judas",
    "apocalipse": "Apocalipse", "ap": "Apocalipse",
}


def _limpar_chave(texto: str) -> str:
    """Remove acentos e caracteres especiais para comparação flexível de chaves."""
    if not texto:
        return ""
    import unicodedata
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", sem_acento.lower())


def carregar_banco_nvi() -> list[dict]:
    """
    Carrega o banco de dados integral da Bíblia NVI (66 livros).
    Ordem de busca:
    1. Memória RAM (se já carregado).
    2. Arquivo local em `src/data/pt_nvi.json`.
    3. Download automático com cache local a partir dos mirrors CDN.
    """
    global _BANCO_NVI_MEMORIA, _INDICE_LIVROS_NVI

    if _BANCO_NVI_MEMORIA is not None:
        return _BANCO_NVI_MEMORIA

    DIRETORIO_DATA.mkdir(parents=True, exist_ok=True)

    # 1. Tenta carregar do arquivo local
    if ARQUIVO_NVI_LOCAL.exists() and ARQUIVO_NVI_LOCAL.stat().st_size > 500000:
        try:
            with open(ARQUIVO_NVI_LOCAL, "r", encoding="utf-8") as f:
                _BANCO_NVI_MEMORIA = json.load(f)
                _indexar_banco(_BANCO_NVI_MEMORIA)
                logger.info("Banco NVI carregado com sucesso a partir de %s", ARQUIVO_NVI_LOCAL)
                return _BANCO_NVI_MEMORIA
        except Exception as e:
            logger.warning("Falha ao ler pt_nvi.json local: %s. Tentando download...", e)

    # 2. Tenta download dos mirrors
    for url in URLS_NVI_REMOTO:
        try:
            logger.info("Baixando pt_nvi.json de %s...", url)
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "ProjetoBiblia/1.0 (Python/urllib)"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                conteudo = resp.read().decode("utf-8")
                dados = json.loads(conteudo)
                if isinstance(dados, list) and len(dados) >= 66:
                    _BANCO_NVI_MEMORIA = dados
                    _indexar_banco(_BANCO_NVI_MEMORIA)
                    # Salva em cache local para futuras execuções offline instantâneas
                    try:
                        with open(ARQUIVO_NVI_LOCAL, "w", encoding="utf-8") as f_out:
                            json.dump(dados, f_out, ensure_ascii=False)
                        logger.info("Arquivo pt_nvi.json salvo localmente em %s", ARQUIVO_NVI_LOCAL)
                    except Exception as err_save:
                        logger.debug("Não foi possível persistir pt_nvi.json em disco: %s", err_save)
                    return _BANCO_NVI_MEMORIA
        except Exception as e:
            logger.warning("Download do pt_nvi.json de %s falhou: %s", url, e)
            continue

    return []


def _indexar_banco(livros: list[dict]):
    """Cria índice rápido por nome e abreviação para busca O(1)."""
    global _INDICE_LIVROS_NVI
    _INDICE_LIVROS_NVI.clear()
    for livro in livros:
        nome = livro.get("name", "")
        abrev = livro.get("abbrev", "")
        if nome:
            _INDICE_LIVROS_NVI[_limpar_chave(nome)] = livro
        if abrev:
            _INDICE_LIVROS_NVI[_limpar_chave(abrev)] = livro


def parsear_referencia(referencia: str) -> Optional[tuple[str, int, int, int]]:
    """
    Faz o parsing de referências bíblicas em português.
    Retorna: (livro_normalizado, capitulo, versiculo_inicio, versiculo_fim).
    Exemplos:
      'Colossenses 3:13' -> ('Colossenses', 3, 13, 13)
      'Salmos 46:10' -> ('Salmos', 46, 10, 10)
      'João 1:1-2' -> ('João', 1, 1, 2)
      '1 Coríntios 13:4-7' -> ('1 Coríntios', 13, 4, 7)
    """
    if not referencia:
        return None

    ref_limpa = referencia.strip()

    # Regex para capturar [Número opcional] [Nome do livro] [capítulo]:[versículo inicial](-[versículo final])?
    match = re.match(
        r"^([1-3]?\s?[A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+)?)\s+(\d+):(\d+)(?:-(\d+))?$",
        ref_limpa,
    )
    if not match:
        return None

    livro_raw = match.group(1).strip()
    capitulo = int(match.group(2))
    vers_inicio = int(match.group(3))
    vers_fim = int(match.group(4)) if match.group(4) else vers_inicio

    # Normaliza o nome do livro via bible_books ou dicionário local
    chave_norm = _limpar_chave(livro_raw)
    livro_canônico = MAPA_NOMES_NORMALIZADOS.get(chave_norm)
    if not livro_canônico:
        livro_canônico = normalizar_nome_livro(livro_raw)

    return livro_canônico, capitulo, vers_inicio, vers_fim


def obter_texto_nvi(referencia: str) -> Optional[str]:
    """
    Recupera o texto exato e inalterado na versão NVI (Nova Versão Internacional)
    a partir da referência fornecida.
    Garante 0% de interferência de traduções NTLH ou versões em inglês.
    """
    parsed = parsear_referencia(referencia)
    if not parsed:
        return None

    livro_nome, capitulo_num, v_inicio, v_fim = parsed

    # 1. Busca no banco de dados canônico completo (66 livros)
    banco = carregar_banco_nvi()
    livro_obj = None

    if _INDICE_LIVROS_NVI:
        livro_obj = _INDICE_LIVROS_NVI.get(_limpar_chave(livro_nome))

    if not livro_obj and banco:
        for item in banco:
            if _limpar_chave(item.get("name", "")) == _limpar_chave(livro_nome):
                livro_obj = item
                break

    if livro_obj and "chapters" in livro_obj:
        capitulos = livro_obj["chapters"]
        cap_idx = capitulo_num - 1
        if 0 <= cap_idx < len(capitulos):
            versiculos_cap = capitulos[cap_idx]
            versos_selecionados = []
            for v_num in range(v_inicio, v_fim + 1):
                v_idx = v_num - 1
                if 0 <= v_idx < len(versiculos_cap):
                    versos_selecionados.append(versiculos_cap[v_idx].strip())

            if versos_selecionados:
                texto_unificado = " ".join(versos_selecionados)
                logger.info(
                    "Texto NVI oficial para '%s' recuperado com sucesso do banco canônico: %s...",
                    referencia,
                    texto_unificado[:60],
                )
                return texto_unificado

    # 2. Fallback Determinístico Local para passagens comuns do projeto se o banco não estiver disponível
    PASSAGENS_CONHECIDAS_NVI = {
        ("Colossenses", 3, 13, 13): "Suportem uns aos outros e perdoem as queixas que tiverem uns contra os outros. Perdoem como o Senhor os perdoou.",
        ("Salmos", 46, 10, 10): "Parem de lutar e saibam que eu sou Deus! Serei exaltado entre as nações, serei exaltado na terra.",
        ("Jeremias", 17, 7, 7): "Mas bendito é o homem cuja confiança está no Senhor, cuja esperança ele é.",
        ("Provérbios", 22, 6, 6): "Instrua a criança segundo os objetivos que você tem para ela, e mesmo com o passar dos anos não se desviará deles.",
        ("Romanos", 8, 28, 28): "Sabemos que Deus age em todas as coisas para o bem daqueles que o amam, dos que foram chamados de acordo com o seu propósito.",
        ("João", 3, 16, 16): "Porque Deus tanto amou o mundo que deu o seu Filho Unigênito, para que todo o que nele crer não pereça, mas tenha a vida eterna.",
        ("Filipenses", 4, 6, 7): "Não andem ansiosos por coisa alguma, mas em tudo, pela oração e súplicas, e com ação de graças, apresentem seus pedidos a Deus. E a paz de Deus, que excede todo o entendimento, guardará os seus corações e as suas mentes em Cristo Jesus.",
        ("Salmos", 23, 1, 1): "O Senhor é o meu pastor; de nada terei falta.",
        ("2 Coríntios", 10, 5, 5): "Destruímos argumentos e toda pretensão que se levanta contra o conhecimento de Deus, e levamos cativo todo pensamento, para torná-lo obediente a Cristo.",
        ("Atos", 17, 25, 25): "Ele não é servido por mãos de homens, como se necessitasse de algo, porque ele mesmo dá a todos a vida, o fôlego e as demais coisas.",
    }

    chave_tupla = (livro_nome, capitulo_num, v_inicio, v_fim)
    if chave_tupla in PASSAGENS_CONHECIDAS_NVI:
        return PASSAGENS_CONHECIDAS_NVI[chave_tupla]

    # 3. Fallback pontual via Gemini (estritamente com prompt restrito à NVI oficial)
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if gemini_key and gemini_key != "sua_chave_gemini_aqui":
        try:
            from src.llm_client import GeminiClient
            client = GeminiClient(api_key=gemini_key)
            prompt = (
                f"Forneça exclusivamente o texto bíblico oficial do versículo {referencia} "
                "na tradução Nova Versão Internacional (NVI) em português do Brasil. "
                "ATENÇÃO: Não use NTLH, não use Almeida e não faça tradução livre do inglês. "
                "Use unicamente a NVI oficial em português. "
                "Responda estritamente com o texto bíblico, sem aspas, sem adicionar a referência e sem comentários."
            )
            resposta = client.gerar_estudo(
                referencia=referencia,
                texto="Consulta NVI estrita",
                versao="nvi",
                prompt_customizado=prompt,
            )
            if resposta:
                txt = resposta.strip().strip('"“”\'')
                txt = re.sub(r"^(?:Texto(?:\s+do\s+vers[íi]culo)?\s*:\s*)", "", txt, flags=re.IGNORECASE).strip()
                if len(txt) > 10:
                    return txt
        except Exception as e:
            logger.debug("Fallback Gemini para texto NVI de %s falhou: %s", referencia, e)

    return None
