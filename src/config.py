"""Configurações globais e carregamento seguro de variáveis de ambiente."""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env caso exista
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


class ConfigError(Exception):
    """Exceção levantada quando há problemas de configuração ou credenciais."""
    pass


# Provedor e Modelo LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip()

# Versão Bíblica padrão e Mapeamento YouVersion
BIBLIA_VERSAO = os.getenv("BIBLIA_VERSAO", "nvi").strip().lower()

# Códigos de versão da Bíblia no YouVersion (bible.com) para português
YOUVERSION_VERSION_IDS: dict[str, int] = {
    "nvi": 129,    # Nova Versão Internacional
    "ara": 1608,   # Almeida Revista e Atualizada
    "naa": 1840,   # Nova Almeida Atualizada
    "nvt": 1930,   # Nova Versão Transformadora
    "arc": 212,    # Almeida Revista e Corrigida
    "ntlh": 211,   # Nova Tradução na Linguagem de Hoje
}

# Diretório padrão para salvar estudos
ESTUDOS_DIR = Path(os.getenv("ESTUDOS_DIR", str(BASE_DIR / "estudos")))

# URLs Fonte do Versículo do Dia
YOUVERSION_VOTD_URL = "https://www.bible.com/pt/verse-of-the-day"
BIBLIAON_VOTD_URL = "https://www.bibliaon.com/versiculo_do_dia/"


def mask_key(key: str) -> str:
    """Retorna a chave mascarada para exibição segura em logs ou terminal."""
    if not key:
        return "<NÃO CONFIGURADA>"
    if len(key) <= 8:
        return "********"
    return f"{key[:4]}...{key[-4:]}"


def validate_api_key() -> str:
    """Valida se a chave da API Gemini foi definida, levantando erro amigável caso falte."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "sua_chave_gemini_aqui":
        raise ConfigError(
            "GEMINI_API_KEY não foi configurada!\n"
            "Crie um arquivo .env na raiz do projeto baseado no .env.example:\n"
            "  GEMINI_API_KEY=sua_chave_aqui\n"
            "Obtenha sua chave gratuitamente em: https://aistudio.google.com/"
        )
    return GEMINI_API_KEY
