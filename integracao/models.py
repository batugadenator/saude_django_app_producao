from django.db import models


class UsuarioImportado(models.Model):
    external_id = models.BigIntegerField(db_index=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    raw = models.JSONField(default=dict)
    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("external_id",)]

    def __str__(self):
        return self.username or self.email or str(self.external_id)