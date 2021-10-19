from django.conf import settings
from django.core.mail import send_mail

from auction.celery import app


@app.task
def send_rejected_mail(user_mail):
    send_mail(
        'offer',
        'u office was rejected',
        settings.EMAIL_HOST_USER,
        [user_mail]
    )


@app.task
def send_sold_mail(user_mail):
    send_mail(
        'offer',
        'u offer was sell',
        settings.EMAIL_HOST_USER,
        [user_mail]
    )
