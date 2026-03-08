# Cadete Funcional — Django + PostgreSQL + Docker (produção)

Este pacote entrega uma base pronta para produção, com:
- Settings separados (`dev` e `prod`)
- Gunicorn, usuário não-root, healthcheck (`/healthz/`)
- Importação da planilha `projeto_saude.xlsm`
- Importação de cadetes a partir de banco PostgreSQL externo em `pessoa.cadastro_de_cadetes`

## Subir em Docker

```bash
cp .env.example .env
docker compose up --build