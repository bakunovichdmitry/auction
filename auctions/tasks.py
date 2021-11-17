from django.utils import timezone
from django.conf import settings

from auction.celery import app
from .emails import _send_reject_email, _send_sale_email


@app.task
def start_auctions():
    from .models import Auction, AuctionStatusChoice

    auctions_unique_id = list(
        Auction.objects.filter(
            opening_date__lte=timezone.now(),
            status=AuctionStatusChoice.PENDING.value
        ).values_list('unique_id', flat=True)
    )
    auctions = Auction.objects.filter(
        opening_date__lte=timezone.now(),
        status=AuctionStatusChoice.PENDING.value
    )
    auctions.update(status=AuctionStatusChoice.IN_PROGRESS.value)
    for unique_id in auctions_unique_id:
        process_auction.delay(unique_id)


@app.task
def process_auction(auction_uuid):
    from .models import Auction, AuctionStatusChoice, AuctionTypeChoice
    try:
        auction = Auction.objects.get(
            pk=auction_uuid,
            status=AuctionStatusChoice.IN_PROGRESS.value
        )
    except Auction.DoesNotExist:
        return

    if auction.type == AuctionTypeChoice.ENGLISH.value:
        process_english_auction(auction)
    elif auction.type == AuctionTypeChoice.DUTCH.value:
        process_dutch_auction(auction)


def process_dutch_auction(auction):
    if (auction.current_price - auction.step) < auction.end_price:
        auction.close()
        return

    auction.update_dutch_price()
    process_auction.apply_async(
        [auction.unique_id],
        countdown=auction.frequency
    )


def process_english_auction(auction):
    now = timezone.now()
    if now - settings.ENGLISH_AUCTION_CLOSE_TIMEDELTA <= auction.closing_date <= now + settings.ENGLISH_AUCTION_CLOSE_TIMEDELTA:
        auction.close()
        return

    process_auction.apply_async(
        [auction.unique_id],
        eta=auction.closing_date
    )


@app.task
def send_reject_email(user_email):
    _send_reject_email(user_email)


@app.task
def send_sale_email(user_email):
    _send_sale_email(user_email)
