from .settings import *

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    get_random_secret_key()
)

ALLOWED_HOSTS = (
    'itechart-auction.herokuapp.com',
)

# MEDIA
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# EMAIL

EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')


# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
]
