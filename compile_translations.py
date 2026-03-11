#!/usr/bin/env python
"""
Script para gerar e compilar mensagens de tradução para português-BR.
Execute este script depois de modificar arquivos de tradução.
"""

import os
import sys
import subprocess
from pathlib import Path

# Adiciona o diretório do projeto ao path
project_root = Path(__file__).parent
os.chdir(project_root)

print("=" * 60)
print("Gerando e compilando mensagens de tradução para pt-BR")
print("=" * 60)

# 1. Gerar mensagens
print("\n[1/2] Gerando mensagens de tradução...")
result = subprocess.run(
    [sys.executable, "manage.py", "makemessages", "-l", "pt_BR", "--ignore=venv*", "--ignore=.venv*"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✓ Mensagens geradas com sucesso")
    if result.stdout:
        print(result.stdout)
else:
    print("✗ Erro ao gerar mensagens:")
    print(result.stderr)
    sys.exit(1)

# 2. Compilar mensagens
print("\n[2/2] Compilando mensagens de tradução...")
result = subprocess.run(
    [sys.executable, "manage.py", "compilemessages", "-l", "pt_BR"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✓ Mensagens compiladas com sucesso")
    if result.stdout:
        print(result.stdout)
else:
    print("✗ Erro ao compilar mensagens:")
    print(result.stderr)
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ Tradução concluída! Restart o servidor Django.")
print("=" * 60)
