from django.utils import timezone

from auction.celery import app
from .emails import _send_reject_email, _send_sale_email


@app.task
def start_auctions():
    from .models import Auction, AuctionStatusChoice

    auctions_unique_id = list(
        Auction.objects.filter(
            opening_date__lte=timezone.now(),
            status=AuctionStatusChoice.PENDING.value
        ).values_list('unique_id', 'closing_date')
    )
    auctions = Auction.objects.filter(
        opening_date__lte=timezone.now(),
        status=AuctionStatusChoice.PENDING.value
    )
    auctions.update(status=AuctionStatusChoice.IN_PROGRESS.value)
    for unique_id, closing_date in auctions_unique_id:
        process_auction.delay(unique_id)
        delay_close_auction.apply_async(
            [unique_id],
            eta=closing_date
        )

@app.task
def process_auction(auction_uuid, user_id=None):
    from .models import Auction, AuctionStatusChoice, AuctionTypeChoice
    try:
        auction = Auction.objects.get(
            pk=auction_uuid,
            status=AuctionStatusChoice.IN_PROGRESS.value
        )
    except Auction.DoesNotExist:
        return

    if auction.type == AuctionTypeChoice.ENGLISH.value:
        work_with_english_auction(auction, user_id)
    elif auction.type == AuctionTypeChoice.DUTCH.value:
        work_with_dutch_auction(auction)


@app.task
def work_with_dutch_auction(auction):
    if (auction.current_price - auction.step) < auction.end_price:
        auction.close()
        return

    auction.update_price()
    process_auction.apply_async(
        [auction.unique_id],
        countdown=auction.frequency
    )


@app.task
def work_with_english_auction(auction, user_id=None):
    if not (auction.history.last() and user_id == auction.history.last().user_id):
        return
    auction.close()


@app.task
def delay_close_auction(auction_uuid):
    from .models import Auction, AuctionStatusChoice
    try:
        auction = Auction.objects.get(pk=auction_uuid, status=AuctionStatusChoice.IN_PROGRESS.value)
        auction.close()
    except Auction.DoesNotExist:
        return


@app.task
def send_reject_email(user_email):
    _send_reject_email(user_email)


@app.task
def send_sale_email(user_email):
    _send_sale_email(user_email)
