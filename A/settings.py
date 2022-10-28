"""
Django settings for A project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from A.local_settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local apps
    'accounts.apps.AccountsConfig',
    'core.apps.CoreConfig',
    'panel.apps.PanelConfig',
    'movie.apps.MovieConfig',
    'finance.apps.FinanceConfig',
    'wallet.apps.WalletConfig',
    'api.apps.ApiConfig',
    # third party apps
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'A.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'A.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if DEBUG:
    DATABASES = {
        'default': {},
        'main_db': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'main_db.sqlite3',
        },
        'secondary_db': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'secondary_db.sqlite3',
        }
    }

else:
    DATABASES = {
        'default': {},
        'mian_db': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': MAIN_DB_NAME,
            'USER': MAIN_DB_USER,
            'PASSWORD': MAIN_DB_PASS,
            'HOST': MAIN_DB_HOST,
            'PORT': MAIN_DB_PORT
        },
        'secondary_db': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': SEC_DB_NAME,
            'USER': SEC_DB_USER,
            'PASSWORD': SEC_DB_PASS,
            'HOST': SEC_DB_HOST,
            'PORT': SEC_DB_PORT
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (BASE_DIR / 'assets',)

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Session backend
SESSION_ENGINE = "django.contrib.sessions.backends.cache"


AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authenticate.UsernameAuthBackend',
]


# Social Auth
SOCIAL_AUTH_JSONFIELD_ENABLED = True

DATABASE_ROUTERS = ['db_routers.routers.MainRouter', 'db_routers.routers.SecondaryRouter']
