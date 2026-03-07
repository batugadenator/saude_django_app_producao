from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UsuarioImportado",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("external_id", models.BigIntegerField(db_index=True)),
                ("username", models.CharField(blank=True, max_length=150, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("nome", models.CharField(blank=True, max_length=255, null=True)),
                ("ativo", models.BooleanField(default=True)),
                ("raw", models.JSONField(default=dict)),
                ("imported_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"unique_together": {("external_id",)}},
        ),
    ]