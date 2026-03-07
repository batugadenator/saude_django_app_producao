import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cadete, Atendimento, Profissional
from .serializers import CadeteSerializer, AtendimentoSerializer, ProfissionalSerializer

logger = logging.getLogger(__name__)


class CadeteViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Cadetes com filtro e busca."""
    queryset = Cadete.objects.all().order_by("numero")
    serializer_class = CadeteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["curso", "ano", "subunidade", "pelotao"]
    search_fields = ["numero", "nome", "nome_de_guerra"]
    ordering_fields = ["numero", "nome", "curso", "ano"]


class ProfissionalViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Profissionais com filtro."""
    queryset = Profissional.objects.all().order_by("tipo", "identificador")
    serializer_class = ProfissionalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["tipo"]
    search_fields = ["identificador", "nome"]


class AtendimentoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Atendimentos com filtros, busca e otimização de queries."""
    queryset = Atendimento.objects.select_related("cadete").all().order_by("-data", "-id")
    serializer_class = AtendimentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["cadete", "data", "atendimento", "profissional_tipo", "lesao_tipo", "parte_do_corpo", "alta"]
    search_fields = ["cadete__nome", "cadete__numero", "lesao_tipo", "profissional_nome"]
    ordering_fields = ["data", "criado_em", "cadete"]