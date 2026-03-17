FROM python:3.12-slim

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Usuário não-root para segurança
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Instalar dependências Python primeiro (cache de camadas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório de arquivos estáticos e configurar permissões
RUN mkdir -p /app/staticfiles /app/media && \
    chmod +x /app/docker/entrypoint.sh

# Coletar arquivos estáticos em tempo de build (SECRET_KEY temporária)
ARG BUILD_SECRET_KEY=build-time-only-not-used-in-prod
ENV DJANGO_SETTINGS_MODULE=cadete_funcional.settings.prod \
    SECRET_KEY=${BUILD_SECRET_KEY} \
    DEBUG=False \
    ALLOWED_HOSTS=localhost \
    POSTGRES_HOST=localhost \
    POSTGRES_DB=saude \
    POSTGRES_USER=saude \
    POSTGRES_PASSWORD=saude \
    SECURE_SSL_REDIRECT=False

RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Ajustar permissões após collectstatic
RUN chown -R appuser:appuser /app

# Remover SECRET_KEY temporária do ambiente da imagem final
ENV SECRET_KEY=""

USER appuser

EXPOSE 8000

# Health check: envia Host header correto para evitar DisallowedHost
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f -H "Host: localhost" http://127.0.0.1:8000/healthz/ || exit 1

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "cadete_funcional.wsgi:application", "-c", "config/gunicorn.conf.py"]
