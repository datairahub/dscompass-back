import os
from datetime import timedelta
from .settings_base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
CIPHER_KEY = os.environ.get('CIPHER_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ["ds-compass-api.protectioninternational.org"]

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.mysql",
        'NAME': os.environ.get('DJANGO_DB_NAME'),
        'USER': os.environ.get('DJANGO_DB_USER'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
    }
}

CORS_ORIGIN_WHITELIST = (
    "ds-compass.protectioninternational.org",
)
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True # to accept cookies via ajax request

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=12),
    'ROTATE_REFRESH_TOKENS': False,
    'UPDATE_LAST_LOGIN': True,
    'COOKIE_ACCESS_KEY': "access",
    'COOKIE_REFRESH_KEY': "refresh",
    'COOKIE_SECURE': False,
    'COOKIE_HTTPONLY': True,
    'COOKIE_DOMAIN': "protectioninternational.org",
    'COOKIE_SAMESITE': 'Lax',
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

APP_FRONTEND_URL = "https://ds-compass.protectioninternational.org/"
USER_ACTIVATION_REDIRECT_URL = "https://ds-compass.protectioninternational.org/?user=created"

TIME_ZONE = 'Europe/Madrid'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'), )
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

