from django.conf import settings
from django.core.mail import send_mail


def _send_reject_email(email):
    send_mail(
        'offer',
        'u office was rejected',
        settings.EMAIL_HOST_USER,
        [email]
    )


def _send_sale_email(email):
    send_mail(
        'offer',
        'u offer was sell',
        settings.EMAIL_HOST_USER,
        [email]
    )
