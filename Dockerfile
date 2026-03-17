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

# Ajustar permissões (collectstatic roda no entrypoint com ambiente completo)
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Health check: envia Host header correto para evitar DisallowedHost
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f -H "Host: localhost" http://127.0.0.1:8000/healthz/ || exit 1

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "cadete_funcional.wsgi:application", "-c", "config/gunicorn.conf.py"]
