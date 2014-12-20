"""
Django settings for tuesday project.
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.join(BASE_DIR, os.path.pardir)

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

# Extensions
INSTALLED_APPS += (
    'django_extensions',
)


INSTALLED_APPS += (
    'arm',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tuesday.urls'
WSGI_APPLICATION = 'tuesday.wsgi.application'

# Templates
TEMPLATE_DIRS = (
    BASE_DIR + '/templates/'
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

