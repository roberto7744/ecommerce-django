from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# SECRET KEY & DEBUG
# ---------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-no-usar-en-produccion")

DEBUG = os.environ.get("DEBUG", "True") == "True"

# ---------------------------------------------------------
# ALLOWED HOSTS
# ---------------------------------------------------------
ALLOWED_HOSTS = [
    "*",
    "ecommerce-django-production-39cb.up.railway.app",
]

# ---------------------------------------------------------
# APPS
# ---------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_yasg',

    # App del proyecto
    'store',
]

# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Archivos estáticos en deploy

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta templates global
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------
# PASSWORDS
# ---------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# ---------------------------------------------------------
# INTERNACIONALIZACIÓN
# ---------------------------------------------------------
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# STATICFILES PARA DEPLOY
# ---------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------------
# REST FRAMEWORK + JWT
# ---------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# ---------------------------------------------------------
# CSRF — NECESARIO PARA RAILWAY (HTTPS)
# ---------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://ecommerce-django-production-39cb.up.railway.app",
]
