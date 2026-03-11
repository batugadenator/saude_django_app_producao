"""Serializers para os modelos da aplicação de saúde."""
import logging
from datetime import date
from rest_framework import serializers
from .models import Cadete, Atendimento, Profissional

logger = logging.getLogger(__name__)


class CadeteSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Cadete com validações."""
    
    class Meta:
        model = Cadete
        fields = "__all__"
        read_only_fields = ["id", "criado_em", "atualizado_em", "criado_por"]
    
    def validate_numero(self, value):
        """Valida que número do cadete é positivo."""
        if value <= 0:
            raise serializers.ValidationError("Número do cadete deve ser positivo.")
        return value
    
    def validate_nome(self, value):
        """Valida que nome não está vazio."""
        if not value or not value.strip():
            raise serializers.ValidationError("Nome do cadete não pode estar vazio.")
        return value


class ProfissionalSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Profissional com validações."""
    
    class Meta:
        model = Profissional
        fields = "__all__"
        read_only_fields = ["id", "criado_em", "atualizado_em", "criado_por"]
    
    def validate(self, data):
        """Valida que tipo e identificador são fornecidos."""
        if not data.get("tipo"):
            raise serializers.ValidationError("Tipo do profissional é obrigatório.")
        if not data.get("identificador"):
            raise serializers.ValidationError("Identificador é obrigatório.")
        return data


class AtendimentoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Atendimento com campos relacionados e validações."""
    
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
        read_only_fields = ["id", "criado_em", "atualizado_em", "criado_por"]
    
    def validate_data(self, value):
        """Valida que data não é no futuro."""
        if value > date.today():
            raise serializers.ValidationError("Data do atendimento não pode ser no futuro.")
        return value
    
    def validate(self, data):
        """Validações cruzadas do atendimento."""
        # Valida que cadete existe
        if not data.get("cadete"):
            raise serializers.ValidationError("Cadete é obrigatório.")
        # Valida que data existe
        if not data.get("data"):
            raise serializers.ValidationError("Data do atendimento é obrigatória.")
        return data