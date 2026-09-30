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


def parse_estudo_markdown(conteudo_md: str) -> dict[str, Any]:
    """Extrai campos estruturados do markdown do estudo para formato web com fidelidade total."""
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
    match_ctx = re.search(r"###\s*1\.\s*O Contexto Histórico[^\n]*\n(.*?)(?=###|\Z)", estudo_puro, re.DOTALL)
    if match_ctx:
        conteudo_contexto = sanitizar_texto_markdown_para_web(match_ctx.group(1).strip())

    # 2. Anatomia
    conteudo_anatomia = ""
    termos_originais = []
    match_ana = re.search(r"###\s*2\.\s*A Anatomia do Texto[^\n]*\n(.*?)(?=###|\Z)", estudo_puro, re.DOTALL)
    if match_ana:
        texto_ana = match_ana.group(1).strip()
        padrao_termo = re.finditer(r'\*\s*\*\*"([^"]+)"\*\*\s*\(([^)]+)\):\s*([^\n]+)', texto_ana)
        for pt in padrao_termo:
            termos_originais.append({
                "termo": f"{pt.group(1)} ({pt.group(2)})",
                "significado": pt.group(1),
                "explicacao": pt.group(3).strip(),
            })
        texto_ana_limpo = re.sub(r'^\s*\*\s*\*\*"[^"]+"\*\*.*$\n?', '', texto_ana, flags=re.MULTILINE)
        conteudo_anatomia = sanitizar_texto_markdown_para_web(texto_ana_limpo.strip() or texto_ana)

    # 3. Aplicação
    conteudo_aplicacao = ""
    match_app = re.search(r"###\s*3\.\s*O que tirar disso[^\n]*\n(.*?)(?=###|\Z)", estudo_puro, re.DOTALL)
    if match_app:
        conteudo_aplicacao = sanitizar_texto_markdown_para_web(match_app.group(1).strip())

    # 4. Conexões Canônicas & Citações
    conteudo_canonicas = ""
    citacoes = []
    match_can = re.search(r"###\s*4\.\s*Conexões Canônicas[^\n]*\n(.*?)(?=###|\Z)", estudo_puro, re.DOTALL)
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
    match_perg = re.search(r"###\s*5\.\s*Fechamento[^\n]*\n(.*?)(?=---|\Z)", estudo_puro, re.DOTALL)
    if match_perg:
        conteudo_pergunta = match_perg.group(1).replace("*", "").strip()

    return {
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
    }


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
            if "Provérbios 4:23" in dados.get("referencia", ""):
                dados["comparacaoTraducoes"] = {
                    "titulo": "Comparação Exegética: NVI vs. Texto Original Hebraico",
                    "versaoPrincipal": {
                        "sigla": "NVI (Nova Versão Internacional)",
                        "texto": "Tenha cuidado com o que você pensa, pois a sua vida é dirigida pelos seus pensamentos.",
                        "rotulo": "Ênfase Conceitual Contemporânea",
                        "foco": "Foco na mente, pensamentos e sistema interno de crenças."
                    },
                    "versaoOriginal": {
                        "sigla": "Texto Original Hebraico / ARC Literal",
                        "texto": "Acima de tudo o que se deve guardar, guarda o teu coração, porque dele procedem as fontes da vida.",
                        "rotulo": "Antropologia Bíblica Veterotestamentária",
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
            elif "Romanos 8:1" in dados.get("referencia", ""):
                dados["comparacaoTraducoes"] = {
                    "titulo": "Comparação Exegética: NVI vs. Termo Jurídico Grego",
                    "versaoPrincipal": {
                        "sigla": "NVI (Nova Versão Internacional)",
                        "texto": "Portanto, agora já não há condenação para os que estão em Cristo Jesus.",
                        "rotulo": "Declaração de Plena Absolvição",
                        "foco": "Ausência absoluta de condenação para os justificados."
                    },
                    "versaoOriginal": {
                        "sigla": "Original Grego (Termo Forense / Jurídico)",
                        "texto": "Οὐδὲν ἄρα νῦν κατάκριμα τοῖς ἐν Χριστῷ Ἰησοῦ (Ouden ara nyn katakrima tois en Christō Iēsou)",
                        "rotulo": "Linguagem Forense da Redenção",
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
    destino_js.write_text(js_code, encoding="utf-8")

    # Sincroniza espelho na raiz se presente
    try:
        espelho_raiz = destino_js.parent.parent.parent / "web" / "data.js"
        if espelho_raiz.parent.exists():
            espelho_raiz.write_text(js_code, encoding="utf-8")
    except Exception:
        pass

    return destino_js


def exportar_estudo_para_web_data(caminho_estudo: Path, destino_js: Path | None = None) -> Path:
    """Exporta o histórico completo incluindo o estudo atual para web/data.js."""
    return exportar_todos_estudos_para_web_data(destino_js=destino_js)
