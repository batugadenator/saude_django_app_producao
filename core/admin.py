"""Admin interface para os modelos da aplicação de saúde."""
import logging
import csv
from django.contrib import admin
from django.db.models import Count, Max, Q
from django.utils.html import format_html
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from .models import Cadete, Profissional, Atendimento
from collections import defaultdict
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


class UltimoAtendimentoFilter(admin.SimpleListFilter):
    title = 'status de atendimento'
    parameter_name = 'status_atendimento'

    def lookups(self, request, model_admin):
        return (('mais_30_dias', 'Último atendimento há mais de 30 dias'),)

    def queryset(self, request, queryset):
        if self.value() == "mais_30_dias":
            thirty_days_ago = timezone.now().date() - timedelta(days=30)
            return queryset.filter(
                Q(ultimo_atendimento_data__lt=thirty_days_ago) | Q(ultimo_atendimento_data__isnull=True)
            )


class AtendimentoInline(admin.TabularInline):
    model = Atendimento
    extra = 0  # Remove o formulário extra em branco
    fields = ("data", "atendimento", "lesao_tipo", "parte_do_corpo")
    readonly_fields = fields
    can_delete = False
    show_change_link = True  # Permite navegar para a página de detalhes do Atendimento

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Cadete)
class CadeteAdmin(admin.ModelAdmin):
    search_fields = ("numero", "nome", "nome_de_guerra")
    list_display = ("numero", "nome", "curso", "ano", "ultimo_atendimento", "subunidade", "pelotao")
    list_filter = (UltimoAtendimentoFilter, )
    inlines = [AtendimentoInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(ultimo_atendimento_data=Max("atendimentos__data"))
        return qs

    @admin.display(description="Último Atendimento")
    def ultimo_atendimento(self, obj):
        # obj.ultimo_atendimento_data está disponível por causa da anotação em get_queryset
        return obj.ultimo_atendimento_data

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sem-atendimento/",
                self.admin_site.admin_view(self.sem_atendimento_view),
                name="core_cadete_sem_atendimento",
            )
        ]
        return custom_urls + urls

    def sem_atendimento_view(self, request):
        cadetes_sem_atendimento = (Cadete.objects.annotate(num_atendimentos=Count("atendimentos"))
                                   .filter(num_atendimentos=0)
                                   .order_by("numero"))
        context = self.admin_site.each_context(request)
        context["title"] = "Cadetes Sem Atendimento Registrado"
        context["cadetes"] = cadetes_sem_atendimento
        context["opts"] = self.model._meta
        return TemplateResponse(request, "admin/core/cadete/sem_atendimento.html", context)


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    search_fields = ("identificador", "nome")
    list_display = ("tipo", "identificador", "nome")
    list_filter = ("tipo",)


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    search_fields = ("cadete__nome", "cadete__numero", "parte_lesionada", "local_da_lesao")
    list_display = ("id", "cadete", "data", "atendimento", "lesao_tipo", "parte_do_corpo", "lateralidade")
    list_filter = ("atendimento", "data", "lesao_tipo", "parte_do_corpo", "lateralidade", "origem_da_lesao", "causa")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "export-csv/",
                self.admin_site.admin_view(self.export_csv_view),
                name="core_atendimento_export_csv",
            )
        ]
        return custom_urls + urls

    def export_csv_view(self, request):
        """Export de atendimentos com limite de segurança e logging."""
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Limite de segurança: máximo 10000 registros por export
        MAX_EXPORT_RECORDS = 10000
        
        # Registra tentativa de export
        logger.info(f"Export CSV iniciado por {request.user.username}")
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="atendimentos.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Cadete', 'Data', 'Atendimento', 'Lesão Tipo', 'Parte do Corpo', 'Lateralidade', 'Criado Em'])

        # Query otimizada com select_related e limite de segurança
        atendimentos = (
            Atendimento.objects
            .select_related('cadete')
            .values_list(
                'id', 'cadete__numero', 'cadete__nome', 'data', 'atendimento',
                'lesao_tipo', 'parte_do_corpo', 'lateralidade', 'criado_em'
            )
            [:MAX_EXPORT_RECORDS]
        )
        
        # Streaming para evitar carregar tudo na memória
        total_exported = 0
        for atendimento in atendimentos:
            writer.writerow([
                atendimento[0],  # id
                f"{atendimento[1]} - {atendimento[2]}",  # cadete
                atendimento[3],  # data
                atendimento[4],  # atendimento
                atendimento[5],  # lesao_tipo
                atendimento[6],  # parte_do_corpo
                atendimento[7],  # lateralidade
                atendimento[8],  # criado_em
            ])
            total_exported += 1
        
        logger.info(f"Export CSV concluído: {total_exported} registros exportados por {request.user.username}")
        
        # Adiciona aviso se atingiu o limite
        if total_exported >= MAX_EXPORT_RECORDS:
            response.write(f"\n# AVISO: Limite de {MAX_EXPORT_RECORDS} registros atingido. Use filtros para refinar a busca.")
        
        return response