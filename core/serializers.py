"""Serializers para os modelos da aplicação de saúde."""
import logging
from rest_framework import serializers
from .models import Cadete, Atendimento, Profissional

logger = logging.getLogger(__name__)


class CadeteSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Cadete."""
    
    class Meta:
        model = Cadete
        fields = "__all__"
        read_only_fields = ["id"]


class ProfissionalSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Profissional."""
    
    class Meta:
        model = Profissional
        fields = "__all__"
        read_only_fields = ["id"]


class AtendimentoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Atendimento com campos relacionados."""
    
    cadete = CadeteSerializer(read_only=True)
    cadete_id = serializers.PrimaryKeyRelatedField(
        source="cadete",
        queryset=Cadete.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Atendimento
        fields = "__all__"
        read_only_fields = ["id", "criado_em"]