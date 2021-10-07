from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from auction.celery import app
# from .models import Auction, AuctionStatusChoice, AuctionTypeChoice
#
#
# @app.task
# def start_auctions():
#     auctions = Auction.objects.filter(
#         opening_date__lte=timezone.now(),
#         status=AuctionStatusChoice.PENDING
#     )
#     for auction in auctions:
#         work_with_auction(auction)
#
# def work_with_auction(auction):
#     if timezone.now() >= auction.closing_date:
#         auction.status = AuctionStatusChoice.CLOSED
#         if auction.type == AuctionTypeChoice.ENGLISH:
#             #send_mail()
#             pass
#         if auction.type == AuctionTypeChoice.DUTCH:
#             update_price.apply_async(
#                 args=auction.unique_id,
#             )
#
# @app.task
# def update_price(auction_uuid):
#     pass
#
@app.task
def send_reject_mail(user_mail):
    send_mail(
        'your offer was rejected',
        'offer_template',
        settings.EMAIL_HOST_USER,
        [user_mail]
    )
