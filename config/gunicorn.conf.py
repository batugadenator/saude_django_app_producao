import multiprocessing
import os

# Server socket
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")

# Workers
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
threads = int(os.environ.get("GUNICORN_THREADS", 2))
worker_connections = 1000

# Timeouts
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 60))
graceful_timeout = 30

# Keep-alive
keepalive = 2

# Logging
accesslog = os.environ.get("GUNICORN_ACCESS_LOG", "-")  # stdout
errorlog = os.environ.get("GUNICORN_ERROR_LOG", "-")   # stderr
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (configure via environment se necessário)
# keyfile = os.environ.get("GUNICORN_KEYFILE")
# certfile = os.environ.get("GUNICORN_CERTFILE")
# ssl_version = ssl.PROTOCOL_TLSv1_2

# Process naming
proc_name = "saude_django_app"
