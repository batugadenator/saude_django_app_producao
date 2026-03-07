from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CadeteViewSet, AtendimentoViewSet, ProfissionalViewSet

router = DefaultRouter()
router.register(r"cadetes", CadeteViewSet)
router.register(r"profissionais", ProfissionalViewSet)
router.register(r"atendimentos", AtendimentoViewSet)

urlpatterns = [path("", include(router.urls))]