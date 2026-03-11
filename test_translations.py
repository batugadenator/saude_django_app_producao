#!/usr/bin/env python
"""
Script de teste para verificar se as traduções para português-BR estão funcionando.
Execute dentro do Django shell ou como um comando management customizado.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadete_funcional.settings.base')
sys.path.insert(0, str(Path(__file__).parent))

django.setup()

from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType

print("\n" + "=" * 70)
print("🌐 TESTE DE TRADUÇÃO PARA PORTUGUÊS-BR")
print("=" * 70)

# 1. Verificar configurações
print("\n[1/3] Verificando configurações Django...")
print(f"  ✓ LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
print(f"  ✓ USE_I18N: {settings.USE_I18N}")
print(f"  ✓ LOCALE_PATHS: {settings.LOCALE_PATHS}")

# 2. Testar tradução de strings
print("\n[2/3] Testando tradução de strings...")
test_strings = {
    "Pode adicionar grupo": _("Can add group"),
    "Pode alterar grupo": _("Can change group"),
    "Pode deletar grupo": _("Can delete group"),
    "Pode visualizar grupo": _("Can view group"),
    "usuário": _("user"),
    "grupo": _("group"),
    "permissão": _("permission"),
}

all_translated = True
for pt_expected, en_original in test_strings.items():
    # Try to get from Django's translation
    translated = _(en_original)
    is_translated = translated != en_original
    status = "✓" if is_translated else "✗"
    
    if not is_translated:
        all_translated = False
    
    print(f"  {status} '{en_original}' → '{translated}'")

# 3. Verificar arquivo .mo
print("\n[3/3] Verificando arquivos de tradução...")
mo_file = Path(settings.BASE_DIR) / "locale" / "pt_BR" / "LC_MESSAGES" / "django.mo"
po_file = Path(settings.BASE_DIR) / "locale" / "pt_BR" / "LC_MESSAGES" / "django.po"

if po_file.exists():
    size = po_file.stat().st_size
    print(f"  ✓ Arquivo .po encontrado: {po_file}")
    print(f"    Tamanho: {size} bytes")
else:
    print(f"  ✗ Arquivo .po NÃO encontrado: {po_file}")

if mo_file.exists():
    size = mo_file.stat().st_size
    print(f"  ✓ Arquivo .mo encontrado: {mo_file}")
    print(f"    Tamanho: {size} bytes")
else:
    print(f"  ✗ Arquivo .mo NÃO encontrado: {mo_file}")
    print(f"    Você precisa executar: python compile_pt_br.py")

# 4. Teste com permissões reais
print("\n[4/4] Testando permissões do admin...")
try:
    # Pegar permissões de grupos
    group_perms = Permission.objects.filter(content_type__model='group')
    
    for perm in group_perms[:4]:  # Mostrar as 4 primeiras
        print(f"  ► {perm.codename}: {perm.name}")
    
    print(f"\n  Total de permissões: {Permission.objects.count()}")
except Exception as e:
    print(f"  ✗ Erro ao verificar permissões: {e}")

# Resumo final
print("\n" + "=" * 70)
if all_translated and mo_file.exists():
    print("✅ SUCESSO! As traduções estão funcionando corretamente.")
    print("\nPróximos passos:")
    print("1. Reinicie o servidor: python manage.py runserver")
    print("2. Visite: http://127.0.0.1:8000/admin/")
    print("3. Vá para: /admin/auth/group/add/")
    print("4. Verifique as permissões em português")
else:
    print("⚠️  AVISO: Há problemas com as traduções.")
    if not mo_file.exists():
        print("\n➤ Faltando arquivo .mo")
        print("  Execute: python compile_pt_br.py")
    if not all_translated:
        print("\n➤ Strings ainda em inglês")
        print("  Possíveis causas:")
        print("    - Django ainda não carregou as traduções")
        print("    - Arquivo .mo pode estar desatualizado")
        print("    - Cache do navegador pode estar interferindo")
print("=" * 70 + "\n")
