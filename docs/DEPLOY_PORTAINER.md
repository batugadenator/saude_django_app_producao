# Deploy via Portainer (Docker Stack)

## Pré-requisitos no servidor remoto

- Docker instalado e em execução
- Portainer instalado e acessível
- Git instalado (para clonar o repositório)

---

## Opção A — Deploy via Repositório Git (recomendado)

O Portainer clona o repositório diretamente do Git e faz o build automaticamente.

### 1. Configurar o arquivo `.env` no servidor

SSH no servidor e crie o arquivo de ambiente:

```bash
ssh usuario@ip-do-servidor
mkdir -p /opt/cadete-funcional
cd /opt/cadete-funcional

# Clonar o repositório
git clone <url-do-repositorio> .

# Copiar e editar o .env de produção
cp config/.env.example config/.env
nano config/.env
```

**Valores obrigatórios no `config/.env`:**

```env
DJANGO_SETTINGS_MODULE=cadete_funcional.settings.prod
DEBUG=False

# Gere com: python -c "import secrets; print(secrets.token_urlsafe(50))"
SECRET_KEY=pC6sXHDTOhb7mHj5Kb9YMou_wv_3q6kuxjR9LR1eWUdR8S7AKByTZpxbhqGETrXQhm4

# IP ou domínio do servidor (separados por vírgula)
ALLOWED_HOSTS=192.168.3.60

# Banco de dados
POSTGRES_DB=saude
POSTGRES_USER=saude
POSTGRES_PASSWORD=highlighter
POSTGRES_HOST=db
POSTGRES_PORT=5432

# SSL (False sem HTTPS configurado)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

NGINX_PORT=80
LOG_LEVEL=INFO
USE_X_FORWARDED_HOST=True
```

### 2. Deploy no Portainer

1. Acesse o Portainer: `http://ip-do-portainer:9000`
2. Navegue para **Stacks → Add Stack**
3. Selecione **"Repository"**
4. Preencha:
   - **Repository URL**: URL do seu repositório Git
   - **Reference**: `main` (ou sua branch de produção)
   - **Compose path**: `docker-compose.yml`
5. Em **Environment variables**, adicione variáveis sensíveis (opcional — o `.env` já está no servidor)
6. Clique em **Deploy the stack**

---

## Opção B — Upload direto do `docker-compose.yml` (sem Git)

Use quando o código já está no servidor ou quando não tem acesso Git direto.

### 1. Enviar os arquivos para o servidor

No Windows (PowerShell):

```powershell
# Compactar o projeto
Compress-Archive -Path "d:\BigData\Projetos\saude_django_app_producao\*" `
    -DestinationPath "cadete-funcional.zip" `
    -Force

# Enviar via SCP
scp cadete-funcional.zip usuario@ip-do-servidor:/opt/cadete-funcional.zip

# Descompactar no servidor (via SSH)
ssh usuario@ip-do-servidor "cd /opt && unzip cadete-funcional.zip -d cadete-funcional && cd cadete-funcional && cp config/.env.example config/.env"
```

### 2. Editar o `.env` no servidor

```bash
ssh usuario@ip-do-servidor
nano /opt/cadete-funcional/config/.env
# (preencher os valores conforme seção anterior)
```

### 3. Deploy no Portainer

1. Acesse **Stacks → Add Stack**
2. Selecione **"Upload"** ou **"Web editor"**
3. Cole o conteúdo do `docker-compose.yml` ou faça upload
4. Adjust **Working directory** para `/opt/cadete-funcional`
5. Clique em **Deploy the stack**

---

## Estrutura de containers criados

```
┌─────────────────────────────────────────────────────┐
│                    Servidor Remoto                   │
│                                                      │
│  ┌──────────┐    ┌─────────────┐    ┌────────────┐  │
│  │  nginx   │───►│  web (8000) │───►│ db (5432)  │  │
│  │ port:80  │    │  Gunicorn   │    │ PostgreSQL  │  │
│  └──────────┘    └─────────────┘    └────────────┘  │
│       │                 │                            │
│  [static_volume]  [static_volume]  [pgdata_volume]  │
└─────────────────────────────────────────────────────┘
```

---

## Comandos pós-deploy (executar via Portainer ou SSH)

### Criar superusuário admin

No Portainer, vá em **Containers → web → Console (Exec)**:

```bash
python manage.py createsuperuser
```

Ou via SSH:

```bash
docker exec -it <nome-do-container-web> python manage.py createsuperuser
```

### Verificar saúde da aplicação

```bash
curl http://ip-do-servidor/healthz/
# Resposta esperada: {"status": "ok", "database": true}
```

### Ver logs

```bash
docker logs <nome-do-container-web> -f
docker logs <nome-do-container-nginx> -f
```

---

## Atualizações futuras

```bash
# No servidor, na pasta do projeto:
git pull origin main

# No Portainer:
# Stacks → <nome-da-stack> → Update the stack → Pull and redeploy
```

---

## Portas expostas

| Serviço | Porta interna | Porta no host |
|---------|--------------|---------------|
| nginx   | 80           | `${NGINX_PORT:-80}` |
| db      | 5432         | **não exposta** (interna) |
| web     | 8000         | **não exposta** (interna) |

> **Segurança**: apenas o nginx é exposto ao host. PostgreSQL e Gunicorn ficam na rede interna `app_network`.
