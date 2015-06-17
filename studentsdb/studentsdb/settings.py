# -*- coding: utf-8 -*-
from django.conf import global_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

gettext_noop = lambda s: s

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3c0zw#vof&2tpn#3x(nvq2jg6p8$r8jjba=6_(1vuajl7j)fl0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'crispy_forms',
    'students',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'studentsdb.urls'

WSGI_APPLICATION = 'studentsdb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

try:
    from database_settings import DATABASES
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
        }
    }

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'studentsdb.context_processors.students_proc',
    'students.context_processors.groups_processor',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'uk'
LANGUAGES = (
    ('uk', gettext_noop('Ukrainian')),
    ('en', gettext_noop('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

############### SMTP settings ################
ADMIN_EMAIL = 'alexander.tyapkin@hotmail.com'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'atyapkin20@gmail.com'
EMAIL_HOST_PASSWORD = 'LqWREnAPdNJZM8F6VE_rXw'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
###############################################

######## Localhost SMTP settings ########
# ADMIN_EMAIL = 'admin@test.loc'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '1025'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
#########################################

## Crispy forms template pack settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django contact form settings
DEFAULT_FROM_EMAIL = ADMIN_EMAIL
MANAGERS = (
    ('Alexander OUTLOOK', 'alexander.tyapkin@hotmail.com'),
    ('Alexander GMAIL', 'atyapkin20@gmail.com'),
)

LOG_FILE = os.path.join(BASE_DIR, 'studentsdb.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'students.signals': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'students.views.contact_admin': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'students.forms.forms': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
        }
    }
}
