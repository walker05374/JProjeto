import os
from pathlib import Path
from django.contrib.messages import constants as messages
import dj_database_url
from dotenv import load_dotenv

from pathlib import Path

AUTH_USER_MODEL = 'meuapp.CustomUser'

# Para formulários e exibição no admin
DATE_INPUT_FORMATS = ['%Y-%m-%d']  # ou outros formatos como '%d/%m/%Y' se quiser
DATE_FORMAT = 'Y-m-d'  # Afeta templates com {{ date_var|date }}


# Localização (opcional, mas ajuda)
LANGUAGE_CODE = 'pt-br'
USE_L10N = False 
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

BASE_DIR = Path(__file__).resolve().parent.parent

# Chaves e configurações gerais
SECRET_KEY = 'django-insecure-p#-s*niuw&rarqw863#8aaw1vs*ru56cfir9nxdvpo(2w)ci3y'
DEBUG = True
ALLOWED_HOSTS = ['*']
SITE_ID = 1


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' 
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
SOCIALACCOUNT_LOGIN_ON_GET = True


# Aplicativos instalados
INSTALLED_APPS = [

    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount',
    'django_extensions',
    'inicio.meuapp',
    'rest_framework',
    'allauth.account',
    'allauth',
    'social_django',
    'jornada_maternal',
    'crispy_forms',
    'crispy_bootstrap4',
    'widget_tweaks',
    'notifications',

    

]


# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    


]


# URLs e templates
ROOT_URLCONF = 'jornada_maternal.urls'
TEMPLATES = [

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'inicio', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
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


#\c dbjornada
#GRANT ALL PRIVILEGES ON SCHEMA public TO dbjornada_user;
#ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dbjornada_user;

load_dotenv() # Carrega as variáveis do arquivo .env


DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]




# Configurações de mensagens
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}



STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'inicio/static'),
]



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'site'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jornadamaternal@gmail.com'
EMAIL_HOST_PASSWORD = 'zoieonynxuehwwhc'  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = DEFAULT_FROM_EMAIL


UTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',



]



GOOGLE_MAPS_API_KEY = 'AIzaSyCyvcrx33ToDSWfGyv5QHs6H6F1PmGs850'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


ACCOUNT_EMAIL_VERIFICATION = 'none'

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
            'SCOPE': ['profile', 'email'],
            'AUTH_PARAMS': {'access_type': 'online'},
        },
    },





    
}

DEBUG = True
