import os
from pathlib import Path
from django.contrib.messages import constants as messages
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-p#-s*niuw&rarqw863#8aaw1vs*ru56cfir9nxdvpo(2w)ci3y'
DEBUG = True
ALLOWED_HOSTS = ['*']
SITE_ID = 1

# --- IMPORTANTE: Modelo de Usuário Personalizado ---
AUTH_USER_MODEL = 'meuapp.CustomUser'

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps de Terceiros (Ordem Importa)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_extensions',
    'rest_framework',
    'social_django',
    'crispy_forms',
    'crispy_bootstrap4',
    'widget_tweaks',
    'notifications',
    
    # Seus Apps
    'inicio.meuapp',
    'jornada_maternal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # Obrigatório para Allauth
]

ROOT_URLCONF = 'jornada_maternal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'inicio', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Obrigatório para Allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'inicio.meuapp.context_processors.clientes_context',
                'inicio.meuapp.context_processors.vacina_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'jornada_maternal.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = False
USE_TZ = True

DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d/%m/%Y']
DATE_FORMAT = 'd/m/Y'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'inicio/static')]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# --- CONFIGURAÇÕES DE LOGIN E ALLAUTH ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'site' # Redireciona para 'site' após login
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'

# Backends de Autenticação (Permite login normal + social)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configurações do Allauth
ACCOUNT_AUTHENTICATION_METHOD = 'username_email' # Permite logar com User ou Email
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none' # Evita bloqueio por falta de email verificado no teste
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '34871990688-nhvf5m7lt9v7kgrgckof019efvp82ocm.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'facebook': {
        'APP': {  
            'client_id': '897035592479067',
            'secret': '4a0ca8dcb8e694469a4597f6a00b5c2e',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jornadamaternal@gmail.com'
EMAIL_HOST_PASSWORD = 'zoieonynxuehwwhc'  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'


GOOGLE_MAPS_API_KEY = 'AIzaSyCyvcrx33ToDSWfGyv5QHs6H6F1PmGs850'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'