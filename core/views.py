import logging
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.db.models import Count, Q
from .models import Cadete, Atendimento, Profissional

logger = logging.getLogger(__name__)


def logout_view(request):
    """Faz logout do usuário e redireciona para a página inicial."""
    logout(request)
    return redirect('index')


def index(request):
    """Página inicial com estatísticas e lesões mais comuns."""
    try:
        # Totais gerais usando agregação eficiente
        total_cadetes = Cadete.objects.count()
        total_atendimentos = Atendimento.objects.count()
        profissionais_count = Profissional.objects.count()
        
        # Taxa de atendimento (atendimentos por cadete)
        taxa_atendimento = (
            round(total_atendimentos / total_cadetes, 1) 
            if total_cadetes > 0 
            else 0
        )
        
        # Top 5 lesões mais comuns (ignorando vazios)
        top_lesoes = (
            Atendimento.objects.exclude(Q(lesao_tipo__isnull=True) | Q(lesao_tipo__exact=""))
            .values("lesao_tipo")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        )

        context = {
            "total_cadetes": total_cadetes,
            "total_atendimentos": total_atendimentos,
            "profissionais_count": profissionais_count,
            "taxa_atendimento": taxa_atendimento,
            "top_lesoes": top_lesoes,
        }
        
        return render(request, "index.html", context)
    except Exception as e:
        logger.error(f"Erro ao renderizar página inicial: {e}", exc_info=True)
        raise