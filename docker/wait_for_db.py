import os
import time
import psycopg

host = os.getenv("POSTGRES_HOST", "db")
port = int(os.getenv("POSTGRES_PORT", "5432"))
db = os.getenv("POSTGRES_DB", "saude")
user = os.getenv("POSTGRES_USER", "saude")
pw = os.getenv("POSTGRES_PASSWORD", "saude")

for _ in range(60):
    try:
        with psycopg.connect(host=host, port=port, dbname=db, user=user, password=pw) as conn:
            with conn.cursor() as cur:
                cur.execute("select 1")
                cur.fetchone()
        break
    except psycopg.OperationalError:
        time.sleep(1)
else:
    raise SystemExit("Banco não ficou disponível.")