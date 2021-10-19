from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from auction.celery import app
from .emails import send_sold_mail


@app.task
def start_auctions():
    from .models import Auction, AuctionStatusChoice

    auctions = Auction.objects.filter(
        opening_date__lte=timezone.now(),
        status=AuctionStatusChoice.PENDING
    )
    auctions.update(status=AuctionStatusChoice.IN_PROGRESS)
    for auction in auctions:
        work_with_auction(auction.unique_id)


@app.task
def work_with_auction(auction_uuid, user_id=None):
    from .models import Auction, AuctionStatusChoice, AuctionTypeChoice
    try:
        auction = Auction.objects.get(pk=auction_uuid, status=AuctionStatusChoice.IN_PROGRESS.value)
    except Auction.DoesNotExist:
        return

    if timezone.now() >= auction.closing_date:
        close_auction(auction)
        return

    if auction.type == AuctionTypeChoice.ENGLISH.value:
        work_with_english_auction(auction, user_id)
        return
    work_with_dutch_auction(auction)


@app.task
def work_with_dutch_auction(auction):
    auction.current_price -= auction.step
    if auction.current_price < auction.end_price:
        close_auction(auction)

    auction.update_price()
    work_with_auction.apply_async(
        [auction.unique_id],
        countdown=auction.frequency
    )


@app.task
def work_with_english_auction(auction, user_id):
    if not user_id:
        work_with_auction.apply_async(
            [auction.unique_id],
            eta=auction.closing_date
        )
        return
    try:
        user = User.objects.get(pk=user_id)
        if auction.history.last() and user == auction.history.last().user:
            with transaction.atomic():
                close_auction(auction)
                transaction.on_commit(
                    send_sold_mail.delay(user.email)
                )
    except User.DoesNotExist:
        pass


def close_auction(auction):
    from .models import AuctionStatusChoice
    auction.status = AuctionStatusChoice.CLOSED.value
    auction.save()

# TODO: replace close auction method
