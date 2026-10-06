"""Módulo de persistência e gerenciamento de cache de estudos em arquivos Markdown."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from src.config import ESTUDOS_DIR, GEMINI_MODEL


def normalizar_slug(texto: str) -> str:
    """Converte uma referência bíblica em um slug seguro para nome de arquivo."""
    slug = texto.lower()
    slug = re.sub(r"[àáâãä]", "a", slug)
    slug = re.sub(r"[èéêë]", "e", slug)
    slug = re.sub(r"[ìíîï]", "i", slug)
    slug = re.sub(r"[òóôõö]", "o", slug)
    slug = re.sub(r"[ùúûü]", "u", slug)
    slug = re.sub(r"[ç]", "c", slug)
    slug = re.sub(r"[^\w\s-]", "_", slug)
    slug = re.sub(r"[\s_]+", "_", slug).strip("_")
    return slug


def obter_pasta_estudos() -> Path:
    """Garante a existência da pasta de estudos e a retorna."""
    pasta = Path(ESTUDOS_DIR)
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def obter_estudo_hoje(data_str: str | None = None) -> Path | None:
    """
    Verifica se já existe algum estudo gerado para a data especificada (padrão: hoje).
    Retorna o Path do arquivo ou None.
    """
    if not data_str:
        data_str = datetime.now().strftime("%Y-%m-%d")

    pasta = obter_pasta_estudos()
    # Busca qualquer arquivo que comece com a data especificada
    arquivos = list(pasta.glob(f"{data_str}_*.md"))
    if arquivos:
        return arquivos[0]
    return None


def estudo_existe_hoje(data_str: str | None = None) -> bool:
    """Retorna True se já existe um estudo gerado para a data informada."""
    return obter_estudo_hoje(data_str) is not None


def salvar_estudo(
    referencia: str,
    texto_versiculo: str,
    versao: str,
    conteudo_estudo: str,
    conteudo_whatsapp: str = "",
    conteudo_cafe: dict[str, Any] | str | None = None,
    data_str: str | None = None,
) -> Path:
    """
    Salva o estudo bíblico completo e sua versão WhatsApp em um arquivo Markdown estruturado.
    Retorna o Path do arquivo gerado.
    """
    agora = datetime.now()
    if not data_str:
        data_str = agora.strftime("%Y-%m-%d")

    slug_ref = normalizar_slug(referencia)
    nome_arquivo = f"{data_str}_{slug_ref}.md"
    pasta = obter_pasta_estudos()
    caminho_arquivo = pasta / nome_arquivo

    secao_whatsapp = ""
    if conteudo_whatsapp.strip():
        secao_whatsapp = f"""

---

## 📱 Versão para WhatsApp / Compartilhamento Rápido

```text
{conteudo_whatsapp.strip()}
```
"""

    secao_cafe = ""
    if conteudo_cafe:
        if isinstance(conteudo_cafe, dict):
            texto_cafe = json.dumps(conteudo_cafe, ensure_ascii=False, indent=2)
        else:
            texto_cafe = str(conteudo_cafe).strip()
            if "```" in texto_cafe:
                m = re.search(r"```(?:json)?\s*(.*?)\s*```", texto_cafe, re.DOTALL)
                if m:
                    texto_cafe = m.group(1).strip()
        secao_cafe = f"""

---

## ⏱️ Devocional Minuto com Deus / Café com Deus Pai

```json
{texto_cafe}
```
"""

    conteudo_final = f"""---
data: "{data_str}"
referencia: "{referencia}"
versao: "{versao.upper()}"
modelo: "{GEMINI_MODEL}"
gerado_em: "{agora.isoformat()}"
---

# Versículo do Dia: {referencia} ({versao.upper()})

> *"{texto_versiculo.strip()}"*
> — **{referencia}**

---

{conteudo_estudo.strip()}
{secao_whatsapp}
{secao_cafe}
"""

    caminho_arquivo.write_text(conteudo_final, encoding="utf-8")
    try:
        exportar_estudo_para_web_data(caminho_arquivo)
    except Exception:
        pass
    return caminho_arquivo


def ler_estudo(caminho: Path) -> str:
    """Lê e retorna o conteúdo textual de um estudo existente."""
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de estudo não encontrado: {caminho}")
    return caminho.read_text(encoding="utf-8")


def listar_historico() -> list[dict[str, Any]]:
    """Lista todos os estudos já gerados em ordem cronológica decrescente."""
    pasta = obter_pasta_estudos()
    arquivos = sorted(pasta.glob("*.md"), reverse=True)
    historico = []

    for arq in arquivos:
        nome = arq.stem
        partes = nome.split("_", 1)
        data = partes[0] if len(partes) > 0 else "Desconhecido"
        ref_slug = partes[1] if len(partes) > 1 else ""
        historico.append({
            "caminho": arq,
            "arquivo": arq.name,
            "data": data,
            "referencia_slug": ref_slug,
            "tamanho_bytes": arq.stat().st_size,
        })

    return historico


def extrair_secao_whatsapp(conteudo_md: str) -> str:
    """Extrai o texto preparado para o WhatsApp de dentro do arquivo markdown de estudo."""
    match = re.search(
        r"##\s*📱?\s*Versão para WhatsApp[^\n]*\n+```(?:text)?\n(.*?)\n```",
        conteudo_md,
        re.DOTALL | re.IGNORECASE,
    )
    if match:
        return match.group(1).strip()

    match_header = re.search(
        r"##\s*📱?\s*Versão para WhatsApp[^\n]*\n+(.*)",
        conteudo_md,
        re.DOTALL | re.IGNORECASE,
    )
    if match_header:
        return match_header.group(1).strip()

    return conteudo_md


def extrair_estudo_completo(conteudo_md: str) -> str:
    """Extrai o estudo teológico completo (sem frontmatter YAML e sem a seção resumida para WhatsApp)."""
    # Remove frontmatter YAML se houver
    texto = re.sub(r"^---\n.*?\n---\n+", "", conteudo_md, flags=re.DOTALL)

    # Remove a seção de resumo para WhatsApp
    partes = re.split(r"(?:---\s*\n+)?##\s*📱?\s*Versão para WhatsApp", texto, flags=re.IGNORECASE)
    texto_estudo = partes[0].strip()

    return texto_estudo or conteudo_md.strip()


def formatar_data_extenso(data_str: str) -> str:
    """Converte '2026-09-29' em '29 de Setembro de 2026'."""
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d")
        return f"{dt.day} de {meses[dt.month - 1]} de {dt.year}"
    except Exception:
        return data_str


def sanitizar_texto_markdown_para_web(texto: str) -> str:
    """Higieniza markdown para HTML limpo, eliminando asteriscos soltos e formatando ênfases."""
    if not texto:
        return ""

    # Converte negrito duplo **texto** em <strong>texto</strong>
    texto_formatado = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', texto)

    # Converte itálico *texto* ou _texto_ em <em>texto</em>
    texto_formatado = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', texto_formatado)
    texto_formatado = re.sub(r'_([^_]+)_', r'<em>\1</em>', texto_formatado)

    # Remove marcadores de lista (* item ou - item) transformando em fluxo contínuo
    texto_formatado = re.sub(r'^\s*[*•-]\s+', '', texto_formatado, flags=re.MULTILINE)

    # Remove citações cruas > se sobraram
    texto_formatado = re.sub(r'^\s*>\s*', '', texto_formatado, flags=re.MULTILINE)

    # Remove quaisquer asteriscos órfãos remanescentes
    texto_formatado = texto_formatado.replace("*", "")

    # Normaliza quebras de linha em parágrafos limpos com <br><br>
    texto_formatado = re.sub(r'\n{2,}', '<br><br>', texto_formatado)
    texto_formatado = re.sub(r'\n', ' ', texto_formatado)
    return texto_formatado.strip()


def derivar_titulo_e_leituras_minuto(referencia: str, versiculo_texto: str) -> dict[str, Any]:
    """Deriva um título contextual impactante e leituras bíblicas complementares."""
    ref_upper = (referencia or "").upper()
    v_upper = (versiculo_texto or "").upper()

    if "55:22" in ref_upper or "SUSTER" in v_upper or "FARDO" in v_upper or "PREOCUPAÇ" in v_upper:
        return {
            "titulo": "SUSTENTO INABALÁVEL",
            "fraseDoDia": "Você não foi desenhado para carregar o peso do mundo sozinho; entregue o fardo a Quem sustenta o universo.",
            "autorFrase": "@cslewis",
            "leiturasComplementares": [
                "1 PEDRO 5.7",
                "MATEUS 11.28-30",
                "SALMOS 68.19",
                "FILIPENSES 4.6,7",
                "ISAÍAS 41.10"
            ],
            "leituraComplementar": "1 PEDRO 5.7",
        }
    if "JUDAS" in ref_upper or "DUVID" in v_upper or "MISERICÓRDIA" in v_upper:
        return {
            "titulo": "O ABRIGO DA MISERICÓRDIA",
            "fraseDoDia": "A misericórdia não descarta quem está vacilando; ela estende a mão para curar.",
            "autorFrase": "@timkeller",
            "leiturasComplementares": [
                "LUCAS 15.11-24",
                "MATEUS 12.20",
                "ROMANOS 14.1",
                "GÁLATAS 6.1,2",
                "1 TESSALONICENSES 5.14"
            ],
            "leituraComplementar": "LUCAS 15.11-24",
        }
    if "51:10" in ref_upper or "CORAÇÃO PURO" in v_upper or "PURIFIC" in v_upper:
        return {
            "titulo": "A PUREZA DO CORAÇÃO",
            "fraseDoDia": "Deus não reforma nossa fachada moral; Ele recria o coração a partir do arrependimento sincero.",
            "autorFrase": "@agostinho",
            "leiturasComplementares": [
                "EZEQUIEL 36.26",
                "MATEUS 5.8",
                "1 JOÃO 1.9",
                "SALMOS 24.3,4",
                "TITO 3.5"
            ],
            "leituraComplementar": "EZEQUIEL 36.26",
        }
    if "4:23" in ref_upper or "PENSAMENTO" in v_upper or "GUARDA" in v_upper:
        return {
            "titulo": "A GUARDA DO CORAÇÃO",
            "fraseDoDia": "Vigiar o coração não é viver em paranoia; é proteger a nascente pura para que a vida não adoeça.",
            "autorFrase": "@agostinho",
            "leiturasComplementares": [
                "FILIPENSES 4.8",
                "ROMANOS 12.2",
                "LUCAS 6.45",
                "COLOSSENSES 3.2",
                "SALMOS 139.23,24"
            ],
            "leituraComplementar": "FILIPENSES 4.8",
        }
    if "8:1" in ref_upper or "CONDENA" in v_upper:
        return {
            "titulo": "LIVRES DA CONDENAÇÃO",
            "fraseDoDia": "A cruz liquidou a sentença penal: quem está em Cristo não deve nada ao tribunal da culpa.",
            "autorFrase": "@johnstott",
            "leiturasComplementares": [
                "JOÃO 5.24",
                "ISAÍAS 53.5",
                "ROMANOS 5.1",
                "COLOSSENSES 2.14",
                "HEBREUS 10.14"
            ],
            "leituraComplementar": "JOÃO 5.24",
        }
    if "7:37" in ref_upper or "SEDE" in v_upper or "ÁGUA VIVA" in v_upper:
        return {
            "titulo": "INESGOTÁVEL",
            "fraseDoDia": "Só Deus pode satisfazer o anseio mais íntimo da sua alma.",
            "autorFrase": "@juniorrostirola",
            "leiturasComplementares": [
                "APOCALIPSE 22.17",
                "JEREMIAS 2.13",
                "SALMOS 36.9",
                "JOÃO 4.13,14",
                "ISAÍAS 55.1",
                "ISAÍAS 44.3"
            ],
            "leituraComplementar": "JOÃO 4.13,14",
        }
    if "APOCALIPSE 2" in ref_upper or "PRIMEIRO AMOR" in v_upper:
        return {
            "titulo": "DE VOLTA AO PRIMEIRO AMOR",
            "fraseDoDia": "Lembre-se de onde você caiu e volte ao primeiro amor.",
            "autorFrase": "@juniorrostirola",
            "leiturasComplementares": [
                "JEREMIAS 2.2",
                "MATEUS 24.12",
                "HEBREUS 10.32-36",
                "GÁLATAS 6.9",
                "HEBREUS 6.10-12",
                "JOÃO 21.15-17"
            ],
            "leituraComplementar": "JEREMIAS 2.2",
        }

    if "14:27" in ref_upper or ("PAZ" in v_upper and "PERTURBE" in v_upper):
        return {
            "titulo": "A PAZ INABALÁVEL",
            "fraseDoDia": "A paz de Cristo não é a ausência de tempestades ao redor, mas a presença soberana do Salvador no barco da sua vida.",
            "autorFrase": "@cslewis",
            "leiturasComplementares": [
                "FILIPENSES 4.6,7",
                "COLOSSENSES 3.15",
                "ISAÍAS 26.3",
                "ROMANOS 5.1",
                "SALMOS 4.8"
            ],
            "leituraComplementar": "FILIPENSES 4.6,7",
        }

    return {
        "titulo": "DESCANSO NA PALAVRA",
        "fraseDoDia": "A Palavra de Deus não é um manual de regras frias, é o alicerce vivo para a sua alma hoje.",
        "autorFrase": "@cslewis",
        "leiturasComplementares": [
            "SALMOS 119.105",
            "2 TIMÓTEO 3.16,17",
            "HEBREUS 4.12",
            "TIAGO 1.22"
        ],
        "leituraComplementar": "SALMOS 119.105",
    }


def parse_estudo_markdown(conteudo_md: str | Path) -> dict[str, Any]:
    """Extrai campos estruturados do markdown do estudo para formato web com fidelidade total."""
    if isinstance(conteudo_md, Path):
        conteudo_md = conteudo_md.read_text(encoding="utf-8")
    # Extrair Frontmatter
    match_data = re.search(r'data:\s*"([^"]+)"', conteudo_md)
    data_str = match_data.group(1) if match_data else datetime.now().strftime("%Y-%m-%d")

    match_ref = re.search(r'referencia:\s*"([^"]+)"', conteudo_md)
    referencia = match_ref.group(1) if match_ref else "Passagem Bíblica"

    match_ver = re.search(r'versao:\s*"([^"]+)"', conteudo_md)
    versao = match_ver.group(1) if match_ver else "NVI"

    match_mod = re.search(r'modelo:\s*"([^"]+)"', conteudo_md)
    modelo = match_mod.group(1) if match_mod else "gemini-3.5-flash"

    match_ger = re.search(r'gerado_em:\s*"([^"]+)"', conteudo_md)
    gerado_em = match_ger.group(1) if match_ger else ""

    # Extrair texto do versículo
    match_v_text = re.search(r'>\s*\*"([^"]+)"\*', conteudo_md)
    versiculo_texto = match_v_text.group(1).strip() if match_v_text else ""

    # Extrair WhatsApp
    zap = extrair_secao_whatsapp(conteudo_md)
    if "***" in zap:
        partes_zap = zap.split("***", 1)
        zap = partes_zap[1].strip()
    elif "\n\n*" in zap and not zap.startswith("*"):
        partes_zap = zap.split("\n\n*", 1)
        zap = "*" + partes_zap[1].strip()

    # Extrair Seções
    estudo_puro = extrair_estudo_completo(conteudo_md)

    # 1. Contexto
    conteudo_contexto = ""
    match_ctx = re.search(r"#{2,3}\s*1\.\s*(?:O\s+)?Contexto[^\n]*\n(.*?)(?=\n#{2,3}\s*2\.|\Z)", estudo_puro, re.DOTALL)
    if match_ctx:
        conteudo_contexto = sanitizar_texto_markdown_para_web(match_ctx.group(1).strip())

    # 2. Anatomia
    conteudo_anatomia = ""
    termos_originais = []
    comparacao_extraida = None
    match_ana = re.search(r"#{2,3}\s*2\.\s*(?:A\s+)?Anatomia[^\n]*\n(.*?)(?=\n#{2,3}\s*3\.|\Z)", estudo_puro, re.DOTALL)
    if match_ana:
        texto_ana = match_ana.group(1).strip()

        # 2.1 Extrai Bloco de Comparação de Versões se presente no markdown
        match_comp = re.search(
            r"(?:#{3,4}\s*Comparação[^\n]*\n)(.*?)(?=\n#{3,4}|\Z)",
            texto_ana,
            re.DOTALL | re.IGNORECASE,
        )
        if match_comp:
            bloco_comp = match_comp.group(1).strip()
            m_nvi = re.search(
                r"[-*•]\s*(?:\*\*)?NVI[^*:\n]*:(?:\*\*)?\s*[\"“]?([^\"”\n|]+)[\"”]?(?:\s*\|?\s*(?:\*\*)?Foco:(?:\*\*)?\s*([^\n]+))?",
                bloco_comp,
                re.IGNORECASE,
            )
            m_lit = re.search(
                r"[-*•]\s*(?:\*\*)?(?:Tradução\s+Literal|Literal)[^*:\n]*:(?:\*\*)?\s*[\"“]?([^\"”\n|]+)[\"”]?(?:\s*\|?\s*(?:\*\*)?Foco:(?:\*\*)?\s*([^\n]+))?",
                bloco_comp,
                re.IGNORECASE,
            )
            m_herm = re.search(
                r"[-*•]\s*(?:\*\*)?Chave\s+Hermenêutica[^*:\n]*:(?:\*\*)?\s*([^\n]+)",
                bloco_comp,
                re.IGNORECASE,
            )

            if m_nvi and m_lit:
                texto_nvi = m_nvi.group(1).strip().strip('"“”')
                foco_nvi = (m_nvi.group(2) or "Ênfase na fluidez e inteligibilidade contemporânea.").strip()
                texto_lit = m_lit.group(1).strip().strip('"“”')
                foco_lit = (m_lit.group(2) or "Fidelidade rigorosa ao vocabulário e gramática original.").strip()
                nota_herm = m_herm.group(1).strip() if m_herm else "A comparação de versões evidencia nuances profundas do texto bíblico."

                comparacao_extraida = {
                    "titulo": "Comparação Exegética de Versões",
                    "versaoPrincipal": {
                        "sigla": "NVI (Nova Versão Internacional)",
                        "texto": texto_nvi,
                        "rotulo": "Tradução Dinâmica Contemporânea",
                        "foco": foco_nvi,
                    },
                    "versaoOriginal": {
                        "sigla": "Literal (Tradução ao Pé da Letra)",
                        "rotulo": "Equivalência Formal Estrita",
                        "textoLiteral": texto_lit,
                        "texto": texto_lit,
                        "foco": foco_lit,
                    },
                    "notaHermeneutica": nota_herm,
                }

            # Remove o bloco de comparação da narrativa expositiva
            texto_ana = re.sub(
                r"(?:#{3,4}\s*Comparação[^\n]*\n)(.*?)(?=\n#{3,4}|\Z)",
                "",
                texto_ana,
                flags=re.DOTALL | re.IGNORECASE,
            ).strip()

        # 2.2 Extrai Termos Originais
        match_termos = re.search(
            r"(?:#{3,4}\s*Termos\s+Originais[^\n]*\n)(.*?)(?=\n#{3,4}|\Z)",
            texto_ana,
            re.DOTALL | re.IGNORECASE,
        )
        bloco_termos = match_termos.group(1) if match_termos else texto_ana

        padrao_termo = re.finditer(
            r'[-*•]\s*\*\*["“]?([^"”*]+)["”]?\*\*\s*(?:\(([^)]+)\))?:\s*([^|\n]+)(?:\s*\|\s*([^\n]+))?',
            bloco_termos,
        )
        for pt in padrao_termo:
            nome = pt.group(1).strip()
            grafia = pt.group(2).strip() if pt.group(2) else ""
            sig = pt.group(3).strip()
            exp = pt.group(4).strip() if pt.group(4) else sig
            termos_originais.append({
                "termo": f"{nome} ({grafia})" if grafia else nome,
                "significado": sig,
                "explicacao": exp,
            })

        if match_termos:
            texto_ana = re.sub(
                r"(?:#{3,4}\s*Termos\s+Originais[^\n]*\n)(.*?)(?=\n#{3,4}|\Z)",
                "",
                texto_ana,
                flags=re.DOTALL | re.IGNORECASE,
            ).strip()

        texto_ana_limpo = re.sub(r'^\s*[-*•]\s*\*\*.*$\n?', '', texto_ana, flags=re.MULTILINE)
        conteudo_anatomia = sanitizar_texto_markdown_para_web(texto_ana_limpo.strip() or texto_ana)

    # 3. Aplicação
    conteudo_aplicacao = ""
    match_app = re.search(r"#{2,3}\s*(?:2|3)\.\s*(?:O que tirar disso|Aplicação)[^\n]*\n(.*?)(?=\n#{2,3}\s*4\.|\Z)", estudo_puro, re.DOTALL)
    if match_app:
        conteudo_aplicacao = sanitizar_texto_markdown_para_web(match_app.group(1).strip())

    # 4. Conexões Canônicas & Citações
    conteudo_canonicas = ""
    citacoes = []
    match_can = re.search(r"#{2,3}\s*4\.\s*Conexões Canônicas[^\n]*\n(.*?)(?=\n#{2,3}\s*5\.|\Z)", estudo_puro, re.DOTALL)
    if match_can:
        texto_can = match_can.group(1).strip()
        padrao_citacao = re.finditer(
            r'>\s*[*"]*([^"\n*]+)[*"]*\s*\n>\s*—\s*\*\*([^*]+)\*\*,\s*\*([^*]+)\*',
            texto_can,
        )
        for pc in padrao_citacao:
            citacoes.append({
                "autor": pc.group(2).strip(),
                "obra": pc.group(3).strip(),
                "texto": pc.group(1).strip(),
            })

        if not citacoes:
            padrao_sec = re.finditer(
                r'\*\*([^*]+)\*\*(?:,\s*em\s*\*([^*]+)\*)?[^>]*>\s*[*"]*([^"\n*]+)[*"]*',
                texto_can,
                re.DOTALL,
            )
            for ps in padrao_sec:
                citacoes.append({
                    "autor": ps.group(1).strip(),
                    "obra": (ps.group(2) or "").strip(),
                    "texto": ps.group(3).strip(),
                })

        partes_can = re.split(r"(?:Sobre isso|Sobre ess[ae]|Do mesmo modo|Quanto a isso)[^\n]*:", texto_can, flags=re.IGNORECASE)
        if len(partes_can) > 1 and partes_can[0].strip():
            conteudo_canonicas = sanitizar_texto_markdown_para_web(partes_can[0].strip())
        else:
            texto_can_limpo = re.sub(r'^\s*>[^\n]*$\n?', '', texto_can, flags=re.MULTILINE)
            conteudo_canonicas = sanitizar_texto_markdown_para_web(texto_can_limpo.strip() or texto_can)

    # 5. Pergunta Central
    conteudo_pergunta = ""
    match_perg = re.search(r"#{2,3}\s*5\.\s*Fechamento[^\n]*\n(.*?)(?=\n#{2,3}\s*📱|---|##\s*📱|\Z)", estudo_puro, re.DOTALL)
    if match_perg:
        conteudo_pergunta = match_perg.group(1).replace("*", "").strip()

    # 6. Minuto com Deus / Café com Deus Pai
    match_minuto = re.search(
        r"##\s*[⏱️☕]?\s*(?:Devocional\s+)?(?:Minuto com Deus|Café com Deus Pai)[^\n]*[\s\S]*?```(?:json)?\n(.*?)\n```",
        conteudo_md,
        re.DOTALL | re.IGNORECASE,
    )
    minuto_com_deus = None
    if match_minuto:
        try:
            minuto_com_deus = json.loads(match_minuto.group(1).strip())
        except Exception:
            pass

    match_cafe = re.search(
        r"##\s*☕?\s*Café com Deus Pai[^\n]*[\s\S]*?```(?:json)?\n(.*?)\n```",
        conteudo_md,
        re.DOTALL | re.IGNORECASE,
    )
    cafe_com_deus_pai = None
    if match_cafe and not minuto_com_deus:
        try:
            cafe_com_deus_pai = json.loads(match_cafe.group(1).strip())
        except Exception:
            pass

    info_contextual = derivar_titulo_e_leituras_minuto(referencia, versiculo_texto)

    if minuto_com_deus:
        if not minuto_com_deus.get("titulo") or minuto_com_deus.get("titulo") in ["NOVOS COMEÇOS", "REFLEXÃO DO DIA"]:
            minuto_com_deus["titulo"] = info_contextual["titulo"]
        if not minuto_com_deus.get("leiturasComplementares"):
            minuto_com_deus["leiturasComplementares"] = info_contextual["leiturasComplementares"]
        if not minuto_com_deus.get("leituraComplementar"):
            minuto_com_deus["leituraComplementar"] = info_contextual["leituraComplementar"]
        if not minuto_com_deus.get("autorFrase"):
            minuto_com_deus["autorFrase"] = info_contextual["autorFrase"]

        texto_dev = minuto_com_deus.get("textoDevocional", "")
        if "<br" not in texto_dev and "\n\n" in texto_dev:
            texto_dev_formatado = "<br><br>".join([p.strip() for p in texto_dev.split("\n\n") if p.strip()])
            minuto_com_deus["textoDevocional"] = texto_dev_formatado
        elif "<br" not in texto_dev and "\n" in texto_dev:
            texto_dev_formatado = "<br><br>".join([p.strip() for p in texto_dev.split("\n") if p.strip()])
            minuto_com_deus["textoDevocional"] = texto_dev_formatado

        cafe_com_deus_pai = {
            "aromaManha": minuto_com_deus.get("fraseDoDia", info_contextual["fraseDoDia"]),
            "vozDoPai": minuto_com_deus.get("textoDevocional", ""),
            "palavraMesa": f"Em {referencia}: \"{versiculo_texto}\".",
            "oracaoMesa": "Pai amado, que Tua graça nos acompanhe hoje. Amém.",
            "cafeParaLevar": minuto_com_deus.get("fraseDoDia", info_contextual["fraseDoDia"])
        }
    elif cafe_com_deus_pai and not minuto_com_deus:
        texto_dev = cafe_com_deus_pai.get("textoDevocional") or f"{cafe_com_deus_pai.get('aromaManha', '')}\n\n{cafe_com_deus_pai.get('palavraMesa', '')}\n\n{cafe_com_deus_pai.get('vozDoPai', '')}"
        minuto_com_deus = {
            "titulo": cafe_com_deus_pai.get("titulo") or info_contextual["titulo"],
            "fraseDoDia": cafe_com_deus_pai.get("fraseDoDia") or cafe_com_deus_pai.get("cafeParaLevar", info_contextual["fraseDoDia"]),
            "autorFrase": cafe_com_deus_pai.get("autorFrase", info_contextual["autorFrase"]),
            "leiturasComplementares": cafe_com_deus_pai.get("leiturasComplementares", info_contextual["leiturasComplementares"]),
            "leituraComplementar": cafe_com_deus_pai.get("leituraComplementar", info_contextual["leituraComplementar"]),
            "textoDevocional": texto_dev
        }
    elif not minuto_com_deus and not cafe_com_deus_pai:
        minuto_com_deus = {
            "titulo": info_contextual["titulo"],
            "fraseDoDia": info_contextual["fraseDoDia"],
            "autorFrase": info_contextual["autorFrase"],
            "leiturasComplementares": info_contextual["leiturasComplementares"],
            "leituraComplementar": info_contextual["leituraComplementar"],
            "textoDevocional": (
                f"Há momentos na vida em que sentimos que o peso das circunstâncias ultrapassa as nossas forças. "
                f"Naquele instante, a ansiedade parece ditar o fim da história. Mas a mensagem de {referencia} nos resgata: \"{versiculo_texto}\". "
                f"O Senhor não nos chamou para sermos os sustentadores solitários de nossa própria vida, mas para descarregarmos a carga sobre os Seus ombros fortes."
            )
        }
        cafe_com_deus_pai = {
            "aromaManha": "Puxe a cadeira devagar e respire fundo. Antes de qualquer notificação ou pressa do dia, o Pai está aqui com você, servindo paz fresca sobre a mesa da sua vida.",
            "vozDoPai": f"Filho, Eu conheço cada inquietação que você trouxe para este dia. Você não precisa carregar o peso do amanhã sozinho. Descanse o coração nas Minhas mãos.",
            "palavraMesa": f"Em {referencia}, o Senhor nos lembra do Seu cuidado presente: \"{versiculo_texto}\". Esta promessa é um abraço seguro de quem nunca dorme cuidando de você.",
            "oracaoMesa": "Meu Pai, obrigado por esta manhã e por Tua presença paciente. Ensina-me a saborear Tua graça e a confiar que o Teu amor é suficiente para cada passo das minhas próximas horas. Amém.",
            "cafeParaLevar": info_contextual["fraseDoDia"]
        }

    resultado = {
        "data": data_str,
        "dataFormatada": formatar_data_extenso(data_str),
        "referencia": referencia,
        "versao": versao,
        "modelo": modelo,
        "geradoEm": gerado_em,
        "versiculoTexto": versiculo_texto,
        "genero": "Literatura de Sabedoria / Bíblica",
        "secoes": [
            {
                "id": "contexto",
                "titulo": "1. O Contexto Histórico e Narrativo",
                "icone": "scroll",
                "conteudo": conteudo_contexto,
            },
            {
                "id": "anatomia",
                "titulo": "2. A Anatomia do Texto e Teologia Central",
                "icone": "book-open",
                "termosOriginais": termos_originais,
                "conteudo": conteudo_anatomia,
            },
            {
                "id": "aplicacao",
                "titulo": "3. O que tirar disso para a prática de hoje?",
                "icone": "compass",
                "conteudo": conteudo_aplicacao,
            },
            {
                "id": "canonicas",
                "titulo": "4. Conexões Canônicas & A Obra de Cristo",
                "icone": "cross",
                "citacoes": citacoes,
                "conteudo": conteudo_canonicas,
            },
            {
                "id": "fechamento",
                "titulo": "5. Pergunta Central para Meditação",
                "icone": "help-circle",
                "pergunta": conteudo_pergunta,
            },
        ],
        "devocionalWhatsApp": zap,
        "minutoComDeus": minuto_com_deus,
        "cafeComDeusPai": cafe_com_deus_pai,
    }

    if comparacao_extraida:
        resultado["comparacaoTraducoes"] = comparacao_extraida

    return resultado


def exportar_todos_estudos_para_web_data(
    pasta_estudos: Path | None = None,
    destino_js: Path | None = None,
) -> Path:
    """
    Lê todos os estudos Markdown na pasta de estudos, compila o histórico ordenado
    por data decrescente e exporta para web/data.js (contendo HISTORICO_ESTUDOS e ESTUDO_ATUAL).
    Sincroniza automaticamente a pasta principal e a pasta do repositório limpo.
    """
    if not pasta_estudos:
        pasta_estudos = obter_pasta_estudos()
    if not destino_js:
        destino_js = Path(__file__).resolve().parent.parent / "web" / "data.js"

    arquivos = sorted(pasta_estudos.glob("*.md"), reverse=True)
    if not arquivos:
        return destino_js

    historico = []
    for arq in arquivos:
        try:
            conteudo = ler_estudo(arq)
            dados = parse_estudo_markdown(conteudo)

            # Enriquecimento exegético e comparativo para Provérbios 4:23
            if "Provérbios 4:23" in dados.get("referencia", "") and not dados.get("comparacaoTraducoes"):
                dados["comparacaoTraducoes"] = {
                    "titulo": "Comparação Exegética de Versões",
                    "versaoPrincipal": {
                        "sigla": "NVI (Nova Versão Internacional)",
                        "texto": "Tenha cuidado com o que você pensa, pois a sua vida é dirigida pelos seus pensamentos.",
                        "rotulo": "Tradução Dinâmica Contemporânea",
                        "foco": "Foco na mente, pensamentos e sistema interno de crenças."
                    },
                    "versaoOriginal": {
                        "sigla": "Literal (Tradução ao Pé da Letra)",
                        "rotulo": "Equivalência Formal Estrita",
                        "textoLiteral": "Acima de tudo o que se deve guardar, guarda o teu coração, porque dele procedem as fontes da vida.",
                        "texto": "Acima de tudo o que se deve guardar, guarda o teu coração, porque dele procedem as fontes da vida.",
                        "foco": "Coração (Lev) como centro de comando integrado (mente, vontade e afetos); Fontes (Totsawot Chayyim) da existência."
                    },
                    "notaHermeneutica": "A NVI foca na faculdade mental ('o que você pensa'), enquanto o original hebraico estabelece uma prioridade absoluta ('mikal-mishmar'): guardar o homem interior (lev), pois é dele que jorram os canais que determinam todas as ações e o destino da vida."
                }
                dados["versiculosRelacionados"] = [
                    {
                        "referencia": "Marcos 7:21-23",
                        "texto": "Porque de dentro, do coração dos homens, procedem os maus pensamentos, as imoralidades sexuais, os roubos, os homicídios, os adultérios, as cobiças, as maldades, o engano, a devassidão, a inveja, a calúnia, o orgulho e a insensatez. Todos esses males vêm de dentro e tornam o homem impuro.",
                        "contexto": "Jesus conecta o pecado à lavoura oculta do coração humano."
                    },
                    {
                        "referencia": "Ezequiel 36:26",
                        "texto": "Darei a vocês um coração novo e porei dentro de vocês um espírito novo; tirarei de vocês o coração de pedra e lhes darei um coração de carne.",
                        "contexto": "A promessa da Nova Aliança: regeneração interior pelo Espírito Santo."
                    },
                    {
                        "referencia": "2 Coríntios 10:5",
                        "texto": "Destruímos argumentos e toda pretensão que se levanta contra o conhecimento de Deus, e levamos cativo todo pensamento à obediência de Cristo.",
                        "contexto": "Submissão diária da mente à soberania e graça de Jesus."
                    },
                    {
                        "referencia": "Jeremias 17:9",
                        "texto": "Enganoso é o coração, mais do que todas as coisas, e desesperadamente corrupto. Quem é capaz de compreendê-lo?",
                        "contexto": "O diagnóstico bíblico da insuficiência da força moral humana."
                    }
                ]
                for secao in dados.get("secoes", []):
                    if secao["id"] == "anatomia":
                        secao["termosOriginais"] = [
                            {
                                "termo": "Lev (לֵב)",
                                "significado": "Coração / Centro de Comando",
                                "explicacao": "Na antropologia bíblica, abrange a mente (pensamentos), a vontade (escolhas) e os afetos (desejos)."
                            },
                            {
                                "termo": "Mikal-mishmar (מִכָּל־מִשְׁמָר)",
                                "significado": "Acima de tudo o que se guarda",
                                "explicacao": "Indica prioridade absoluta sobre bens, reputação ou conquistas exteriores."
                            },
                            {
                                "termo": "Totsawot Chayyim (תּוֹצְאוֹת חַיִּים)",
                                "significado": "Fontes / Nascentes da Vida",
                                "explicacao": "Canais de irrigação que deságuam inevitavelmente em ações, palavras e no destino da existência."
                            },
                            {
                                "termo": "Hokmah (חָכְמָה)",
                                "significado": "Sabedoria Prática Divina",
                                "explicacao": "A literatura sapiencial de Israel transmitida para orientar o homem no caminho reto da aliança."
                            }
                        ]
                    if secao["id"] == "canonicas" and not secao.get("citacoes"):
                        secao["citacoes"] = [
                            {
                                "autor": "John Stott",
                                "obra": "A Cruz de Cristo",
                                "texto": "O cristianismo começa onde a moralidade humana termina: com a confissão da nossa bancarrota espiritual e a necessidade de sermos renovados no centro do nosso ser."
                            },
                            {
                                "autor": "C.S. Lewis",
                                "obra": "Mero Cristianismo",
                                "texto": "Aproximar-se de Deus faz com que você perceba que tem 'pensamentos' que nunca imaginou ter. O cristianismo não diz que o homem bom é aquele que nunca tem um pensamento ruim, mas aquele que usa a mente para render-se a Cristo, permitindo que Ele limpe a casa."
                            }
                        ]

            # Enriquecimento exegético e comparativo para Romanos 8:1
            # Enriquecimento exegético e comparativo para Romanos 8:1
            elif "Romanos 8:1" in dados.get("referencia", "") and not dados.get("comparacaoTraducoes"):
                dados["comparacaoTraducoes"] = {
                    "titulo": "Comparação Exegética de Versões",
                    "versaoPrincipal": {
                        "sigla": "NVI (Nova Versão Internacional)",
                        "texto": "Portanto, agora já não há condenação para os que estão em Cristo Jesus.",
                        "rotulo": "Tradução Dinâmica Contemporânea",
                        "foco": "Ausência absoluta de condenação para os justificados."
                    },
                    "versaoOriginal": {
                        "sigla": "Literal (Tradução ao Pé da Letra)",
                        "rotulo": "Equivalência Formal Estrita",
                        "textoLiteral": "Nenhuma condenação, portanto, há agora para os que estão em Cristo Jesus.",
                        "texto": "Nenhuma condenação, portanto, há agora para os que estão em Cristo Jesus.",
                        "foco": "Katakrima: extinção jurídica simultânea tanto do veredito de culpa quanto da execução da pena penal."
                    },
                    "notaHermeneutica": "O termo forense 'katakrima' comprova que a dívida judicial foi liquidada no tribunal divino na cruz. Estar 'en Christō' significa que a justiça do Filho veste o crente de forma irrevogável."
                }
                dados["versiculosRelacionados"] = [
                    {
                        "referencia": "João 5:24",
                        "texto": "Quem ouve a minha palavra e crê naquele que me enviou tem a vida eterna e não será condenado, mas passou da morte para a vida.",
                        "contexto": "Jesus ratifica o fim definitivo de todo juízo condenatório para os redimidos."
                    },
                    {
                        "referencia": "Isaías 53:5",
                        "texto": "Mas ele foi traspassado por causa das nossas transgressões, foi esmagado por causa de nossas iniquidades; o castigo que nos trouxe paz estava sobre ele, e pelas suas feridas fomos curados.",
                        "contexto": "A profecia do Servo Sofredor que suportou o peso integral da condenação."
                    }
                ]
                for secao in dados.get("secoes", []):
                    if secao["id"] == "anatomia":
                        secao["termosOriginais"] = [
                            {
                                "termo": "Katakrima (κατάκριμα)",
                                "significado": "Condenação / Sentença Judicial",
                                "explicacao": "Termo estritamente jurídico que abrange tanto o veredito de culpa quanto a execução penal, totalmente liquidada na cruz."
                            },
                            {
                                "termo": "Nyn (νῦν)",
                                "significado": "Agora / Nova Era Inaugurada",
                                "explicacao": "Advérbio temporal que marca o encerramento definitivo do tribunal acusatório pela graça."
                            },
                            {
                                "termo": "En Christō Iēsou (ἐν Χριστῷ Ἰησοῦ)",
                                "significado": "Em Cristo Jesus / União Mística",
                                "explicacao": "A condição salvífica exclusiva: o status de justiça do próprio Filho agora veste o crente."
                            }
                        ]
                    if secao["id"] == "canonicas" and not secao.get("citacoes"):
                        secao["citacoes"] = [
                            {
                                "autor": "Martyn Lloyd-Jones",
                                "obra": "Romanos: O Capítulo 8",
                                "texto": "O diabo tentará convencê-lo de que, por causa do seu pecado de hoje, você voltou a estar debaixo da condenação. Mas o apóstolo declara: 'Nenhuma condenação há'. Não é uma questão de sentimentos variáveis, mas do veredito irrevogável do Juiz de toda a terra em Cristo."
                            },
                            {
                                "autor": "John Stott",
                                "obra": "A Mensagem de Romanos",
                                "texto": "Estar em Cristo significa que a nossa segurança não repousa na firmeza da nossa fé, mas na fidelidade daquele em quem fomos enxertados."
                            }
                        ]

            # Enriquecimento exegético e comparativo para João 14:27
            elif "14:27" in dados.get("referencia", "") and not dados.get("comparacaoTraducoes"):
                dados["comparacaoTraducoes"] = {
                    "titulo": "Comparação Exegética de Versões",
                    "versaoPrincipal": {
                        "sigla": "NVI (Nova Versão Internacional)",
                        "texto": "Deixo a paz a vocês; a minha paz lhes dou. Não a dou como o mundo a dá. Não se perturbe o seu coração, nem tenham medo.",
                        "rotulo": "Tradução Dinâmica Contemporânea",
                        "foco": "A promessa consoladora do Salvador aos discípulos com uma dádiva pessoal e eterna."
                    },
                    "versaoOriginal": {
                        "sigla": "Literal (Tradução ao Pé da Letra)",
                        "rotulo": "Equivalência Formal Estrita",
                        "textoLiteral": "Paz vos deixo, a minha paz vos dou; não como o mundo dá, eu vo-la dou. Não se turbe o vosso coração, nem se intimide.",
                        "texto": "Paz vos deixo, a minha paz vos dou; não como o mundo dá, eu vo-la dou. Não se turbe o vosso coração, nem se intimide.",
                        "foco": "Eirēnē (εἰρήνη) como shalom messiânico e o imperativo negativo mē tarassesthō (cessar a agitação interior)."
                    },
                    "notaHermeneutica": "No cenáculo, antes da cruz, Jesus lega aos discípulos não bens terrenos ou ausência de conflitos, mas a Sua própria paz — reconciliação plena com Deus que dissipa o pânico e o medo."
                }
                dados["versiculosRelacionados"] = [
                    {
                        "referencia": "Filipenses 4:7",
                        "texto": "E a paz de Deus, que excede todo o entendimento, guardará os seus corações e as suas mentes em Cristo Jesus.",
                        "contexto": "Paulo descreve a paz sobrenatural que atua como sentinela guardando o íntimo do crente."
                    },
                    {
                        "referencia": "Isaías 26:3",
                        "texto": "Tu guardarás em perfeita paz aquele cujo propósito está firme, porque em ti confia.",
                        "contexto": "A profecia do shalom perfeito para quem ancora a mente no Senhor."
                    }
                ]
                for secao in dados.get("secoes", []):
                    if secao["id"] == "anatomia" and not secao.get("termosOriginais"):
                        secao["termosOriginais"] = [
                            {
                                "termo": "Eirēnē (εἰρήνη)",
                                "significado": "Paz / Shalom Messiânico / Reconciliação",
                                "explicacao": "Mais que mera ausência de conflito exterior; significa integridade de alma, harmonia e comunhão restabelecida com Deus."
                            },
                            {
                                "termo": "Tarassesthō (ταρασσέσθω)",
                                "significado": "Não se perturbe / Não se agite como água revolta",
                                "explicacao": "Imperativo presente com negação no grego, ordenando estancar a comoção interna contínua provocada pela angústia."
                            },
                            {
                                "termo": "Deiliatō (δειλιάτω)",
                                "significado": "Não tenha medo / Não se acovarde",
                                "explicacao": "Verbo que descreve o recuo covarde diante da batalha. Cristo ordena coragem fundamentada em Sua vitória."
                            }
                        ]
                    if secao["id"] == "canonicas" and not secao.get("citacoes"):
                        secao["citacoes"] = [
                            {
                                "autor": "J.C. Ryle",
                                "obra": "Meditações nos Evangelhos: João",
                                "texto": "A paz que Cristo dá não é a calmaria efêmera de um mar dormente, mas a âncora firme da alma ancorada na rocha eterna durante o mais violento temporal."
                            },
                            {
                                "autor": "C.S. Lewis",
                                "obra": "Mero Cristianismo",
                                "texto": "Deus não pode nos dar uma felicidade e uma paz separadas de Si mesmo, porque isso simplesmente não existe fora d'Ele."
                            }
                        ]

            historico.append(dados)
        except Exception:
            continue

    if not historico:
        return destino_js

    js_code = (
        "/**\n"
        " * Dados dos Estudos Bíblicos (Histórico Completo) para visualização na interface Web.\n"
        " * Atualizado automaticamente pelo Projeto Bíblia com suporte exegético e comparações.\n"
        " */\n"
        f"const HISTORICO_ESTUDOS = {json.dumps(historico, ensure_ascii=False, indent=4)};\n\n"
        "const ESTUDO_ATUAL = HISTORICO_ESTUDOS[0];\n"
    )
    destino_js.parent.mkdir(parents=True, exist_ok=True)
    destino_js.write_text(js_code, encoding="utf-8")

    return destino_js


def exportar_estudo_para_web_data(caminho_estudo: Path, destino_js: Path | None = None) -> Path:
    """Exporta o histórico completo incluindo o estudo atual para web/data.js."""
    pasta_estudos = caminho_estudo.parent
    if not destino_js:
        candidato_web = pasta_estudos.parent / "web" / "data.js"
        if candidato_web.parent.exists():
            destino_js = candidato_web
        elif "pytest" not in str(pasta_estudos).lower():
            destino_js = Path(__file__).resolve().parent.parent / "web" / "data.js"
        else:
            destino_js = pasta_estudos / "web" / "data.js"
    return exportar_todos_estudos_para_web_data(pasta_estudos=pasta_estudos, destino_js=destino_js)
