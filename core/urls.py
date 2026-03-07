from django.urls import path
from .views import index
from .health import healthz

urlpatterns = [
    path("healthz/", healthz, name="healthz"),
    path("", index, name="index"),
]