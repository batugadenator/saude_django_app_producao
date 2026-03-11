from django.db import models
from django.db.models import constraints
from django.contrib.auth.models import User


class Cadete(models.Model):
    numero = models.IntegerField(unique=True, db_index=True)
    nome = models.CharField(max_length=255)
    nome_de_guerra = models.CharField(max_length=255, blank=True, null=True)
    curso = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ano = models.IntegerField(blank=True, null=True, db_index=True)
    subunidade = models.CharField(max_length=100, blank=True, null=True)
    pelotao = models.CharField(max_length=50, blank=True, null=True)
    cmt_curso = models.CharField(max_length=100, blank=True, null=True)
    cmt_subunidade = models.CharField(max_length=100, blank=True, null=True)
    cmt_pelotao = models.CharField(max_length=100, blank=True, null=True)
    
    # Auditoria
    criado_em = models.DateTimeField(auto_now_add=True, db_index=True)
    atualizado_em = models.DateTimeField(auto_now=True, db_index=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="cadetes_criados")

    class Meta:
        verbose_name = "Cadete"
        verbose_name_plural = "Cadetes"
        ordering = ["numero"]

    def __str__(self):
        return f"{self.numero} - {self.nome}"


class Profissional(models.Model):
    TIPO_CHOICES = [
        ("medico", "Médico"),
        ("fisioterapeuta", "Fisioterapeuta"),
        ("educador_fisico", "Educador Físico"),
        ("nutricionista", "Nutricionista"),
        ("psicopedagogo", "Psicopedagogo"),
        ("sred", "S-RED"),
        ("enfermagem", "Enfermagem/PM CC"),
        ("instrutor", "Instrutor"),
        ("estatistico", "Estatístico"),
        ("ti", "Profissional de TI"),
    ]

    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, db_index=True)
    identificador = models.CharField(max_length=120)
    nome = models.CharField(max_length=255, blank=True, null=True)
    
    # Auditoria
    criado_em = models.DateTimeField(auto_now_add=True, db_index=True)
    atualizado_em = models.DateTimeField(auto_now=True, db_index=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="profissionais_criados")

    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"
        ordering = ["tipo", "identificador"]
        constraints = [
            constraints.UniqueConstraint(fields=["tipo", "identificador"], name="profissional_tipo_identificador_unique")
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.identificador}"


class Atendimento(models.Model):
    TIPO_ATENDIMENTO = [("inicial", "Inicial"), ("retorno", "Retorno")]

    cadete = models.ForeignKey(Cadete, on_delete=models.PROTECT, related_name="atendimentos", db_index=True)
    data = models.DateField(db_index=True)
    hora = models.TimeField(blank=True, null=True)
    atendimento = models.CharField(max_length=20, choices=TIPO_ATENDIMENTO, db_index=True)
    profissional_tipo = models.CharField(max_length=80, blank=True, null=True, db_index=True)
    profissional_nome = models.CharField(max_length=255, blank=True, null=True)

    lesao_tipo = models.CharField(max_length=60, blank=True, null=True, db_index=True)
    parte_do_corpo = models.CharField(max_length=80, blank=True, null=True, db_index=True)
    lateralidade = models.CharField(max_length=20, blank=True, null=True)
    parte_lesionada = models.CharField(max_length=120, blank=True, null=True)
    local_da_lesao = models.CharField(max_length=120, blank=True, null=True)
    origem_da_lesao = models.CharField(max_length=120, blank=True, null=True)
    sred = models.CharField(max_length=120, blank=True, null=True)
    causa = models.CharField(max_length=120, blank=True, null=True)
    atividade = models.CharField(max_length=120, blank=True, null=True)
    tfm_taf = models.CharField(max_length=120, blank=True, null=True)
    modalidade = models.CharField(max_length=120, blank=True, null=True)
    tratamento = models.CharField(max_length=120, blank=True, null=True)
    medicamentoso = models.CharField(max_length=255, blank=True, null=True)

    fisioterapia = models.BooleanField(default=False, db_index=True)
    sef = models.BooleanField(default=False)
    nutricionista = models.BooleanField(default=False)
    psicopedagogica = models.BooleanField(default=False)

    rx = models.BooleanField(default=False)
    usg = models.BooleanField(default=False)
    tc = models.BooleanField(default=False)
    rm = models.BooleanField(default=False)
    dexa = models.BooleanField(default=False)
    sangue = models.BooleanField(default=False)

    dispensa = models.BooleanField(default=False)
    vcl = models.BooleanField(default=False)
    alta = models.BooleanField(default=False, db_index=True)
    risco_cirurgico = models.BooleanField(default=False)

    # Auditoria
    criado_em = models.DateTimeField(auto_now_add=True, db_index=True)
    atualizado_em = models.DateTimeField(auto_now=True, db_index=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="atendimentos_criados")

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"
        ordering = ["-data", "-criado_em"]
        indexes = [
            models.Index(fields=["cadete", "data"], name="idx_cadete_data"),
            models.Index(fields=["data", "profissional_tipo"], name="idx_data_profissional"),
        ]

    def __str__(self):
        return f"Atendimento {self.id} ({self.cadete.numero}) {self.data}"