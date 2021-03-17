import os
from pathlib import Path

from django.conf.global_settings import DATETIME_INPUT_FORMATS

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Application definition
INSTALLED_APPS = [
    # Custom AdminConfig
    'src.protection_defenders.project_apps.ProtectionInternationalDefendersAdminConfig',
    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    # Third apps
    'rest_framework',
    # 'corsheaders',
    'tinymce',
    # APP
    'src.protection_defenders.defenders_app.apps.ProtectionDefendersAppConfig',
    'src.protection_defenders.defenders_auth.apps.DefendersAuthConfig',
    'src.protection_defenders.core'
]

AUTH_USER_MODEL = 'defenders_auth.User'

MIDDLEWARE = [
    'src.protection_defenders.defenders_auth.middlewares.CookieJWTMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.protection_defenders.project_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'src.protection_defenders.project_wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 20,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'src.protection_defenders.core.auth.IsAuthenticatedAndActive',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',)
}

NOAUTH_URLS = (
    '/token/access/',
    '/token/logout/',
)

DEFAULT_DATE_TIME_FORMAT = DATETIME_INPUT_FORMATS[0]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTHENTICATION_BACKENDS = [
    'src.protection_defenders.defenders_auth.auth_backend.AuthBackend',
]

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MAX_UPLOAD_SIZE = "5242880"  # 5MB

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'app': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_false'],
            'filename': os.path.join(BASE_DIR, 'logs.txt'),
            'formatter': 'app',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}