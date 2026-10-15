"""Testes unitários para validação de rotação e diversificação de pensadores e autores de frases."""

import pytest
from pathlib import Path
from unittest.mock import patch

from src.storage import obter_ultimos_autores_frases
from src.prompts import (
    montar_prompt_usuario,
    montar_prompt_minuto,
    PROMPT_SISTEMA_BASE,
    PROMPT_DERIVACAO_MINUTO_COM_DEUS,
)


def test_obter_ultimos_autores_frases_com_arquivos_reais():
    """Valida que a função lê corretamente os estudos recentes e retorna autores distintos."""
    autores = obter_ultimos_autores_frases(limite_dias=2)
    assert isinstance(autores, list)
    # Como o estudo de hoje foi atualizado para Dietrich Bonhoeffer e o de ontem é Tim Keller:
    if len(autores) >= 1:
        assert any(a in ["Dietrich Bonhoeffer", "Tim Keller", "C.S. Lewis"] for a in autores)


def test_obter_ultimos_autores_frases_com_mock(tmp_path):
    """Testa a extração e normalização resiliente de autores a partir de arquivos de estudo."""
    # Cria estudos fictícios em ordem cronológica
    estudo_dia_3 = tmp_path / "2026-10-15_teste_3.md"
    estudo_dia_3.write_text(
        '---\ndata: "2026-10-15"\n---\n```json\n{"autorFrase": "Dietrich Bonhoeffer"}\n```',
        encoding="utf-8",
    )

    estudo_dia_2 = tmp_path / "2026-10-14_teste_2.md"
    estudo_dia_2.write_text(
        '---\ndata: "2026-10-14"\n---\n```json\n{"autorFrase": "@timkeller"}\n```',
        encoding="utf-8",
    )

    estudo_dia_1 = tmp_path / "2026-10-13_teste_1.md"
    estudo_dia_1.write_text(
        '---\ndata: "2026-10-13"\n---\n> — **C.S. Lewis**, *Mero Cristianismo*',
        encoding="utf-8",
    )

    with patch("src.storage.obter_pasta_estudos", return_value=tmp_path):
        ultimos_1 = obter_ultimos_autores_frases(limite_dias=1)
        assert ultimos_1 == ["Dietrich Bonhoeffer"]

        ultimos_2 = obter_ultimos_autores_frases(limite_dias=2)
        assert ultimos_2 == ["Dietrich Bonhoeffer", "Tim Keller"]

        ultimos_3 = obter_ultimos_autores_frases(limite_dias=3)
        assert ultimos_3 == ["Dietrich Bonhoeffer", "Tim Keller", "C.S. Lewis"]


def test_montar_prompt_usuario_injeta_proibicao_de_repeticao():
    """Valida que o prompt do estudo expositivo proíbe explicitamente o autor recente."""
    prompt_sem_restricao = montar_prompt_usuario("Salmos 23:1", "O Senhor é o meu pastor", "NVI")
    assert "REGRA MANDATÓRIA DE ROTAÇÃO" not in prompt_sem_restricao

    autores_recentes = ["Tim Keller"]
    prompt_com_restricao = montar_prompt_usuario(
        "Salmos 23:1",
        "O Senhor é o meu pastor",
        "NVI",
        autores_recentes=autores_recentes,
    )
    assert "REGRA MANDATÓRIA DE ROTAÇÃO DE PENSADORES" in prompt_com_restricao
    assert "'Tim Keller'" in prompt_com_restricao
    assert "É TERMINANTEMENTE PROIBIDO citar 'Tim Keller'" in prompt_com_restricao


def test_montar_prompt_minuto_injeta_proibicao_autor_frase():
    """Valida que o prompt devocional proíbe expressamente repetir o autor da frase do dia anterior."""
    autores_recentes = ["Tim Keller", "Dietrich Bonhoeffer"]
    prompt_minuto = montar_prompt_minuto(
        referencia="Colossenses 3:13",
        texto="Suportem uns aos outros...",
        versao="NVI",
        estudo_gerado="Estudo base...",
        autores_recentes=autores_recentes,
    )

    assert "REGRA MANDATÓRIA DE ROTAÇÃO DA FRASE DO DIA (ANTI-REPETIÇÃO)" in prompt_minuto
    assert "'Tim Keller', 'Dietrich Bonhoeffer'" in prompt_minuto
    assert "É TERMINANTEMENTE PROIBIDO preencher o campo 'autorFrase' com 'Tim Keller', 'Dietrich Bonhoeffer'" in prompt_minuto


def test_prompts_possuem_catalogo_amplo_de_pensadores():
    """Valida que os prompts base e devocionais agora listam múltiplos pensadores históricos."""
    # Lista representativa esperada
    pensadores_esperados = [
        "Dietrich Bonhoeffer",
        "Charles Spurgeon",
        "Santo Agostinho",
        "Martinho Lutero",
        "John Stott",
        "A.W. Tozer",
        "Thomas Watson",
        "Corrie ten Boom",
        "Blaise Pascal",
    ]

    for autor in pensadores_esperados:
        assert autor in PROMPT_SISTEMA_BASE, f"Pensador {autor} não encontrado em PROMPT_SISTEMA_BASE"
        assert autor in PROMPT_DERIVACAO_MINUTO_COM_DEUS, f"Pensador {autor} não encontrado em PROMPT_DERIVACAO_MINUTO_COM_DEUS"
