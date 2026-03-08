# 📖 Guia de Instalação e Deployment

Este documento contém guias completos para instalação local e deployment em servidor.

---

## 📋 Índice

1. [Instalação Local (Desenvolvimento)](#instalação-local-desenvolvimento)
2. [Deployment em Debian Server](#deployment-em-debian-server)

---

## 🔧 Instalação Local (Desenvolvimento)

### Pré-requisitos
- Python 3.12+
- Git
- SQLite (já incluído no Python)

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/saude-django-app.git
cd saude-django-app
```

### Passo 2: Criar Virtual Environment
```bash
python3.12 -m venv venv

# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

### Passo 3: Instalar Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4: Configurar Variáveis de Ambiente
```bash
cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=dev-secret-key-insecure-only-for-local-dev
ALLOWED_HOSTS=localhost,127.0.0.1,*
DJANGO_SETTINGS_MODULE=saude_project.settings.dev
EOF
```

### Passo 5: Configurar SQLite (settings/dev.py)
Abra `saude_project/settings/dev.py` e adicione após os imports:

```python
from pathlib import Path

# Override para desenvolvimento local com SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

### Passo 6: Executar Setup do Banco de Dados
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123
```

### Passo 7: Importar Dados (Opcional)
```bash
python manage.py import_planilha --arquivo projeto_saude.xlsm
```

### Passo 8: Executar Servidor
```bash
python manage.py runserver
```

Acesse: **http://localhost:8000/admin**

---

## 🚀 Deployment em Debian Server

### Pré-requisitos
- VM Debian 11+ com acesso SSH
- Domínio configurado (opcional para HTTPS)

### Passo 1: Conectar ao Servidor
```bash
ssh seu-usuario@seu-ip-servidor
sudo su  # ou use 'sudo' após cada comando
```

### Passo 2: Atualizar Sistema
```bash
apt update && apt upgrade -y
```

### Passo 3: Instalar Dependências
```bash
apt install -y python3.12 python3.12-venv python3-pip \
    git postgresql postgresql-contrib nginx curl
```

### Passo 4: Clonar Repositório
```bash
cd /var/www
git clone https://github.com/seu-usuario/saude-django-app.git
cd saude-django-app
```

### Passo 5: Criar Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 6: Configurar Variáveis de Ambiente
```bash
sudo tee /var/www/saude-django-app/.env > /dev/null << 'EOF'
DEBUG=False
SECRET_KEY=sua-secret-key-muito-segura-e-aleatoria-aqui
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com,seu-ip-servidor
DJANGO_SETTINGS_MODULE=saude_project.settings.prod
POSTGRES_DB=saude
POSTGRES_USER=saude
POSTGRES_PASSWORD=sua-senha-super-segura-aqui
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
EOF
```

### Passo 7: Configurar PostgreSQL
```bash
sudo -u postgres psql << 'EOF'
CREATE DATABASE saude;
CREATE USER saude WITH PASSWORD 'sua-senha-super-segura-aqui';
ALTER ROLE saude SET client_encoding TO 'utf8';
ALTER ROLE saude SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE saude TO saude;
\q
EOF
```

### Passo 8: Aplicar Migrations
```bash
cd /var/www/saude-django-app
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Passo 9: Testar com Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 saude_project.wsgi:application
# Pare com: Ctrl+C
```

### Passo 10: Configurar Gunicorn como Serviço
```bash
sudo tee /etc/systemd/system/gunicorn.service > /dev/null << 'EOF'
[Unit]
Description=Gunicorn WSGI HTTP Server for Saude App
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/saude-django-app
ExecStart=/var/www/saude-django-app/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/run/gunicorn.sock \
    saude_project.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Passo 11: Configurar Nginx (Reverse Proxy)
```bash
sudo tee /etc/nginx/sites-available/saude > /dev/null << 'EOF'
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/saude-django-app/staticfiles/;
    }

    location /media/ {
        alias /var/www/saude-django-app/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/run/gunicorn.sock;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/saude /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default 2>/dev/null || true
sudo nginx -t
sudo systemctl restart nginx
```

### Passo 12: Configurar HTTPS (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação automática:
sudo systemctl enable certbot.timer
```

### Passo 13: Verificar Status
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status postgresql
```

### Passo 14: Visualizar Logs
```bash
# Nginx
sudo tail -f /var/log/nginx/error.log

# Gunicorn
sudo journalctl -u gunicorn -f

# Django
sudo tail -f /var/www/saude-django-app/logs/django.log  # se configurado
```

---

## 🔄 Comandos Úteis para Deployment

### Atualizar Código do GitHub
```bash
cd /var/www/saude-django-app
source venv/bin/activate
git pull origin master
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Backup do Banco de Dados
```bash
sudo -u postgres pg_dump -U saude saude > /backups/saude_backup_$(date +%Y%m%d).sql
```

### Restore do Banco de Dados
```bash
sudo -u postgres psql -U saude saude < /backups/saude_backup_2026-03-07.sql
```

### Verificar Erro do Gunicorn
```bash
sudo systemctl restart gunicorn
sudo journalctl -u gunicorn -n 50
```

### Reiniciar Todos os Serviços
```bash
sudo systemctl restart gunicorn nginx postgresql
```

---

## 📊 Comparação: Local vs Produção

| Aspecto | Local | Produção |
|---------|-------|----------|
| **Banco de Dados** | SQLite | PostgreSQL |
| **Servidor Web** | Django dev | Nginx + Gunicorn |
| **HTTPS** | Não | Sim (Let's Encrypt) |
| **Debug** | True | False |
| **Workers** | 1 | 3+ |
| **Domínio** | localhost | seu-dominio.com |
| **Performance** | Desenvolvimento | Otimizado |

---

## ⚠️ Checklist de Segurança para Produção

- [ ] `DEBUG=False` no .env
- [ ] `SECRET_KEY` alterado e seguro
- [ ] PostgreSQL com senha forte
- [ ] HTTPS ativado
- [ ] Firewall configurado
- [ ] Backups automáticos configurados
- [ ] Logs monitorizados
- [ ] Permissões de arquivo corretas
- [ ] `ALLOWED_HOSTS` configurado corretamente

---

## 🆘 Troubleshooting

### Erro: "No module named 'django'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "Connection refused (PostgreSQL)"
```bash
sudo systemctl status postgresql
sudo systemctl restart postgresql
```

### Erro: "Permission denied" (arquivos estáticos)
```bash
sudo chown -R www-data:www-data /var/www/saude-django-app
sudo chmod -R 755 /var/www/saude-django-app
```

### Porta 8000 já em uso
```bash
# Encontrar processo
lsof -i :8000

# Matar processo
kill -9 <PID>
```

---

## 📞 Contato e Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação oficial: https://docs.djangoproject.com
- Verifique os logs: `journalctl -u gunicorn -f`

---

**Última atualização:** 07/03/2026
