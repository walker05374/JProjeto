import os
from pathlib import Path
from django.contrib.messages import constants as messages

AUTH_USER_MODEL = 'meuapp.CustomUser'



BASE_DIR = Path(__file__).resolve().parent.parent

# Chaves e configurações gerais
SECRET_KEY = 'django-insecure-p#-s*niuw&rarqw863#8aaw1vs*ru56cfir9nxdvpo(2w)ci3y'
DEBUG = True
ALLOWED_HOSTS = ['*']
SITE_ID = 1


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Altere isso para 'mandatory' para forçar verificação
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



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


LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

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
DEFAULT_FROM_EMAIL = 'Jornada Maternal <noreply@mydomain.com>'
EMAIL_HOST_USER = 'jornadamaternal@gmail.com'
EMAIL_HOST_PASSWORD = 'zoieonynxuehwwhc'
DEFAULT_FROM_EMAIL = 'jornadamaternal@gmail.com'



SERVER_EMAIL = DEFAULT_FROM_EMAIL



UTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',



]

ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '143390340743-r8b8rs4tcp4igfjvbf8eplr8r45chind.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},

    },
    'facebook': {
        'APP': {  
        
            'client_id': '1818080662324015',
            'secret': 'd5b2ac89e42f52884fc36639197a18bb',
            'SCOPE': ['profile', 'email'],
            'AUTH_PARAMS': {'access_type': 'online'},
        },
    },





    
}

DEBUG = True
