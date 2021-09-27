from django.db import models


class AuctionCommon(models.Model):
    class Meta:
        abstract = True

    PENDING = 1
    IN_PROGRESS = 2
    CLOSED = 3
    AUCTION_STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (IN_PROGRESS, 'IN PROGRESS'),
        (CLOSED, 'CLOSED'),
    )

    start_price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    step = models.IntegerField()
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    status = models.IntegerField(
        choices=AUCTION_STATUS_CHOICES,
        default=PENDING,
    )


class EnglishAuction(AuctionCommon):
    buy_it_now = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )


class DutchAuction(AuctionCommon):
    end_price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    frequency = models.IntegerField()
