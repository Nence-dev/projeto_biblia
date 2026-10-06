"""Testes unitários para validar referências bíblicas acompanhadas de seus textos completos."""

from pathlib import Path
from src.prompts import SYSTEM_PROMPT_TEOLOGICO, montar_prompt_usuario
from src.storage import parse_estudo_markdown


def test_prompts_mandam_incluir_texto_do_versiculo():
    """Valida se as diretrizes do prompt exigem que cada referência citada venha com o texto literal."""
    assert "texto do versículo em seguida" in SYSTEM_PROMPT_TEOLOGICO.lower() or "texto literal" in SYSTEM_PROMPT_TEOLOGICO.lower()
    assert "transcreva literalmente" in SYSTEM_PROMPT_TEOLOGICO.lower() or "texto do versículo" in SYSTEM_PROMPT_TEOLOGICO.lower()

    prompt_usuario = montar_prompt_usuario("Provérbios 4:23", "Tenha cuidado com o que você pensa", "NVI")
    assert "texto do versículo" in prompt_usuario.lower()
    assert "transcreva literalmente" in prompt_usuario.lower() or "acompanhada do texto" in prompt_usuario.lower()


def test_parse_markdown_preserva_versiculos_completos():
    """Garante que o parser preserva referências com o texto do versículo nos blocos das seções."""
    md_conteudo = """---
data: "2026-09-30"
referencia: "Filipenses 4:6-7"
versao: "NVI"
modelo: "gemini-3.5-flash"
gerado_em: "2026-09-30T10:00:00"
---

# Versículo do Dia: Filipenses 4:6-7 (NVI)

> *"Não andem ansiosos por coisa alguma..."*
> — **Filipenses 4:6-7**

---

### 1. O Contexto Histórico e Narrativo
Paulo escreve aos filipenses a partir da prisão romana.

### 2. A Anatomia do Texto e Teologia Central
A paz de Deus excede todo entendimento.

### 3. O que tirar disso para a prática de hoje?
Submeta tudo a Deus em oração, como lembrado em **1 Pedro 5:7** (*"Lancem sobre ele toda a sua ansiedade, porque ele tem cuidado de vocês"*).

### 4. Conexões Canônicas e Autores da Mesma Linha
Esta oração se harmoniza com as palavras de Jesus em **Mateus 6:34** (*"Portanto, não se preocupem com o amanhã, pois o amanhã trará as suas próprias preocupações"*).
Sobre isso, o teólogo C.S. Lewis pontuava:
> "A oração não muda a Deus, muda a mim."
> — **C.S. Lewis**, *Cartas de um Diabo a seu Aprendiz*

### 5. Fechamento: A Pergunta Central
O que tem roubado a sua paz hoje?

## 📱 Versão para WhatsApp / Compartilhamento Rápido
*Filipenses 4:6-7*
"""
    dados = parse_estudo_markdown(md_conteudo)
    secao_app = next(s for s in dados["secoes"] if s["id"] == "aplicacao")
    assert "1 Pedro 5:7" in secao_app["conteudo"]
    assert "Lancem sobre ele toda a sua ansiedade" in secao_app["conteudo"]

    secao_can = next(s for s in dados["secoes"] if s["id"] == "canonicas")
    assert "Mateus 6:34" in secao_can["conteudo"]
    assert "não se preocupem com o amanhã" in secao_can["conteudo"]


def test_versiculos_relacionados_nao_sao_truncados():
    """Valida se versiculosRelacionados possuem textos integrais e sem reticências desnecessárias."""
    from src.storage import ler_estudo

    # Testa com o estudo real de Provérbios 4:23
    caminho_real = Path(__file__).resolve().parent.parent / "estudos" / "2026-09-29_proverbios_4_23.md"
    if caminho_real.exists():
        conteudo = ler_estudo(caminho_real)
        assert "Marcos 7:21-23" in conteudo
        assert "Ezequiel 36:26" in conteudo
        assert "2 Coríntios 10:5" in conteudo
        assert "Jeremias 17:9" in conteudo

    # Verifica se os arquivos web/data.js existem e contêm os textos completos
    caminho_data_js = Path(__file__).resolve().parent.parent / "web" / "data.js"
    assert caminho_data_js.exists()
    conteudo_js = caminho_data_js.read_text(encoding="utf-8")
    assert "Porque de dentro, do coração dos homens, procedem os maus pensamentos" in conteudo_js
    assert "Darei a vocês um coração novo e porei dentro de vocês um espírito novo" in conteudo_js
    assert "Destruímos argumentos e toda pretensão que se levanta contra o conhecimento de Deus" in conteudo_js
    assert "Enganoso é o coração, mais do que todas as coisas, e desesperadamente corrupto" in conteudo_js


def test_tom_autoral_dialogo_urbano_e_equilibrio():
    """Valida se o prompt incorpora a voz autoral: Engenharia, Teologia, Rock Urbano, ironia e equilíbrio."""
    prompt_lower = SYSTEM_PROMPT_TEOLOGICO.lower()
    assert "engenharia" in prompt_lower
    assert "teologia" in prompt_lower
    assert "rock urbano" in prompt_lower or "rock" in prompt_lower
    assert "ironia" in prompt_lower
    assert "universitário" in prompt_lower
    assert "formalismo pedante" in prompt_lower or "zero formalismo" in prompt_lower
    assert "não tão informal" in prompt_lower or "nem formal" in prompt_lower

