# Generated migration to add audit fields (created_at, updated_at, created_by)

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_alter_atendimento_options_alter_cadete_options_and_more'),
    ]

    operations = [
        # Adicionar campos ao modelo Cadete
        migrations.AddField(
            model_name='cadete',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name='cadete',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='cadete',
            name='criado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cadetes_criados', to=settings.AUTH_USER_MODEL),
        ),
        # Adicionar campos ao modelo Profissional
        migrations.AddField(
            model_name='profissional',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name='profissional',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='profissional',
            name='criado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profissionais_criados', to=settings.AUTH_USER_MODEL),
        ),
        # Adicionar campos ao modelo Atendimento
        migrations.AddField(
            model_name='atendimento',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name='atendimento',
            name='criado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='atendimentos_criados', to=settings.AUTH_USER_MODEL),
        ),
    ]
