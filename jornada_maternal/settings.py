import os
from pathlib import Path
from django.contrib.messages import constants as messages
import dj_database_url
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# AVISO: Mantenha esta chave secreta em segredo em produção!
SECRET_KEY = 'django-insecure-p#-s*niuw&rarqw863#8aaw1vs*ru56cfir9nxdvpo(2w)ci3y'

# DEBUG: True para desenvolvimento local, False para produção (Render)
DEBUG = True 

ALLOWED_HOSTS = ['*']
SITE_ID = 1

# Modelo de Usuário Personalizado
AUTH_USER_MODEL = 'meuapp.CustomUser'

# Aplicativos Instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # Obrigatório para o allauth

    # Allauth (Autenticação Social)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    # Ferramentas e UI
    'django_extensions',
    'rest_framework',
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
    'allauth.account.middleware.AccountMiddleware', # Obrigatório para o allauth
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
                'django.template.context_processors.request', # Obrigatório para o allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'inicio.meuapp.context_processors.clientes_context',
                'inicio.meuapp.context_processors.vacina_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'jornada_maternal.wsgi.application'

# Banco de Dados
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

# Validadores de Senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = False
USE_TZ = True

# Datas
DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d/%m/%Y']
DATE_FORMAT = 'd/m/Y'

# Arquivos Estáticos e Mídia
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'inicio/static')]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuração de Mensagens (Bootstrap)
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# --- CONFIGURAÇÕES DE LOGIN GERAIS ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'site'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'

# Backends de Autenticação (Mantém os dois como você pediu)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# --- CONFIGURAÇÕES CRÍTICAS DO ALLAUTH (CORREÇÃO DE FLUXO) ---

# Permite logar com user ou email
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

# OBRIGATÓRIO: Pede o email, mas não exige verificação por link
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none' 
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

# CRUCIAL: Não pedir para criar username (o sistema gera um a partir do email)
ACCOUNT_USERNAME_REQUIRED = False 

# CRUCIAL: Tenta cadastrar direto sem mostrar formulário extra
SOCIALACCOUNT_AUTO_SIGNUP = True 

# CRUCIAL: Se usar link GET (seu HTML antigo), tenta pular a confirmação de segurança
SOCIALACCOUNT_LOGIN_ON_GET = True 

# Campos do modelo CustomUser
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'

# --- PROVEDORES SOCIAIS ---
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '34871990688-nhvf5m7lt9v7kgrgckof019efvp82ocm.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        # ESSA PARTE É A MAIS IMPORTANTE PARA NÃO PEDIR EMAIL:
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        # Garante que pegamos os dados verificados
        'VERIFIED_EMAIL': True,
    },
    'facebook': {
        'APP': {  
            'client_id': '897035592479067',
            'secret': '4a0ca8dcb8e694469a4597f6a00b5c2e',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'METHOD': 'oauth2', 
    },
}

# Configuração de Envio de E-mail (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jornadamaternal@gmail.com'
EMAIL_HOST_PASSWORD = 'zoieonynxuehwwhc'  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --- CORREÇÃO HTTP/HTTPS ---
# Corrige o problema do Google rejeitar 'https' no localhost (Erro 400)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
else:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

# API Maps
GOOGLE_MAPS_API_KEY = 'AIzaSyCyvcrx33ToDSWfGyv5QHs6H6F1PmGs850'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'