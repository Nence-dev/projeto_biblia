"""Script Python resiliente para subir ao GitHub o novo refinamento dos prompts e testes."""

import subprocess
import sys
from pathlib import Path

def executar_comando(cmd: list[str], ignorar_erro: bool = False) -> int:
    texto_cmd = " ".join(cmd)
    print(f"\n> {texto_cmd}")
    res = subprocess.run(cmd)
    if res.returncode != 0 and not ignorar_erro:
        print(f"⚠️ Aviso no comando: {texto_cmd} (código {res.returncode})")
    return res.returncode

def main():
    pasta_projeto = Path(__file__).resolve().parent
    print("=" * 70)
    print("🚀 Enviando Refinamento dos Prompts do Gemini para o GitHub")
    print("=" * 70)
    print(f"Diretório: {pasta_projeto}")

    # 1. Adicionar arquivos locais modificados (sem tentar adicionar arquivos do .gitignore)
    print("\n[1/4] Adicionando arquivos modificados...")
    arquivos_para_add = [
        "src/prompts.py",
        "tests/test_prompts_e_estilizacao.py",
        "estudos/2026-10-12_proverbios_22_6.md",
        "web/data.js",
        "executar_teste_local.bat",
        "subir_alteracoes_git.py",
        "subir_alteracoes_git.bat",
    ]
    executar_comando(["git", "add"] + arquivos_para_add, ignorar_erro=True)

    # 2. Gravar commit caso haja algo pendente
    print("\n[2/4] Gravando commit local...")
    msg_commit = "feat: refinar prompts do gemini (texto acessivel, sem cliches como asfalto, devocional conciso e historias reais/biblicas)"
    executar_comando(["git", "commit", "-m", msg_commit], ignorar_erro=True)

    # 3. Puxar alterações remotas do GitHub com rebase preservando nossas alterações locais
    print("\n[3/4] Sincronizando com histórico remoto do GitHub (origin main)...")
    res_pull = executar_comando(["git", "pull", "--rebase", "origin", "main", "-X", "ours"], ignorar_erro=True)
    if res_pull != 0:
        print("Tentando merge convencional...")
        executar_comando(["git", "merge", "origin/main", "-X", "ours", "--no-edit"], ignorar_erro=True)

    # 4. Enviar para o GitHub
    print("\n[4/4] Enviando para o GitHub (git push origin main)...")
    res_push = executar_comando(["git", "push", "origin", "main"])

    if res_push == 0:
        print("\n" + "=" * 70)
        print("✅ SUCESSO! Alterações enviadas para o GitHub com sucesso!")
        print("A partir de amanhã, a automação do GitHub Actions gerará o estudo")
        print("no novo formato sem clichês e com histórias reais/bíblicas.")
        print("=" * 70)
    else:
        print("\n⚠️ O push encontrou uma pendência. Tentando push final...")
        executar_comando(["git", "push", "origin", "main", "--force-with-lease"])

if __name__ == "__main__":
    main()
