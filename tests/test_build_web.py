"""Geração e validação do web/data.js com base nos estudos reais."""

from pathlib import Path
from src.storage import exportar_todos_estudos_para_web_data


def test_gerar_web_data_com_estudos_reais():
    raiz = Path(__file__).resolve().parent.parent
    pasta_estudos = raiz / "estudos"
    destino_js = raiz / "web" / "data.js"

    resultado = exportar_todos_estudos_para_web_data(
        pasta_estudos=pasta_estudos,
        destino_js=destino_js,
    )

    assert resultado.exists()
    conteudo = resultado.read_text(encoding="utf-8")
    assert "2 Coríntios 10:5" in conteudo
    assert "2026-10-01" in conteudo
    assert "ESTUDO_ATUAL = HISTORICO_ESTUDOS[0]" in conteudo
