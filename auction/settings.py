import os
from pathlib import Path

import cloudinary
import cloudinary.api
import cloudinary.uploader
import dj_database_url
from django.utils import timezone

# from .setting_local import *

DEBUG = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

ALLOWED_HOSTS = ['*']

SECRET_KEY = '@w9*-uh-$h=6ynfr*)ccidcm(adt%*rl!!h*ggh-bb2uwa)cy-'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auction',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'db',
        'PORT': 5432,
    }
}

DATABASE_URL = os.environ.get('DATABASE_URL')
db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
# EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')
# EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
# EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'auctiondjango@gmail.com'
EMAIL_HOST_PASSWORD = 'AuctionDjango123'
EMAIL_PORT = 587


INSTALLED_APPS = [
    # Local Apps
    'items.apps.ItemsConfig',
    'auctions.apps.AuctionsConfig',
    'lots.apps.LotsConfig',
    'users.apps.UsersConfig',

    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'channels',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    # Django Middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Third-Party Middleware
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'auction.urls'

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

WSGI_APPLICATION = 'auction.wsgi.application'
ASGI_APPLICATION = "auction.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('HEROKU_REDIS_YELLOW_URL', 'redis://redis:6379')],
        },
    },
}

# Password validation

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

# Django REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Minsk'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# Celery

CELERY_BROKER_URL = os.environ.get('HEROKU_REDIS_YELLOW_URL', 'redis://redis:6379')
CELERY_RESULT_BACKEND = os.environ.get('HEROKU_REDIS_YELLOW_URL', 'redis://redis:6379')
CELERY_TIMEZONE = 'Europe/Minsk'

# CORS

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# ENGLISH AUCTION CONSTANTS

ENGLISH_AUCTION_CLOSE_TIMEDELTA = timezone.timedelta(seconds=20)

# LOGGING = {
#     'disable_existing_loggers': False,
#     'version': 1,
#     'handlers': {
#         'console': {
#             # logging handler that outputs log messages to terminal
#             'class': 'logging.StreamHandler',
#             'level': 'DEBUG', # message level to be written to console
#         },
#     },
#     'loggers': {
#         '': {
#             # this sets root level logger to log debug and higher level
#             # logs to console. All other loggers inherit settings from
#             # root level logger.
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False, # this tells logger to send logging message
#                                 # to its parent (will send if set to True)
#         },
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console', ],
#         },
#     },
# }
