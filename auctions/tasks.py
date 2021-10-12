from datetime import timedelta

from celery.schedules import crontab
from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.utils import timezone

from auction.celery import app
from .models import Auction, AuctionStatusChoice, AuctionTypeChoice

@app.task
def start_auctions():
    auctions = Auction.objects.filter(
        opening_date__lte=timezone.now(),
        status=AuctionStatusChoice.PENDING
    )
    auctions.update(status=AuctionStatusChoice.IN_PROGRESS)
    for auction in auctions:
        work_with_auction(auction.unique_id)

@app.task
def work_with_auction(auction_uuid):
    auction = Auction.objects.get(pk=auction_uuid)
    if auction.status == AuctionStatusChoice.IN_PROGRESS.value:
        if timezone.now() >= auction.closing_date:
            auction.status = AuctionStatusChoice.CLOSED
            if auction.type == AuctionTypeChoice.ENGLISH.value:
                last_offer_user_mail = auction.history.last().user.email
                send_mail.delay(
                    'lot was sold',
                    'u bought the item',
                    last_offer_user_mail
                )
            return auction.save()
        print(True)
        if auction.type == AuctionTypeChoice.ENGLISH.value:
            pass
            # work_with_auction.apply_async(
            #     (auction_uuid,),
            #     countdown=0
            # )
        if auction.type == AuctionTypeChoice.DUTCH.value:
            auction.current_price -= auction.step
            if auction.current_price < auction.end_price:
                auction.status = AuctionStatusChoice.CLOSED
                return auction.save()
            auction.update_price()
            work_with_auction.apply_async(
                [auction_uuid],
                countdown=auction.frequency
            )

# @app.task
# def update_price(auction_uuid):
#     auction = Auction.objects.get(auction_uuid)
#     try:
#         auction.update_price()
#         # update_price.apply_async(
#         #     args=auction_uuid,
#         #     countdown=auction.frequency
#         # )
#     except ValueError:
#         pass

@app.task
def send_mail(subject, message, user_mail):
    django_send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_mail]
    )

