from django.utils import timezone

from auction.celery import app
from .models import Auction, AuctionStatusChoice, AuctionTypeChoice


@app.task
def start_auctions():
    queryset = Auction.objects.filter(
        opening_date__lte=timezone.now(),
        status=AuctionStatusChoice.PENDING
    )
    # queryset = Auction.objects.filter(
    #     opening_date__lte=timezone.now(),
    #     status=AuctionStatusChoice.PENDING
    # ).update(status=AuctionStatusChoice.IN_PROGRESS)
    # queryset.filter(type=AuctionTypeChoice.DUTCH)
    for i in queryset:
        print(i)
        # start_dutch_auction?

@app.task
def close_auctions():
    queryset = Auction.objects.filter(
        closing_date__gte=timezone.now(),
        status=AuctionStatusChoice.IN_PROGRESS
    )
    for i in queryset:
        #do_smth
        pass