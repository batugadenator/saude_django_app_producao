import json
from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.utils import OperationalError
from integracao.models import UsuarioImportado

COMMON_COLS = ["id", "username", "email", "nome", "name", "first_name", "last_name", "ativo", "is_active"]


def get_columns(cursor, table_schema, table_name):
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema=%s AND table_name=%s
        ORDER BY ordinal_position
        """,
        [table_schema, table_name],
    )
    return [r[0] for r in cursor.fetchall()]


def split_qualified(name: str):
    if "." in name:
        schema, table = name.split(".", 1)
    else:
        schema, table = "public", name
    return schema, table


class Command(BaseCommand):
    help = "Importa registros de uma tabela de usuários do banco PostgreSQL 'source' para o banco 'default'."

    def add_arguments(self, parser):
        parser.add_argument("--tabela", default="public.usuario")
        parser.add_argument("--limite", type=int, default=0)

    def handle(self, *args, **opts):
        tabela = opts["tabela"]
        limite = opts["limite"]
        schema, table = split_qualified(tabela)

        try:
            conn = connections["source"]
            with conn.cursor() as cursor:
                cols = get_columns(cursor, schema, table)
                if not cols:
                    raise CommandError(f"Tabela '{schema}.{table}' não encontrada no banco source.")

                selected = [c for c in COMMON_COLS if c in cols]
                if "id" not in selected and "pk" in cols:
                    selected.insert(0, "pk")

                sel_sql = ", ".join([f"\"{c}\"" for c in (selected or cols)])
                sql = f'SELECT {sel_sql} FROM "{schema}"."{table}"'
                if limite and limite > 0:
                    sql += f" LIMIT {limite}"

                cursor.execute(sql)
                rows = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]

        except OperationalError as e:
            raise CommandError("Não consegui conectar ao banco 'source'. Configure SOURCE_DB_* no .env.") from e

        imported = 0
        for row in rows:
            data = dict(zip(colnames, row))
            external_id = data.get("id") or data.get("pk")
            if external_id is None:
                external_id = abs(hash(json.dumps(data, default=str)))

            username = data.get("username")
            email = data.get("email")
            nome = data.get("nome") or data.get("name")
            if not nome:
                fn = data.get("first_name")
                ln = data.get("last_name")
                nome = " ".join([x for x in [fn, ln] if x]) or None

            ativo = data.get("ativo")
            if ativo is None:
                ativo = data.get("is_active")
            ativo = bool(ativo) if ativo is not None else True

            UsuarioImportado.objects.update_or_create(
                external_id=external_id,
                defaults={"username": username, "email": email, "nome": nome, "ativo": ativo, "raw": data},
            )
            imported += 1

        self.stdout.write(self.style.SUCCESS(f"Usuários importados/atualizados: {imported}"))