from datetime import timedelta

from .settings_base import *

SECRET_KEY = '...'
CIPHER_KEY = '...'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dscompass',
        'USER': 'CharlesDarwin',
        'PASSWORD': 'dscompass',
    }
}

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
)
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True  # to accept cookies via ajax request

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=12),
    'ROTATE_REFRESH_TOKENS': False,
    'UPDATE_LAST_LOGIN': True,
    'COOKIE_ACCESS_KEY': 'access',
    'COOKIE_REFRESH_KEY': 'refresh',
    'COOKIE_SECURE': False,
    'COOKIE_HTTPONLY': True,
    'COOKIE_DOMAIN': 'localhost',
    'COOKIE_SAMESITE': 'Strict',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)
STATIC_URL = '/static/'

APP_FRONTEND_URL = 'http://localhost:8080'
USER_ACTIVATION_REDIRECT_URL = 'http://localhost:8080/?user=created'

TIME_ZONE = 'Europe/Madrid'
