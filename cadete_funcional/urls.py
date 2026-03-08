from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

from core.health import healthz
from core.views import index, logout_view


urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("api/", include("core.api_urls")),
    path("accounts/login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", logout_view, name="logout"),
    path("healthz/", healthz, name="healthz"),
]
