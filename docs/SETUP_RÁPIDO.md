# ⚡ Setup Rápido - 3 Soluções

## ❌ Problema Atual
Docker está instalado mas **não está rodando**
```
unable to get image 'postgres:16': error during connect
```

---

## ✅ SOLUÇÃO 1: Iniciar Docker Desktop (5 mins)

### Windows 10/11:

1. **Abra o menu Iniciar** e procure por "Docker Desktop"
2. **Clique para abrir**
3. **Aguarde iniciar** (levará 20-30 segundos)
4. Você verá um ícone do Docker na bandeja do sistema (canto inferior direito)
5. **Espere até aparecer "Docker Desktop is running"**

Depois execute:
```powershell
cd d:\BigData\cadete_funcional\saude_django_app_producao
docker-compose up -d
Start-Sleep -Seconds 15
python manage.py makemigrations
python manage.py migrate
python manage.py import_planilha --arquivo projeto_saude.xlsm
python manage.py runserver
```

---

## ✅ SOLUÇÃO 2: SQLite - Sem Dependências (3 mins - RÁPIDO!)

### Passo 1: Criar arquivo .env
```powershell
cd d:\BigData\cadete_funcional\saude_django_app_producao

@"
DEBUG=True
SECRET_KEY=dev-secret-key-insecure-only-for-local-dev
ALLOWED_HOSTS=localhost,127.0.0.1,*
DJANGO_SETTINGS_MODULE=saude_project.settings.dev
"@ | Out-File .env -Encoding UTF8
```

### Passo 2: Editar settings dev para usar SQLite

Abra `saude_project/settings/dev.py` e substitua a seção DATABASES:

Encontre:
```python
from .base import *  # noqa

DEBUG = env("DEBUG", default=True)
```

Adicione ANTES da linha `DEBUG`:
```python
from pathlib import Path
```

Depois adicione DEPOIS de todos os imports:
```python
# Override para desenvolvimento local com SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

### Passo 3: Executar setup
```powershell
cd d:\BigData\cadete_funcional\saude_django_app_producao

# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Criar superuser (admin)
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123

# Testar importação
python manage.py import_planilha --arquivo projeto_saude.xlsm

# Rodar servidor
python manage.py runserver
```

Acesse: **http://localhost:8000/admin**

---

## ✅ SOLUÇÃO 3: PostgreSQL Local (10 mins)

### Passo 1: Verificar se PostgreSQL está instalado
```powershell
Get-Service postgresql* -ErrorAction SilentlyContinue
```

Se não encontrou nada, [baixe PostgreSQL 16](https://www.postgresql.org/download/windows/)

### Passo 2: Iniciar PostgreSQL
```powershell
Start-Service postgresql-x64-16
```

### Passo 3: Criar banco de dados
```powershell
# Substitua a senha conforme necessário
psql -U postgres -c "CREATE DATABASE saude;"
psql -U postgres -c "CREATE USER saude WITH PASSWORD 'saude';"
psql -U postgres -c "ALTER ROLE saude SET client_encoding TO 'utf8';"
psql -U postgres -c "ALTER ROLE saude SET default_transaction_isolation TO 'read committed';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE saude TO saude;"
```

### Passo 4: Configurar .env
```powershell
copy .env.example .env
```

Edite `.env` e configure:
```
DEBUG=True
SECRET_KEY=dev-secret-key-change-me
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=saude
POSTGRES_USER=saude
POSTGRES_PASSWORD=saude
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Passo 5: Rodar setup
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py import_planilha --arquivo projeto_saude.xlsm
python manage.py runserver
```

---

## 🎯 Recomendação: Use SOLUÇÃO 2 (SQLite)

**SOLUÇÃO 2 é mais rápida para testar tudo agora:**
- ✅ Sem dependências externas
- ✅ Pronta em 3 minutos
- ✅ Perfeito para desenvolvimento
- ✅ Nenhuma configuração complexa

**Para Produção:** Use SOLUÇÃO 1 (Docker) com PostgreSQL

---

## 📋 Qual escolher?

| Solução | Tempo | Complexidade | Recomendado Para |
|---------|-------|--------------|------------------|
| **1 - Docker** | 10 min | Média | Produção/Equipe |
| **2 - SQLite** | 3 min | Baixa | **✅ Testar agora** |
| **3 - PostgreSQL** | 10 min | Alta | Local profissional |

**Comece com SOLUÇÃO 2!** 🚀
