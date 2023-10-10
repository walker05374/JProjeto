import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-p#-s*niuw&rarqw863#8aaw1vs*ru56cfir9nxdvpo(2w)ci3y'
DEBUG = True





ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7


ALLOWED_HOSTS = ['*']


SITE_ID = 1
INSTALLED_APPS = [


     'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    


]

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

ROOT_URLCONF = 'jornada_maternal.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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




STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),

    'static',
    'media',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'site'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Jornada Maternal <noreply@mydomain.com>'
EMAIL_HOST_USER = 'jornadamaternal@gmail.com'
EMAIL_HOST_PASSWORD = 'zoieonynxuehwwhc'
SERVER_EMAIL = DEFAULT_FROM_EMAIL





SOCIALACCOUNT_LOGIN_ON_GET=True

UTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_VERIFICATION = 'none'



SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '143390340743-1r857685usse5leinas3on0f02jr79o1.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},


    },
    'facebook': {
        'APP': {  
        
            'client_id': '1482552329230726',
            'secret': '145bf48b8476e719ef08af7bbab9c514',
            'SCOPE': ['profile', 'email'],
            'AUTH_PARAMS': {'access_type': 'online'},
        },
    },
}
