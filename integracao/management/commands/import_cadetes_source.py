from django.core.management.base import BaseCommand, CommandError
from django.db import connections, transaction
from django.db.utils import OperationalError
from core.models import Cadete
import logging

logger = logging.getLogger(__name__)


def split_qualified(name: str):
    if "." in name:
        schema, table = name.split(".", 1)
    else:
        schema, table = "public", name
    return schema.strip('"'), table.strip('"')


def get_columns(cursor, schema, table):
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema=%s AND table_name=%s
        ORDER BY ordinal_position
        """,
        [schema, table],
    )
    return [r[0] for r in cursor.fetchall()]


def pick(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    return None


class Command(BaseCommand):
    help = "Importa cadetes do banco PostgreSQL externo (source) a partir de pessoa.cadastro_de_cadetes."

    def add_arguments(self, parser):
        parser.add_argument("--origem", default="pessoa.cadastro_de_cadetes", help="schema.tabela (default: pessoa.cadastro_de_cadetes)")
        parser.add_argument("--limite", type=int, default=0)

    def handle(self, *args, **opts):
        origem = opts["origem"]
        limite = opts["limite"]
        schema, table = split_qualified(origem)

        try:
            conn = connections["source"]
            with conn.cursor() as cursor:
                cols = get_columns(cursor, schema, table)
                if not cols:
                    raise CommandError(f"Tabela '{schema}.{table}' não encontrada no banco source.")

                col_numero = pick(cols, ["numero", "nr", "matricula", "id_cadete", "cadete_numero"])
                col_nome = pick(cols, ["nome", "nome_completo", "cadete_nome"])
                col_nome_guerra = pick(cols, ["nome_guerra", "nome_de_guerra", "guerra"])
                col_curso = pick(cols, ["curso", "nome_curso"])
                col_ano = pick(cols, ["ano", "ano_curso"])
                col_subunidade = pick(cols, ["subunidade", "companhia", "cia"])
                col_pelotao = pick(cols, ["pelotao", "plt"])
                col_cmt_curso = pick(cols, ["cmt_curso", "comandante_curso"])
                col_cmt_sub = pick(cols, ["cmt_subunidade", "comandante_subunidade"])
                col_cmt_pel = pick(cols, ["cmt_pelotao", "comandante_pelotao"])

                if not col_numero:
                    raise CommandError(
                        "Não encontrei uma coluna de número/matrícula no cadastro_de_cadetes. "
                        "Padronize a coluna (ex.: numero) ou crie uma view com alias."
                    )

                selected = [c for c in [col_numero, col_nome, col_nome_guerra, col_curso, col_ano, col_subunidade, col_pelotao, col_cmt_curso, col_cmt_sub, col_cmt_pel] if c]
                sel_sql = ", ".join([f'"{c}"' for c in selected])
                sql = f'SELECT {sel_sql} FROM "{schema}"."{table}"'
                if limite and limite > 0:
                    sql += f" LIMIT {limite}"

                cursor.execute(sql)
                rows = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]

        except OperationalError as e:
            raise CommandError("Não consegui conectar ao banco 'source'. Configure SOURCE_DB_* no .env.") from e

        imported = 0
        erros = 0
        skipped = 0
        
        for row_idx, row in enumerate(rows):
            try:
                data = dict(zip(colnames, row))
                numero = data.get(col_numero)
                
                if numero is None:
                    skipped += 1
                    continue
                
                # Converte para int com tratamento de erro
                try:
                    numero = int(numero)
                except (ValueError, TypeError):
                    logger.warning(f"Número inválido na linha {row_idx + 1}: {numero}")
                    erros += 1
                    continue

                defaults = {
                    "nome": data.get(col_nome) or f"Cadete {numero}",
                    "nome_de_guerra": data.get(col_nome_guerra),
                    "curso": data.get(col_curso),
                    "ano": data.get(col_ano),
                    "subunidade": data.get(col_subunidade),
                    "pelotao": data.get(col_pelotao),
                    "cmt_curso": data.get(col_cmt_curso),
                    "cmt_subunidade": data.get(col_cmt_sub),
                    "cmt_pelotao": data.get(col_cmt_pel),
                }

                # Usa transaction para garantir atomicidade
                with transaction.atomic():
                    Cadete.objects.update_or_create(numero=numero, defaults=defaults)
                imported += 1
            except Exception as e:
                erros += 1
                logger.error(f"Erro ao importar cadete linha {row_idx + 1}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Cadetes: {imported} importados/atualizados, {erros} erros, {skipped} pulados"))