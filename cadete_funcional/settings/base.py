from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# Carregar .env primeiro
if (BASE_DIR / "config" / ".env").exists():
    environ.Env.read_env(str(BASE_DIR / "config" / ".env"))

SECRET_KEY = env("SECRET_KEY", default="dev-secret-key-change-me" if env("DEBUG", default=False) else "")
if not SECRET_KEY and not env("DEBUG", default=False):
    raise ValueError("SECRET_KEY deve ser definida em produção")
DEBUG = env("DEBUG", default=False)

# Parse ALLOWED_HOSTS com suporte a múltiplos formatos
_allowed_hosts = env("ALLOWED_HOSTS", default="localhost,127.0.0.1")
if isinstance(_allowed_hosts, str):
    ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts.split(",")]
else:
    ALLOWED_HOSTS = _allowed_hosts if _allowed_hosts else ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "core",
    "integracao",
]

# Jazzmin configuration
JAZZMIN_SETTINGS = {
    "site_title": "Administração Cadete Funcional",
    "site_header": "Sistema Cadete Funcional - Administração",
    "site_brand": "Cadete Funcional",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Bem-vindo ao Sistema Cadete Funcional (SCF)",
    "copyright": "Sistema Cadete Funcional - DTSIC AMAN",
    "search_model": ["core.Cadete", "core.Atendimento", "core.Profissional"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "core.Cadete"},
        {"model": "core.Atendimento"},
        {"model": "core.Profissional"},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin", "new_window": True},
        {"model": "auth.user"}
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["core", "auth"],
    "custom_links": {},
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Cadete": "fas fa-user-graduate",
        "core.Atendimento": "fas fa-stethoscope",
        "core.Profissional": "fas fa-user-md",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    "language_chooser": False,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cadete_funcional.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cadete_funcional.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="saude"),
        "USER": env("POSTGRES_USER", default="saude"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="saude"),
        "HOST": env("POSTGRES_HOST", default="db"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    },
    "source": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("SOURCE_DB_NAME", default=""),
        "USER": env("SOURCE_DB_USER", default=""),
        "PASSWORD": env("SOURCE_DB_PASSWORD", default=""),
        "HOST": env("SOURCE_DB_HOST", default=""),
        "PORT": env("SOURCE_DB_PORT", default="5432"),
    },
}

DATABASE_ROUTERS = ["integracao.routers.NoMigrateSourceRouter"]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS Configuration
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS", default="http://localhost:3000,http://127.0.0.1:3000").split(",")

# REST Framework Configuration
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend", "rest_framework.filters.SearchFilter", "rest_framework.filters.OrderingFilter"],
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle", "rest_framework.throttling.UserRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/hour", "user": "1000/hour"},
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# CORS
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Redirect after login/logout
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"