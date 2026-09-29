"""Testes unitários para a CLI e integração com a interface Web."""

import pytest
from pathlib import Path
from src.cli import criar_parser
from src.storage import (
    extrair_secao_whatsapp,
    extrair_estudo_completo,
    parse_estudo_markdown,
    exportar_todos_estudos_para_web_data,
)


def test_cli_parser_configuracao_limpa():
    """Valida que a CLI contém as flags modernas de Web e não possui flags legadas de NTFY."""
    parser = criar_parser()
    actions = [act.dest for act in parser._actions]

    # Flags ativas esperadas
    assert "web" in actions
    assert "historico" in actions
    assert "versiculo" in actions
    assert "force" in actions

    # Flags legadas que DEVEM ter sido removidas
    assert "enviar_ntfy" not in actions
    assert "reenviar_hoje" not in actions
    assert "test_ntfy" not in actions


def test_exportacao_web_data_json(tmp_path, monkeypatch):
    """Valida se o compilador Web gera corretamente o arquivo data.js estruturado."""
    pasta_estudos = tmp_path / "estudos"
    pasta_estudos.mkdir(parents=True)
    monkeypatch.setattr("src.storage.ESTUDOS_DIR", pasta_estudos)

    md_content = """---
data: "2026-09-29"
referencia: "Romanos 8:1"
versao: "NVI"
modelo: "gemini-2.5-flash"
gerado_em: "2026-09-29T10:00:00"
---

# Versículo do Dia: Romanos 8:1 (NVI)

> *"Portanto, agora já não há condenação para os que estão em Cristo Jesus."*
> — **Romanos 8:1**

---

## 1. Contexto Histórico & Literário
Paulo escreve aos crentes em Roma enfatizando a justificação pela fé.

## 2. Aplicação Prática
Viva em liberdade em Cristo Jesus.

---

## 📱 Versão para WhatsApp / Compartilhamento Rápido

```text
*Romanos 8:1* - Nenhuma condenação há!
```
"""
    estudo_md = pasta_estudos / "2026-09-29_romanos_8_1.md"
    estudo_md.write_text(md_content, encoding="utf-8")

    destino_js = tmp_path / "web" / "data.js"
    resultado_js = exportar_todos_estudos_para_web_data(destino_js=destino_js)

    assert resultado_js.exists()
    conteudo_js = resultado_js.read_text(encoding="utf-8")
    assert "const HISTORICO_ESTUDOS =" in conteudo_js
    assert "const ESTUDO_ATUAL = HISTORICO_ESTUDOS[0];" in conteudo_js
    assert "Romanos 8:1" in conteudo_js
    assert "Paulo escreve aos crentes em Roma" in conteudo_js


def test_extracao_secoes_markdown():
    """Valida a separação precisa do estudo expositivo e da síntese de compartilhamento."""
    texto_total = """# Estudo Bíblico

Texto de introdução teológica.

---

## 📱 Versão para WhatsApp / Compartilhamento Rápido

```text
Resumo para leitura rápida
```
"""
    zap = extrair_secao_whatsapp(texto_total)
    assert zap == "Resumo para leitura rápida"

    completo = extrair_estudo_completo(texto_total)
    assert "Texto de introdução teológica." in completo
    assert "Versão para WhatsApp" not in completo
