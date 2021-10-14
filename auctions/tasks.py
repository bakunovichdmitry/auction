from django.utils import timezone

from auction.celery import app
from .emails import send_sold_mail
from django.contrib.auth.models import User

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

def work_with_dutch_auction(auction):
    from .models import AuctionStatusChoice

    auction.current_price -= auction.step
    if auction.current_price < auction.end_price:
        auction.status = AuctionStatusChoice.CLOSED.value
        return auction.save()
    auction.update_price()
    work_with_auction.apply_async(
        [auction.unique_id],
        countdown=auction.frequency
    )


@app.task
def work_with_english_auction(auction, user_id):
    from .models import AuctionStatusChoice

    if not user_id:
        work_with_auction.apply_async(
            [auction.unique_id],
            eta=auction.closing_date
        )
        return

    user = User.objects.get(pk=user_id)

    if user == auction.history.last().user:
        auction.status = AuctionStatusChoice.CLOSED.value
        auction.save()
        send_sold_mail.delay(user.email)
        return


@app.task
def work_with_auction(auction_uuid, user_id=None):
    from .models import Auction, AuctionStatusChoice, AuctionTypeChoice
    try:
        auction = Auction.objects.get(pk=auction_uuid, status=AuctionStatusChoice.IN_PROGRESS.value)
    except Auction.DoesNotExist:
        return

    if timezone.now() >= auction.closing_date:
        auction.status = AuctionStatusChoice.CLOSED.value
        auction.save()
        return

    if auction.type == AuctionTypeChoice.ENGLISH.value:
        work_with_english_auction(auction, user_id)
    if auction.type == AuctionTypeChoice.DUTCH.value:
        work_with_dutch_auction(auction)

@app.task
def test_task():
    return True
