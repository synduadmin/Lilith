"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import sys
import ssl

import dj_database_url

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-qkgnrai@@lsq6s!&i$wt)!gbt1i56#aht41f18@_b(h$=gjx@s"


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "syndu.com",
    "www.syndu.com",
    "139.59.53.236",
    "68.183.80.204",
]


# Application definition

INSTALLED_APPS = [
    "channels",
    "daphne",
    "chat_asgi",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_hosts",
    "crispy_forms",
    "crispy_bootstrap5", # add this
    "django_bootstrap5",
    "django_extensions",
    # 3rd party
    "allauth",  # new
    "allauth.account",  # new
    "allauth.socialaccount",  # new
    "sass_processor",
    "core",
    "crown",
    "chatbot",
    "pages",
    "todo_app",
    "logger",
    "rest_framework",
    "simple_history",
    "blog",
    "django_summernote",
    "panels",
    "google_analytics",
    "files_core",
    "studio",
    "leads",
]

GOOGLE_ANALYTICS = {
    "client_id": "G-268C1PX10W",
}

AUTH_USER_MODEL = "auth.User"  # new
CSRF_COOKIE_DOMAIN = ".syndu.com"

CSRF_TRUSTED_ORIGINS = [
    "http://syndu.com",
    "https://syndu.com",
    "http://www.syndu.com",
    "http://www.syndu.com",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_hosts.middleware.HostsRequestMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]
# settings.py
LOGIN_REDIRECT_URL = "chatbot:chatbot"
LOGIN_URL = "/accounts/login/"

ROOT_URLCONF = "base.urls"
ROOT_HOSTCONF = "base.hosts"
DEFAULT_HOST = "www"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"),
                 os.path.join(BASE_DIR, 'crown' , 'templates')],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
                "django.template.context_processors.media",

            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "libraries": {
                "forms": "django.template.defaulttags",  # add this line
            },
        },
    },
]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Jerusalem'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATIC_URL = "static/"
STATIC_ROOTx = os.path.join(BASE_DIR, STATIC_URL)
STATIC_ROOT = os.path.join(BASE_DIR, "assets/")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, STATIC_URL),
    os.path.join(STATIC_ROOTx, "css/"),
    os.path.join(STATIC_ROOTx, "js/"),
    os.path.join(STATIC_ROOTx, "img/"),
)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

SASS_PROCESSOR_INCLUDE_DIRS = []
SASS_PROCESSOR_AUTO_INCLUDE = False
SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r"^.+\.scss$"
SASS_PRECISION = 8
SASS_OUTPUT_STYLE = "compact"

# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

# Set email as the primary authentication detail
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True


ACCOUNT_FORMS = {
    "login": "base.forms.CustomLoginForm",
}

# config/settings.py
LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
}


WSGI_APPLICATION = "base.wsgi.application"

# mysite/settings.py

# Uvicorn
ASGI_APPLICATION = "base.asgi.application"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
# we wait a bit with the redis :-)

if ENVIRONMENT == "development":

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("localhost", 6379)],
            },
        },
    }

    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_DOMAIN = "127.0.0.1"

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django.db.backends": {
                "level": "WARNING",
                "handlers": ["console"],
            },
            "chat_asgi": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
        },
    }
else:  # production
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
    
    INSTALLED_APPS.append('storages')

    DO_SPACES_ACCESS_KEY = os.environ.get("DO_SPACES_ACCESS_KEY")
    DO_SPACES_SECRET_KEY = os.environ.get("DO_SPACES_SECRET_KEY")
    DO_SPACES_SPACE_NAME = os.environ.get("DO_SPACES_SPACE_NAME")
    DO_SPACES_SPACE_REGION = os.environ.get("DO_SPACES_SPACE_REGION")
    AWS_LOCATION= 'media'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = DO_SPACES_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = DO_SPACES_SECRET_KEY
    AWS_STORAGE_BUCKET_NAME = DO_SPACES_SPACE_NAME
    AWS_S3_REGION_NAME = DO_SPACES_SPACE_REGION
    AWS_S3_ENDPOINT_URL = f"https://{DO_SPACES_SPACE_REGION}.digitaloceanspaces.com"
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = 'public-read'
    MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "/home/syndu/logs/django.log",
                "maxBytes": 1024 * 1024 * 5,  # 5 MB
                "backupCount": 5,
                "formatter": "verbose",
            },
        },
        "formatters": {
            "verbose": {"format": "%(asctime)s %(levelname)s [%(module)s] %(message)s"},
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "INFO",
            },
            "django.db.backends": {
                "level": "WARNING",
                "handlers": ["console", "file"],
            },
            "chat_asgi": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
            },
        },
    }

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    ssl_context = ssl.SSLContext()
    ssl_context.check_hostname = False

    ssl_host_str = f"rediss://default:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
    do_redis_ssl_host = {
        "address": ssl_host_str,
    }

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [
                    (
                        "rediss://default:AVNS_T0NVp7SeCDDQC1X9DcE@db-redis-blr1-92931-do-user-12825119-0.b.db.ondigitalocean.com:25061"
                    )
                ],
            },
        },
    }
