import os
from datetime import timedelta
from .settings_base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
CIPHER_KEY = os.environ.get('CIPHER_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOST')]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DB_ENGINE'),
        'NAME': os.environ.get('DJANGO_DB_NAME'),
        'USER': os.environ.get('DJANGO_DB_USER'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
        'HOST': os.environ.get('DJANGO_DB_HOST'),
        'PORT': os.environ.get('DJANGO_DB_PORT'),
    }
}

CORS_ORIGIN_WHITELIST = (
    os.environ.get('DJANGO_ALLOWED_ORIGIN'),
)
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True # to accept cookies via ajax request

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=12),
    'ROTATE_REFRESH_TOKENS': False,
    'UPDATE_LAST_LOGIN': True,
    'COOKIE_ACCESS_KEY': os.environ.get('JWT_COOKIE_ACCESS_KEY'),
    'COOKIE_REFRESH_KEY': os.environ.get('JWT_COOKIE_REFRESH_KEY'),
    'COOKIE_SECURE': False,
    'COOKIE_HTTPONLY': True,
    'COOKIE_DOMAIN': os.environ.get('JWT_COOKIE_DOMAIN'),
    'COOKIE_SAMESITE': 'Strict',
}

EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT'))
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

APP_FRONTEND_URL = os.environ.get('APP_FRONTEND_URL') # 'https://dscompass.dataira.com'
USER_ACTIVATION_REDIRECT_URL = os.environ.get('USER_ACTIVATION_REDIRECT_URL') # 'https://dscompass.dataira.com/?user=created'

TIME_ZONE = 'Europe/Madrid'