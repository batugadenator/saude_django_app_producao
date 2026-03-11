# Compilar Traduções para Português-BR

Para traduzir a interface de admin para português-BR, execute os seguintes comandos:

## 1. Ativar o ambiente virtual

```powershell
# PowerShell (Windows)
& .\.venv\Scripts\Activate.ps1

# Ou Command Prompt
.venv\Scripts\activate.bat
```

## 2. Gerar mensagens de tradução

```bash
python manage.py makemessages -l pt_BR
```

Este comando varre todos os arquivos Python e template procurando por strings de tradução e cria o arquivo `locale/pt_BR/LC_MESSAGES/django.po`.

## 3. Compilar mensagens

```bash
python manage.py compilemessages -l pt_BR
```

Este comando compila o arquivo `.po` em um arquivo `.mo` que o Django usa em produção.

## 4. Ou execute o script automático

Você pode executar o script Python que faz ambos os passos:

```bash
python compile_translations.py
```

## 5. Reiniciar o servidor

```bash
python manage.py runserver
```

Agora visite http://127.0.0.1:8000/admin/ e verá todas as permissões traduzidas para português-BR.

---

## 📝 Notas Importantes

- O arquivo `locale/pt_BR/LC_MESSAGES/django.po` já contém as traduções base
- Após compilar, os arquivos `.mo` são gerados automaticamente
- Se modificar as traduções no arquivo `.po`, execute novamente `compilemessages`
- O Django cacheará as traduções, pode precisar reiniciar o servidor para ver mudanças

---

## 🔍 Verificar Traduções

As traduções estarão visíveis em:
- Admin interface: /admin/
- Permissões: /admin/auth/group/
- Modelos: /admin/core/cadete/, etc.

Nomes de permissões como **"Can add group"** aparecerão como **"Pode adicionar grupo"**.
