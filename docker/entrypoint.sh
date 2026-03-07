#!/bin/bash
set -e

echo "[*] Aguardando banco de dados..."
python docker/wait_for_db.py
echo "[✓] Banco de dados pronto!"

echo "[*] Executando migrações..."
python manage.py migrate --noinput
echo "[✓] Migrações concluídas!"

echo "[*] Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear 2>/dev/null || echo "[!] Aviso: collectstatic teve problemas"
echo "[✓] Arquivos estáticos coletados!"

# Import automático opcional do banco externo
if [ -n "$AUTO_IMPORT_CADETES_SOURCE" ]; then
  echo "[*] Importando cadetes do banco externo..."
  ORIGEM=${SOURCE_CADETES_ORIGEM:-pessoa.cadastro_de_cadetes}
  python manage.py import_cadetes_source --origem "$ORIGEM" || echo "[!] Aviso: import_cadetes_source falhou"
fi

echo "[✓] Iniciando aplicação Django!"
exec "$@"