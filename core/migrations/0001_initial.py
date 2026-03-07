from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cadete",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero", models.IntegerField(unique=True)),
                ("nome", models.CharField(max_length=255)),
                ("nome_de_guerra", models.CharField(blank=True, max_length=255, null=True)),
                ("curso", models.CharField(blank=True, max_length=100, null=True)),
                ("ano", models.IntegerField(blank=True, null=True)),
                ("subunidade", models.CharField(blank=True, max_length=100, null=True)),
                ("pelotao", models.CharField(blank=True, max_length=50, null=True)),
                ("cmt_curso", models.CharField(blank=True, max_length=100, null=True)),
                ("cmt_subunidade", models.CharField(blank=True, max_length=100, null=True)),
                ("cmt_pelotao", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Profissional",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo", models.CharField(choices=[("medico", "Médico"), ("fisioterapeuta", "Fisioterapeuta"), ("educador_fisico", "Educador Físico"), ("nutricionista", "Nutricionista"), ("psicopedagogo", "Psicopedagogo"), ("sred", "S-RED"), ("enfermagem", "Enfermagem/PM CC"), ("instrutor", "Instrutor"), ("estatistico", "Estatístico"), ("ti", "Profissional de TI")], max_length=50)),
                ("identificador", models.CharField(max_length=120)),
                ("nome", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={"unique_together": {("tipo", "identificador")}},
        ),
        migrations.CreateModel(
            name="Atendimento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("data", models.DateField()),
                ("hora", models.TimeField(blank=True, null=True)),
                ("atendimento", models.CharField(choices=[("inicial", "Inicial"), ("retorno", "Retorno")], max_length=20)),
                ("profissional_tipo", models.CharField(blank=True, max_length=80, null=True)),
                ("profissional_nome", models.CharField(blank=True, max_length=255, null=True)),
                ("lesao_tipo", models.CharField(blank=True, max_length=60, null=True)),
                ("parte_do_corpo", models.CharField(blank=True, max_length=80, null=True)),
                ("lateralidade", models.CharField(blank=True, max_length=20, null=True)),
                ("parte_lesionada", models.CharField(blank=True, max_length=120, null=True)),
                ("local_da_lesao", models.CharField(blank=True, max_length=120, null=True)),
                ("origem_da_lesao", models.CharField(blank=True, max_length=120, null=True)),
                ("sred", models.CharField(blank=True, max_length=120, null=True)),
                ("causa", models.CharField(blank=True, max_length=120, null=True)),
                ("atividade", models.CharField(blank=True, max_length=120, null=True)),
                ("tfm_taf", models.CharField(blank=True, max_length=120, null=True)),
                ("modalidade", models.CharField(blank=True, max_length=120, null=True)),
                ("tratamento", models.CharField(blank=True, max_length=120, null=True)),
                ("medicamentoso", models.CharField(blank=True, max_length=10, null=True)),
                ("fisioterapia", models.BooleanField(default=False)),
                ("sef", models.BooleanField(default=False)),
                ("nutricionista", models.BooleanField(default=False)),
                ("psicopedagogica", models.BooleanField(default=False)),
                ("rx", models.BooleanField(default=False)),
                ("usg", models.BooleanField(default=False)),
                ("tc", models.BooleanField(default=False)),
                ("rm", models.BooleanField(default=False)),
                ("dexa", models.BooleanField(default=False)),
                ("sangue", models.BooleanField(default=False)),
                ("dispensa", models.BooleanField(default=False)),
                ("vcl", models.BooleanField(default=False)),
                ("alta", models.BooleanField(default=False)),
                ("risco_cirurgico", models.BooleanField(default=False)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("cadete", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="atendimentos", to="core.cadete")),
            ],
        ),
    ]