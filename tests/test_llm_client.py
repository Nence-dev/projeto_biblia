"""Testes unitários para prompts e cliente Gemini (src/prompts.py e src/llm_client.py)."""

import pytest
from unittest.mock import MagicMock
from src.prompts import (
    SYSTEM_PROMPT_TEOLOGICO,
    PROMPT_DERIVACAO_WHATSAPP,
    montar_prompt_usuario,
    montar_prompt_whatsapp,
)
from src.llm_client import GeminiClient, LLMError


def test_prompts_contem_diretrizes_essenciais():
    # Valida presença das 5 etapas obrigatórias
    assert "1. O Contexto Histórico e Narrativo" in SYSTEM_PROMPT_TEOLOGICO
    assert "2. A Anatomia do Texto e Teologia Central" in SYSTEM_PROMPT_TEOLOGICO
    assert "3. O que tirar disso para a prática de hoje?" in SYSTEM_PROMPT_TEOLOGICO
    assert "4. Conexões Canônicas e Autores da Mesma Linha" in SYSTEM_PROMPT_TEOLOGICO
    assert "5. Fechamento: A Pergunta Central" in SYSTEM_PROMPT_TEOLOGICO

    # Valida fundamentação reformada e da graça
    assert "reformada, cristocêntrica e da graça" in SYSTEM_PROMPT_TEOLOGICO
    assert "Zé Bruno" in SYSTEM_PROMPT_TEOLOGICO
    assert "teologia da prosperidade" in SYSTEM_PROMPT_TEOLOGICO


def test_montar_prompts():
    prompt_user = montar_prompt_usuario("Gálatas 2:20", "Fui crucificado com Cristo...", "NVI")
    assert "Gálatas 2:20" in prompt_user
    assert "Fui crucificado com Cristo" in prompt_user
    assert "5 etapas" in prompt_user

    prompt_zap = montar_prompt_whatsapp(
        "Gálatas 2:20",
        "Fui crucificado com Cristo...",
        "NVI",
        "Estudo completo gerado anteriormente...",
    )
    assert "Gálatas 2:20" in prompt_zap
    assert "WhatsApp" in prompt_zap
    assert "Estudo completo gerado anteriormente" in prompt_zap


def test_gemini_client_com_mock(monkeypatch):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "## 1. O Contexto Histórico...\nEstudo gerado com sucesso."
    mock_client.models.generate_content.return_value = mock_response

    client = GeminiClient(api_key="AIzaSyDummyKeyForTestingOnly12345")
    client._client = mock_client
    client._use_new_sdk = True
    client._types = MagicMock()

    resultado = client.gerar_estudo_completo("Romanos 8:1", "Sem condenação", "NVI")
    assert "Estudo gerado com sucesso" in resultado
    mock_client.models.generate_content.assert_called_once()


def test_gemini_client_retry_em_503(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda s: None)  # Não espera no teste

    mock_client = MagicMock()
    mock_success = MagicMock()
    mock_success.text = "Sucesso após retry."

    # Primeira chamada falha com 503 UNAVAILABLE, segunda tem sucesso
    mock_client.models.generate_content.side_effect = [
        Exception("503 UNAVAILABLE: This model is currently experiencing high demand."),
        mock_success,
    ]

    client = GeminiClient(api_key="AIzaSyDummyKeyForTestingOnly12345")
    client._client = mock_client
    client._use_new_sdk = True
    client._types = MagicMock()

    resultado = client.gerar_estudo_completo("João 3:16", "Deus amou o mundo", "NVI")
    assert resultado == "Sucesso após retry."
    assert mock_client.models.generate_content.call_count == 2
