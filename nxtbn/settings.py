"""
Django settings for nxtbn project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

"""
 Important: Must Read this.
 01. The DEBUG and DEVELOPMENT_SERVER variables are not same thing. DEVELOPMENT_SERVER is custom for special purpose.
 02. Please read insturction of every enviroment variables to avoid any security risk
 03. To develop and solve a problem first, you first read whole settings.py files.
"""

from pathlib import Path
import os
from datetime import timedelta
import sys
from dotenv import load_dotenv

load_dotenv()


def get_env_var(key, default=None, var_type=str):
    value = os.getenv(key)
    if value is None:
        if default is not None:
            return default
        else:
            raise ValueError(f"Environment variable '{key}' is missing, and no default value is provided.")
    if var_type == int:
        return int(value)
    if var_type == bool:
        return value.lower() in ["true", "1", "yes"]
    if var_type == list:
        return [item.strip() for item in value.split(",") if item.strip()]
    return value


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: Keep the secret key used in production confidential!
SECRET_KEY = get_env_var('SECRET_KEY', 'django-insecure-#(7!^&*')

# SECURITY WARNING: Debug mode exposes sensitive information and should only be used during development.
DEBUG = get_env_var("DEBUG", default=False, var_type=bool)

# SECURITY WARNING: Allowing all origins in production is a security risk.
CORS_ORIGIN_ALLOW_ALL = get_env_var("CORS_ORIGIN_ALLOW_ALL", default=False, var_type=bool)

ALLOWED_HOSTS = get_env_var("ALLOWED_HOSTS", default=["*"], var_type=list)

CORS_ALLOWED_ORIGINS = get_env_var("CORS_ALLOWED_ORIGINS", default=[
    'http://localhost:3000',
], var_type=list)


DEVELOPMENT_SERVER = get_env_var("DEVELOPMENT_SERVER", default=False, var_type=bool)


SITE_ID = 1

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = get_env_var("SECURE_SSL_REDIRECT", default=False, var_type=bool)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

LOCAL_APPS = [
    'nxtbn.core',
    'nxtbn.home',
    'nxtbn.users.apps.UsersConfig',
    'nxtbn.seo',
    'nxtbn.discount',
    'nxtbn.product',
    'nxtbn.invoice',
    'nxtbn.plugins',
    'nxtbn.payment',
    'nxtbn.order',
    'nxtbn.tax',
    'nxtbn.filemanager',
    'nxtbn.vendor',
    'nxtbn.cart',
    'nxtbn.gift_card',
    'nxtbn.post',
]

HELPING_HAND_APPS = [
    'rest_framework',
    'allauth',
    'allauth.account',
    'drf_yasg',
    'django_extensions',
    "corsheaders",
    "django_filters",
    'django_celery_beat',
]

INSTALLED_APPS += LOCAL_APPS + HELPING_HAND_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # TODO: Do we need this?
    'nxtbn.core.currency_middleware.CurrencyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'nxtbn.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'nxtbn.pluggins'),
        ],
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

WSGI_APPLICATION = 'nxtbn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if get_env_var('DATABASE_NAME', ''):
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_var('DATABASE_NAME', ''),
        'USER': get_env_var('DATABASE_USER', ''),
        'PASSWORD': get_env_var('DATABASE_PASSWORD', ''),
        'HOST': get_env_var('DATABASE_HOST', ''),
        'PORT': get_env_var('DATABASE_PORT', ''),
        }
    }
else:
   DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# When test, use sqlute as test DB
if sys.argv[1] == 'test':
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# more details can be found here http://whitenoise.evans.io/en/stable/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# More details can be found here: https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
AWS_ACCESS_KEY_ID = get_env_var("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = get_env_var("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = get_env_var("AWS_STORAGE_BUCKET_NAME", "")
AWS_STORAGE_REGION = get_env_var("AWS_STORAGE_REGION", "")

IS_AWS_S3 = (
    AWS_ACCESS_KEY_ID and
    AWS_SECRET_ACCESS_KEY and
    AWS_STORAGE_BUCKET_NAME and
    AWS_STORAGE_REGION
)

if IS_AWS_S3:
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_CUSTOM_DOMAIN = get_env_var("AWS_S3_CUSTOM_DOMAIN", "")
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_DEFAULT_ACL = get_env_var("AWS_DEFAULT_ACL", "public-read")
    AWS_LOCATION = "media"
    AWS_AUTO_CREATE_BUCKET = get_env_var("AWS_AUTO_CREATE_BUCKET", True, var_type=bool)
    DEFAULT_FILE_STORAGE = get_env_var(
        "DEFAULT_FILE_STORAGE", "nxtbn.users.storages.NxtbnS3Storage"
    )


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# allauth config
ACCOUNT_EMAIL_VERIFICATION =  get_env_var("ACCOUNT_EMAIL_VERIFICATION", "optional")
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_UNIQUE_EMAIL = True
LOGIN_REDIRECT_URL = "account_profiles"

ACCOUNT_ADAPTER = "nxtbn.users.auth_adapters.CustomAccountAdapter"
SOCIALACCOUNT_ADAPTER = "nxtbn.users.auth_adapters.CustomSocialAccountAdapter"

ACCOUNT_FORMS = { # Allauth Server-side signup rendered signup
    'signup': 'nxtbn.users.forms.AllauthSignupForm',
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'nxtbn.users.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

if DEVELOPMENT_SERVER:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append(
        'nxtbn.users.authentication.CsrfExemptSessionAuthentication' # WARNING: Not Secure
    )


AUTH_USER_MODEL = "users.User" 
  
EMAIL_HOST = get_env_var("EMAIL_HOST", "")
EMAIL_HOST_USER =get_env_var("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = get_env_var("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT =  get_env_var("EMAIL_PORT", '')
EMAIL_USE_TLS = get_env_var("EMAIL_USE_TLS", False, var_type=bool)
DEFAULT_FROM_EMAIL = get_env_var("DEFAULT_FROM_EMAIL", "")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

IS_SMTP = (
    EMAIL_HOST and EMAIL_PORT
)

if IS_SMTP:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"



SWAGGER_SETTINGS = { # "Token <YOUR TOKEN>""
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization' # 'rest_framework.authentication.TokenAuthentication',
        }
    },
}



CELERY_BROKER_URL = get_env_var("REDIS_URL", "redis://redis:6379/1")
CELERY_RESULT_BACKEND = get_env_var("REDIS_URL", "redis://redis:6379/1") 
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# ============================
# NXTBN Specific Configuration
# ============================

PLUGIN_BASE_DIR = 'nxtbn.plugins.sources'

NXTBN_JWT_SETTINGS = {
    'SECRET_KEY': get_env_var("JWT_SECRET_KEY", SECRET_KEY), # default django's secret key
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_EXPIRATION_SECONDS': timedelta(hours=1),  # Default to 1 hour
    'REFRESH_TOKEN_EXPIRATION_SECONDS': timedelta(days=1),  # 1 day for refresh token
}


# Currency Configuration
BASE_CURRENCY = get_env_var("BASE_CURRENCY", default="USD")
ALLOWED_CURRENCIES = get_env_var("ALLOWED_CURRENCIES", default=[], var_type=list)
IS_MULTI_CURRENCY = get_env_var("IS_MULTI_CURRENCY", default=False, var_type=bool)
