from .settings import *

DEBUG = True
SECRET_KEY = get_random_secret_key()
ALLOWED_HOSTS = (
    '*',
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'auctiondjango@gmail.com'
EMAIL_HOST_PASSWORD = 'AuctionDjango123'
EMAIL_PORT = 587

# STATIC

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

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
