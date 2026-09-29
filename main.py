#!/usr/bin/env python3
"""Ponto de entrada executável do projeto Versículo do Dia & Especialista Teológico Expositivo."""

import sys
from pathlib import Path

# Adiciona a raiz do projeto ao sys.path para importações absolutas limpas
RAIZ = Path(__file__).resolve().parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.cli import main

if __name__ == "__main__":
    main()
