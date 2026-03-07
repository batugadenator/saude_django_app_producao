from django.contrib import admin
from django.urls import path, include

from core.health import healthz
from core.views import index


urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("api/", include("core.api_urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("healthz/", healthz, name="healthz"),
]