FROM python:3.12-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cria usuário não-root
RUN useradd -m -u 1000 appuser

# Define diretório de trabalho
WORKDIR /app

# Copia requirements e instala dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY . /app/

# Define permissões corretas
RUN chmod +x /app/docker/entrypoint.sh && \
    chown -R appuser:appuser /app

# Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Muda para usuário não-root
USER appuser

# Expõe porta
EXPOSE 8000

# Define módulo de settings
ENV DJANGO_SETTINGS_MODULE=saude_project.settings.prod

# Entrypoint
ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "saude_project.wsgi:application", "-c", "gunicorn.conf.py"]