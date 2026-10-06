"""Testes unitários para o módulo de persistência e cache (src/storage.py)."""

import pytest
from pathlib import Path
from src.storage import (
    normalizar_slug,
    salvar_estudo,
    ler_estudo,
    obter_estudo_hoje,
    estudo_existe_hoje,
    listar_historico,
)


def test_normalizar_slug():
    assert normalizar_slug("Romanos 8:1") == "romanos_8_1"
    assert normalizar_slug("1 Coríntios 13:4-7") == "1_corintios_13_4-7"
    assert normalizar_slug("Provérbios 4:23") == "proverbios_4_23"
    assert normalizar_slug("João 3:16") == "joao_3_16"


def test_salvar_e_ler_estudo(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.ESTUDOS_DIR", tmp_path)

    referencia = "Romanos 8:1"
    texto = "Portanto, agora já não há condenação para os que estão em Cristo Jesus."
    versao = "nvi"
    conteudo_estudo = "## 1. O Contexto Histórico\nPaulo escreve à comunidade em Roma..."
    conteudo_whatsapp = "*Romanos 8:1*\nSem condenação em Cristo Jesus!"
    data_teste = "2026-09-29"

    caminho = salvar_estudo(
        referencia=referencia,
        texto_versiculo=texto,
        versao=versao,
        conteudo_estudo=conteudo_estudo,
        conteudo_whatsapp=conteudo_whatsapp,
        data_str=data_teste,
    )

    assert caminho.exists()
    assert caminho.name == "2026-09-29_romanos_8_1.md"

    conteudo_lido = ler_estudo(caminho)
    assert "referencia: \"Romanos 8:1\"" in conteudo_lido
    assert "Portanto, agora já não há condenação" in conteudo_lido
    assert "Paulo escreve à comunidade em Roma" in conteudo_lido
    assert "Versão para WhatsApp" in conteudo_lido
    assert "Sem condenação em Cristo Jesus!" in conteudo_lido


def test_obter_estudo_hoje_e_existencia(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.ESTUDOS_DIR", tmp_path)

    data_teste = "2026-09-29"
    assert not estudo_existe_hoje(data_teste)
    assert obter_estudo_hoje(data_teste) is None

    salvar_estudo(
        referencia="João 3:16",
        texto_versiculo="Porque Deus tanto amou o mundo...",
        versao="NVI",
        conteudo_estudo="Estudo sobre amor divino.",
        data_str=data_teste,
    )

    assert estudo_existe_hoje(data_teste)
    caminho_hoje = obter_estudo_hoje(data_teste)
    assert caminho_hoje is not None
    assert "2026-09-29_joao_3_16.md" in caminho_hoje.name


def test_listar_historico(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.ESTUDOS_DIR", tmp_path)

    salvar_estudo("Salmos 23:1", "O Senhor é o meu pastor...", "NVI", "Estudo 1", data_str="2026-09-28")
    salvar_estudo("Salmos 91:1", "Aquele que habita no abrigo...", "NVI", "Estudo 2", data_str="2026-09-29")

    historico = listar_historico()
    assert len(historico) == 2
    # Ordem cronológica decrescente
    assert historico[0]["data"] == "2026-09-29"
    assert historico[1]["data"] == "2026-09-28"


def test_parse_estudo_markdown_completo(tmp_path):
    from src.storage import parse_estudo_markdown

    conteudo_md = """---
data: "2026-09-29"
referencia: "Provérbios 4:23"
versao: "NVI"
modelo: "gemini-3.5-flash"
gerado_em: "2026-09-29T12:44:00"
---

# Versículo do Dia: Provérbios 4:23 (NVI)

> *"Tenha cuidado com o que você pensa, pois a sua vida é dirigida pelos seus pensamentos."*
> — **Provérbios 4:23**

---

### 1. O Contexto Histórico e Narrativo
Contexto de Salomão educando seu filho.

### 2. A Anatomia do Texto e Teologia Central
No texto hebraico, a palavra coração (*lev*) é o centro de comando.

### 3. O que tirar disso para a prática de hoje?
Não viver de ativismo performático.

### 4. Conexões Canônicas e Autores da Mesma Linha
Conexão com Marcos 7:21-23 e Ezequiel 36:26.
Sobre isso, o teólogo John Stott pontuava:
> "O cristianismo começa onde a moralidade humana termina..."
> — **John Stott**, *A Cruz de Cristo*

### 5. Fechamento: A Pergunta Central
Qual narrativa secreta tem ocupado seus pensamentos?

## 📱 Versão para WhatsApp / Compartilhamento Rápido
*Versão WhatsApp*
"""
    arquivo_md = tmp_path / "2026-09-29_proverbios_4_23.md"
    arquivo_md.write_text(conteudo_md, encoding="utf-8")

    dados = parse_estudo_markdown(arquivo_md)

    assert dados["referencia"] == "Provérbios 4:23"
    assert dados["modelo"] == "gemini-3.5-flash"
    assert dados["data"] == "2026-09-29"
    assert len(dados["secoes"]) >= 5

    # Verifica se a citação teológica de John Stott foi extraída
    secao_canonicas = next(s for s in dados["secoes"] if s["id"] == "canonicas")
    assert len(secao_canonicas["citacoes"]) >= 1
    assert secao_canonicas["citacoes"][0]["autor"] == "John Stott"
    assert "moralidade humana termina" in secao_canonicas["citacoes"][0]["texto"]


def test_exportar_web_data(tmp_path, monkeypatch):
    from src.storage import exportar_todos_estudos_para_web_data, salvar_estudo

    monkeypatch.setattr("src.storage.ESTUDOS_DIR", tmp_path)

    salvar_estudo(
        referencia="Provérbios 4:23",
        texto_versiculo="Tenha cuidado com o que você pensa...",
        versao="NVI",
        conteudo_estudo="### 1. O Contexto Histórico\nContexto\n### 2. A Anatomia do Texto\nAnatomia\n### 3. Prática\nAplicação\n### 4. Conexões Canônicas\nCanônicas\n### 5. Fechamento\nPergunta",
        data_str="2026-09-29",
    )

    destino = tmp_path / "web_test" / "data.js"
    exportar_todos_estudos_para_web_data(destino_js=destino)

    assert destino.exists()
    conteudo_js = destino.read_text(encoding="utf-8")
    assert "const HISTORICO_ESTUDOS =" in conteudo_js
    assert "Provérbios 4:23" in conteudo_js
    assert "comparacaoTraducoes" in conteudo_js
    assert "versiculosRelacionados" in conteudo_js
    assert "cafeComDeusPai" in conteudo_js
