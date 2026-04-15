import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_celery_beat',
    'reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reports.middleware.AuditLoggingMiddleware',
    'reports.middleware.SecurityAuditMiddleware',
]

ROOT_URLCONF = 'npc_reporting.urls'

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

WSGI_APPLICATION = 'npc_reporting.wsgi.application'

# Database Configuration - Supports both local SQLite and Render PostgreSQL
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'NPC_REPORTING_SYSTEM'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', '2002'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS Configuration for Production
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:3000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "https://npc-reporting-frontend.netlify.app",
]

if not DEBUG:
    CORS_ALLOWED_ORIGINS.extend([
        os.getenv('FRONTEND_URL', 'https://npc-reporting-frontend.netlify.app'),
    ])

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type', 'dnt',
    'origin', 'user-agent', 'x-csrftoken', 'x-requested-with', 'cache-control', 'pragma', 'expires',
]

SITE_URL = os.getenv('SITE_URL', 'https://npc-reporting-backend.onrender.com')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://npc-reporting-frontend.netlify.app')

MAX_UPLOAD_SIZE = 10485760

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@npc-reporting.com')

REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'reports.error_handlers.custom_exception_handler'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'app.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'reports': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

os.makedirs(BASE_DIR / 'logs', exist_ok=True)

SIGNATURE_SECRET_KEY = os.getenv('SIGNATURE_SECRET_KEY', SECRET_KEY)
SIGNATURE_ENCRYPTION_KEY = os.getenv(
    'SIGNATURE_ENCRYPTION_KEY',
    'gAAAAABl_default_key_change_in_production_12345678901234567890='
)
SIGNATURE_2FA_ENABLED = os.getenv('SIGNATURE_2FA_ENABLED', 'True') == 'True'
SIGNATURE_OTP_VALIDITY_MINUTES = int(os.getenv('SIGNATURE_OTP_VALIDITY_MINUTES', '5'))
SIGNATURE_MAX_OTP_ATTEMPTS = int(os.getenv('SIGNATURE_MAX_OTP_ATTEMPTS', '3'))
SIGNATURE_RATE_LIMIT_HOUR = int(os.getenv('SIGNATURE_RATE_LIMIT_HOUR', '10'))
SIGNATURE_RATE_LIMIT_DAY = int(os.getenv('SIGNATURE_RATE_LIMIT_DAY', '50'))
SIGNATURE_LOG_GEOLOCATION = os.getenv('SIGNATURE_LOG_GEOLOCATION', 'False') == 'True'
SIGNATURE_ENABLE_ENCRYPTION = os.getenv('SIGNATURE_ENABLE_ENCRYPTION', 'True') == 'True'
SIGNATURE_ENABLE_VERIFICATION_HASH = os.getenv('SIGNATURE_ENABLE_VERIFICATION_HASH', 'True') == 'True'
SIGNATURE_REQUIRE_DEVICE_FINGERPRINT = os.getenv('SIGNATURE_REQUIRE_DEVICE_FINGERPRINT', 'True') == 'True'
SIGNATURE_NOTIFY_ON_SIGNATURE = os.getenv('SIGNATURE_NOTIFY_ON_SIGNATURE', 'True') == 'True'
SIGNATURE_NOTIFY_ON_SUSPICIOUS = os.getenv('SIGNATURE_NOTIFY_ON_SUSPICIOUS', 'True') == 'True'

LOGGING['loggers']['signature_audit'] = {
    'handlers': ['file'],
    'level': 'INFO',
    'propagate': False,
}
