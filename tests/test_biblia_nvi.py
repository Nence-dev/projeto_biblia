"""Testes unitários para o módulo canônico da Bíblia NVI e sua integração com o scraper."""

import pytest
from unittest.mock import patch, MagicMock

from src.biblia_nvi import parsear_referencia, obter_texto_nvi, _limpar_chave
from src.scraper import (
    assegurar_versiculo_em_portugues,
    recuperar_texto_versiculo_em_portugues,
    VersiculoDoDia,
)


def test_parsear_referencia():
    """Valida a extração e normalização de referências bíblicas."""
    casos = [
        ("Colossenses 3:13", ("Colossenses", 3, 13, 13)),
        ("Salmos 46:10", ("Salmos", 46, 10, 10)),
        ("Jeremias 17:7", ("Jeremias", 17, 7, 7)),
        ("Provérbios 22:6", ("Provérbios", 22, 6, 6)),
        ("1 Coríntios 13:4-7", ("1 Coríntios", 13, 4, 7)),
        ("João 3:16", ("João", 3, 16, 16)),
        ("Filipenses 4:6-7", ("Filipenses", 4, 6, 7)),
        ("2 Coríntios 10:5", ("2 Coríntios", 10, 5, 5)),
    ]
    for entrada, esperado in casos:
        assert parsear_referencia(entrada) == esperado, f"Falha para {entrada}"

    # Casos inválidos
    assert parsear_referencia("") is None
    assert parsear_referencia("Texto Aleatório") is None


def test_limpar_chave():
    """Valida a remoção de acentos e caracteres não alfanuméricos."""
    assert _limpar_chave("Colossenses") == "colossenses"
    assert _limpar_chave("Gênesis") == "genesis"
    assert _limpar_chave("1 Coríntios") == "1corintios"
    assert _limpar_chave("Cânticos") == "canticos"


def test_obter_texto_nvi_passagens_conhecidas():
    """Valida que passagens canônicas retornam o texto exato da NVI."""
    texto_colossenses = obter_texto_nvi("Colossenses 3:13")
    assert texto_colossenses == (
        "Suportem uns aos outros e perdoem as queixas que tiverem uns contra os outros. "
        "Perdoem como o Senhor os perdoou."
    )

    texto_salmos = obter_texto_nvi("Salmos 46:10")
    assert texto_salmos == (
        "Parem de lutar e saibam que eu sou Deus! Serei exaltado entre as nações, "
        "serei exaltado na terra."
    )

    texto_jeremias = obter_texto_nvi("Jeremias 17:7")
    assert texto_jeremias == "Mas bendito é o homem cuja confiança está no Senhor, cuja esperança ele é."

    texto_proverbios = obter_texto_nvi("Provérbios 22:6")
    assert texto_proverbios == (
        "Instrua a criança segundo os objetivos que você tem para ela, "
        "e mesmo com o passar dos anos não se desviará deles."
    )


def test_obter_texto_nvi_com_banco_mock():
    """Valida resolução a partir da estrutura canônica de 66 livros."""
    banco_mock = [
        {
            "name": "Efésios",
            "abbrev": "ef",
            "chapters": [
                ["Verso 1:1", "Verso 1:2"],
                ["Verso 2:1", "Verso 2:2", "Verso 2:3", "Verso 2:4", "Verso 2:5", "Verso 2:6", "Verso 2:7", "Pela graça sois salvos..."],
            ],
        }
    ]

    with patch("src.biblia_nvi.carregar_banco_nvi", return_value=banco_mock):
        # Limpa o índice em memória para forçar o recarregamento pelo teste
        import src.biblia_nvi as mod
        mod._INDICE_LIVROS_NVI = {"efesios": banco_mock[0], "ef": banco_mock[0]}

        texto = obter_texto_nvi("Efésios 2:8")
        assert texto == "Pela graça sois salvos..."


def test_scraper_neutraliza_texto_ntlh_e_aplica_nvi():
    """
    Testa o caso crítico reportado pelo usuário:
    O YouVersion entrega referência NVI mas texto da NTLH (ou outra versão).
    O scraper deve substituir automaticamente pelo texto oficial da NVI.
    """
    # Texto real que veio no dia 15/10/2026 da NTLH:
    texto_ntlh = (
        "Não fiquem irritados uns com os outros e perdoem uns aos outros, "
        "caso alguém tenha alguma queixa contra outro. Assim como o Senhor perdoou vocês, "
        "perdoem também eles."
    )

    versiculo_original = VersiculoDoDia(
        referencia="Colossenses 3:13",
        texto=texto_ntlh,
        versao="NVI",
        data="2026-10-15",
    )

    versiculo_corrigido = assegurar_versiculo_em_portugues(versiculo_original)

    # O texto DEVE ter sido substituído pela NVI canônica
    assert versiculo_corrigido.texto == (
        "Suportem uns aos outros e perdoem as queixas que tiverem uns contra os outros. "
        "Perdoem como o Senhor os perdoou."
    )
    assert versiculo_corrigido.versao == "NVI"


def test_scraper_substitui_ntlh_salmos_46_10():
    """Valida a neutralização de texto NTLH para Salmos 46:10."""
    texto_ntlh_salmos = "Parem de lutar e fiquem sabendo que eu sou Deus. Eu sou o Rei das nações; eu sou o Rei do mundo inteiro."

    versiculo_original = VersiculoDoDia(
        referencia="Salmos 46:10",
        texto=texto_ntlh_salmos,
        versao="NVI",
        data="2026-10-14",
    )

    versiculo_corrigido = assegurar_versiculo_em_portugues(versiculo_original)

    assert versiculo_corrigido.texto == (
        "Parem de lutar e saibam que eu sou Deus! Serei exaltado entre as nações, "
        "serei exaltado na terra."
    )
    assert versiculo_corrigido.versao == "NVI"
