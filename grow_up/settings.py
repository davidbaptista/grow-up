import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'k*r3kv%xlkkk2d+5$*aebwmps(jg=x1=90rw4_^91s6^ls4*m#'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '84.90.108.132']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'formtools',
    'website.apps.GrowUpWebsiteConfig',
    'dashboard.apps.DashboardConfig',
    'authentication.apps.AuthenticationConfig',
    'administration.apps.AdministrationConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'grow_up.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'grow_up.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'grow_up',
        'USER': 'david',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'website.validators.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'website.validators.MinimumLengthValidator'
    },
    {
        'NAME': 'website.validators.NumericPasswordValidator',
    },
]

LANGUAGES = [
    ('pt', _('Portuguese'))
]

LANGUAGE_CODE = 'pt'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    'static/',
    'tools/',
    'data/',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/index/'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'grow.up.portugal@gmail.com'
EMAIL_HOST_PASSWORD = 'vlylnaqnqpkzaefb'
EMAIL_PORT = 587

DATE_INPUT_FORMATS = ['%d/%m/%Y']

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
