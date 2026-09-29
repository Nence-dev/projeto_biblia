"""Interface de Linha de Comando (CLI) interativa com visualização Rich."""

from __future__ import annotations

import argparse
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Confirm, Prompt

from src.config import (
    BIBLIA_VERSAO,
    GEMINI_MODEL,
    mask_key,
    GEMINI_API_KEY,
)
from src.scraper import obter_versiculo_do_dia, ScraperError
from src.llm_client import GeminiClient, LLMError
from src.storage import (
    obter_estudo_hoje,
    salvar_estudo,
    ler_estudo,
    listar_historico,
    obter_pasta_estudos,
    extrair_secao_whatsapp,
    extrair_estudo_completo,
    exportar_estudo_para_web_data,
)


console = Console()


def exibir_banner() -> None:
    """Exibe o cabeçalho estilizado do projeto no terminal."""
    texto_banner = (
        "[bold cyan]📖 VERSÍCULO DO DIA & TEOLOGIA EXPOSITIVA[/bold cyan]\n"
        "[dim]Coleta no YouVersion (bible.com) + Reflexão Reformada & Cristocêntrica (Gemini)[/dim]"
    )
    console.print(Panel(texto_banner, border_style="cyan", expand=False))


def abrir_arquivo_no_sistema(caminho: Path) -> None:
    """Abre o arquivo Markdown gerado no aplicativo padrão do sistema operacional."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(caminho))
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", str(caminho)], check=False)
        else:
            subprocess.run(["xdg-open", str(caminho)], check=False)
    except Exception as exc:
        console.print(f"[yellow]Não foi possível abrir o arquivo automaticamente: {exc}[/yellow]")


def abrir_web_no_navegador(caminho_web: Path | None = None) -> None:
    """Abre a interface Web Local (web/index.html) no navegador padrão do sistema operacional."""
    import webbrowser

    if caminho_web is None:
        caminho_web = Path(__file__).resolve().parent.parent / "web" / "index.html"

    if not caminho_web.exists():
        console.print(f"[bold red]Arquivo da interface web não encontrado em: {caminho_web}[/bold red]")
        return

    console.print(
        Panel(
            f"🌐 [bold green]Abrindo Interface Web Local no Navegador...[/bold green]\n"
            f"[dim]Arquivo:[/dim] [cyan]{caminho_web.resolve()}[/cyan]",
            border_style="green",
        )
    )
    try:
        webbrowser.open(caminho_web.resolve().as_uri())
    except Exception as exc:
        try:
            abrir_arquivo_no_sistema(caminho_web)
        except Exception:
            console.print(f"[yellow]Não foi possível abrir o navegador automaticamente: {exc}[/yellow]")


def comando_listar_historico() -> None:
    """Exibe uma tabela no terminal com todos os estudos já gerados."""
    historico = listar_historico()
    if not historico:
        console.print("[yellow]Nenhum estudo salvo encontrado na pasta de estudos.[/yellow]")
        return

    tabela = Table(title="📚 Histórico de Estudos Bíblicos Gerados", border_style="cyan")
    tabela.add_column("Data", style="green", no_wrap=True)
    tabela.add_column("Arquivo / Referência", style="bold white")
    tabela.add_column("Tamanho", style="dim", justify="right")

    for item in historico:
        tamanho_kb = f"{item['tamanho_bytes'] / 1024:.1f} KB"
        tabela.add_row(item["data"], item["arquivo"], tamanho_kb)

    console.print(tabela)


def executar_fluxo(args: argparse.Namespace) -> None:
    """Executa o fluxo principal de coleta, análise teológica e gravação."""
    exibir_banner()

    # Se solicitado apenas o histórico
    if args.historico:
        comando_listar_historico()
        return

    data_hoje = datetime.now().strftime("%Y-%m-%d")

    # Se a flag --web foi solicitada diretamente e já existe estudo hoje, abre no navegador
    if getattr(args, "web", False) and not args.force and not args.versiculo:
        estudo_existente = obter_estudo_hoje(data_hoje)
        if estudo_existente:
            try:
                exportar_estudo_para_web_data(estudo_existente)
            except Exception:
                pass
            abrir_web_no_navegador()
            return

    # 1. Verificação de Cache / Estudo já existente no dia (se não for forçado e nem versículo manual)
    if not args.force and not args.versiculo:
        estudo_existente = obter_estudo_hoje(data_hoje)
        if estudo_existente:
            console.print(
                Panel(
                    f"⚠️ [bold yellow]O estudo de hoje já foi gerado anteriormente![/bold yellow]\n\n"
                    f"📁 Arquivo: [cyan]{estudo_existente}[/cyan]\n"
                    f"Deseja reutilizar o estudo existente para evitar consumir tokens da API?",
                    title="Cache do Dia",
                    border_style="yellow",
                )
            )

            try:
                usar_existente = Confirm.ask("Ler o estudo existente agora?", default=True)
            except (KeyboardInterrupt, EOFError):
                usar_existente = True

            if usar_existente:
                conteudo = ler_estudo(estudo_existente)
                console.print(Markdown(conteudo))
                if args.abrir:
                    abrir_arquivo_no_sistema(estudo_existente)
                return
            else:
                console.print("[cyan]Regenerando o estudo com a API Gemini (--force ativo)...[/cyan]")


    # 2. Coleta do Versículo do Dia (Scraper YouVersion ou Manual)
    versao = args.versao or BIBLIA_VERSAO
    try:
        if args.versiculo:
            console.print(f"[cyan]ℹ️ Utilizando versículo manual informado: [bold]{args.versiculo}[/bold][/cyan]")
            versiculo = obter_versiculo_do_dia(
                versao=versao,
                versiculo_manual=args.versiculo,
                texto_manual=args.texto,
            )
        else:
            with console.status(f"[bold green]Coletando Versículo do Dia em bible.com ({versao.upper()})...", spinner="dots"):
                versiculo = obter_versiculo_do_dia(versao=versao)
    except ScraperError as err:
        console.print(Panel(f"[bold red]Erro na Coleta:[/bold red]\n{err}", border_style="red"))
        sys.exit(1)

    # Exibe o versículo coletado
    painel_versiculo = (
        f"[bold white]{versiculo.texto}[/bold white]\n\n"
        f"[dim]— {versiculo.referencia} ({versiculo.versao}) | Fonte: {versiculo.url_fonte}[/dim]"
    )
    console.print(Panel(painel_versiculo, title="📖 Versículo Selecionado", border_style="green"))

    # 3. Inicialização do Cliente Gemini e Geração Teológica Expositiva
    try:
        client = GeminiClient(model_name=args.modelo or GEMINI_MODEL)
    except Exception as err:
        console.print(Panel(f"[bold red]Configuração da API Gemini:[/bold red]\n{err}", border_style="red"))
        sys.exit(1)

    with console.status("[bold blue]Consultando o Especialista Teológico Expositivo (Gemini)...", spinner="bouncingBall"):
        try:
            estudo_gerado = client.gerar_estudo_completo(
                referencia=versiculo.referencia,
                texto=versiculo.texto,
                versao=versiculo.versao,
                on_status=lambda msg: console.log(f"[yellow]{msg}[/yellow]"),
            )
        except LLMError as err:
            console.print(Panel(f"[bold red]Falha na Geração do Estudo:[/bold red]\n{err}", border_style="red"))
            sys.exit(1)

    # 4. Geração da Derivação para WhatsApp
    with console.status("[bold magenta]Elaborando síntese para WhatsApp e Redes Sociais...", spinner="dots"):
        try:
            whatsapp_gerado = client.gerar_derivacao_whatsapp(
                referencia=versiculo.referencia,
                texto=versiculo.texto,
                versao=versiculo.versao,
                estudo_gerado=estudo_gerado,
                on_status=lambda msg: console.log(f"[yellow]{msg}[/yellow]"),
            )
        except LLMError as err:
            console.print(f"[yellow]Aviso: Não foi possível gerar a derivação para WhatsApp: {err}[/yellow]")
            whatsapp_gerado = ""

    # 5. Salvamento no armazenamento local em Markdown
    caminho_salvo = salvar_estudo(
        referencia=versiculo.referencia,
        texto_versiculo=versiculo.texto,
        versao=versiculo.versao,
        conteudo_estudo=estudo_gerado,
        conteudo_whatsapp=whatsapp_gerado,
        data_str=data_hoje,
    )

    # 6. Exibição no Terminal
    if args.whatsapp and whatsapp_gerado:
        console.print(Panel(whatsapp_gerado, title="📱 Versão WhatsApp", border_style="green"))
    else:
        console.print("\n" + "=" * 70 + "\n")
        console.print(Markdown(estudo_gerado))
        if whatsapp_gerado:
            console.print(Panel(whatsapp_gerado, title="📱 Versão para WhatsApp", border_style="green"))

    console.print(
        Panel(
            f"✅ [bold green]Estudo concluído com sucesso![/bold green]\n"
            f"💾 Arquivo salvo em: [bold cyan]{caminho_salvo}[/bold cyan]",
            border_style="green",
        )
    )

    if args.abrir:
        abrir_arquivo_no_sistema(caminho_salvo)

    if getattr(args, "web", False):
        try:
            exportar_estudo_para_web_data(caminho_salvo)
        except Exception:
            pass
        abrir_web_no_navegador()


def criar_parser() -> argparse.ArgumentParser:
    """Cria e configura o parser de argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        prog="versiculo-do-dia",
        description="Coletor automatizado do Versículo do Dia no YouVersion com análise teológica expositiva reformada via Gemini AI e publicação Web.",
    )
    parser.add_argument(
        "-v", "--versiculo",
        type=str,
        help="Especifica manualmente uma passagem bíblica (ex.: 'Romanos 8:1', 'Efésios 2:8-10') em vez de coletar no YouVersion.",
    )
    parser.add_argument(
        "-t", "--texto",
        type=str,
        help="Texto da passagem bíblica quando informada manualmente via --versiculo.",
    )
    parser.add_argument(
        "--versao",
        type=str,
        choices=["nvi", "ara", "naa", "nvt", "arc"],
        default=None,
        help="Versão da Bíblia a coletar no YouVersion (padrão: nvi).",
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Força uma nova coleta e geração do estudo, mesmo que já exista um estudo gerado hoje.",
    )
    parser.add_argument(
        "-w", "--whatsapp",
        action="store_true",
        help="Exibe prioritariamente a versão sintetizada para WhatsApp no terminal.",
    )
    parser.add_argument(
        "--historico",
        action="store_true",
        help="Lista todos os estudos bíblicos já gerados e armazenados localmente.",
    )
    parser.add_argument(
        "--abrir",
        action="store_true",
        help="Abre o arquivo Markdown gerado no aplicativo padrão do sistema após concluir.",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Abre o estudo bíblico na interface web local interativa no navegador padrão.",
    )
    parser.add_argument(
        "-m", "--modelo",
        type=str,
        default=None,
        help=f"Modelo Gemini a utilizar (padrão: {GEMINI_MODEL}).",
    )
    return parser


def main() -> None:
    """Ponto de entrada do CLI."""
    parser = criar_parser()
    args = parser.parse_args()
    executar_fluxo(args)


if __name__ == "__main__":
    main()
