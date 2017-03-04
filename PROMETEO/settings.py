"""
Django settings for PROMETEO project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '427z3^uwql6f&0kygc=0i7p*t3dni7_fk82k*b&j)#6$$=soon'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'empresas',
    'modelos_existentes',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'PROMETEO.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR,'usuarios/templates'),
                 os.path.join(BASE_DIR,'empresas/templates'),]
        ,
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

WSGI_APPLICATION = 'PROMETEO.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'OPTIONS': {
            'options': '-c search_path=sql_soluciones'
        },
    'NAME': 'prometeo',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': '127.0.0.1',
    'PORT': '5432',
    'CONN_MAX_AGE': 500,
    }
}


STATIC_URL = '/static/'


HOSTNAME = '54.200.145.159:8080'
MEDIA_ROOT = 'PROMETEO/media/'
MEDIA_URL = 'http://%s/PROMETEO/media/'%(HOSTNAME)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGIN_URL = reverse_lazy('login_user')
LOGIN_REDIRECT_URL = reverse_lazy('principal')
LOGOUT_URL = reverse_lazy('login_user')

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', "usuarios.backends.BackendUsuarios")


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


RECAPTCHA_PUBLIC_KEY = '6LcLryMTAAAAAEbrchsa2PMbizBwJoOk197CK15q'

RECAPTCHA_PRIVATE_KEY = '6LcLryMTAAAAAC7mDdMMBLwm7fEMlKlEaExFY52-'

NOCAPTCHA = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sivore@correounivalle.edu.co'
EMAIL_HOST_PASSWORD = 'sivorePass06'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

