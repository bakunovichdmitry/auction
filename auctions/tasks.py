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
        status=AuctionStatusChoice.PENDING.value
    )
    auctions_unique_id = list(
        Auction.objects.filter(
            opening_date__lte=timezone.now(),
            status=AuctionStatusChoice.PENDING.value
        ).values_list('unique_id', flat=True)
    )
    auctions.update(status=AuctionStatusChoice.IN_PROGRESS.value)
    for unique_id in auctions_unique_id:
        work_with_auction.delay(unique_id)


@app.task
def work_with_auction(auction_uuid, user_id=None):
    from .models import Auction, AuctionStatusChoice, AuctionTypeChoice
    try:
        auction = Auction.objects.get(pk=auction_uuid, status=AuctionStatusChoice.IN_PROGRESS.value)
    except Auction.DoesNotExist:
        return

    if auction.type == AuctionTypeChoice.ENGLISH.value:
        work_with_english_auction(auction, user_id)
        return
    work_with_dutch_auction(auction)


@app.task
def work_with_dutch_auction(auction):
    if (auction.current_price - auction.step) < auction.end_price or timezone.now() >= auction.closing_date:
        auction.close()
        return
    auction.update_price()
    work_with_auction.apply_async(
        [auction.unique_id],
        countdown=auction.frequency
    )


@app.task
def work_with_english_auction(auction, user_id):
    if not user_id:
        # work_with_auction.apply_async(
        #     [auction.unique_id],
        #     eta=auction.closing_date
        # )
        close_auction.apply_async(
            [auction.unique_id],
            eta=auction.closing_date
        )
        return
    try:
        user = User.objects.get(pk=user_id)
        if auction.history.last() and user == auction.history.last().user:
            # ???
            # with transaction.atomic():
            auction.close()
            # transaction.on_commit(
            #     lambda: send_sold_mail.delay(user.email)
            # )
    except User.DoesNotExist:
        pass


@app.task
def close_auction(auction_uuid):
    from .models import Auction, AuctionStatusChoice
    try:
        auction = Auction.objects.get(pk=auction_uuid, status=AuctionStatusChoice.IN_PROGRESS.value)
        auction.close()
    except Auction.DoesNotExist:
        return
