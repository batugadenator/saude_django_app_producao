from django.contrib import admin
from .models import UsuarioImportado


@admin.register(UsuarioImportado)
class UsuarioImportadoAdmin(admin.ModelAdmin):
    search_fields = ("username", "email", "nome", "external_id")
    list_display = ("external_id", "username", "email", "nome", "ativo", "imported_at")
    list_filter = ("ativo",)