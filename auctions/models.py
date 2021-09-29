from django.db import models


class Auction(models.Model):

    PENDING = 0
    IN_PROGRESS = 1
    CLOSED = 2
    AUCTION_STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (IN_PROGRESS, 'IN PROGRESS'),
        (CLOSED, 'CLOSED'),
    )

    AUCTION_OPTION_CHOICES = (
        (0, 'DUTCH'),
        (1, 'ENGLISH'),

    )

    start_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=None,
    )
    step = models.IntegerField()
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    status = models.IntegerField(
        choices=AUCTION_STATUS_CHOICES,
        default=PENDING,
    )
    option = models.IntegerField(
        choices=AUCTION_OPTION_CHOICES,
    )
    buy_it_now = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    end_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    frequency = models.IntegerField(
        blank=True,
        null=True,
    )

    def is_english_auction(self):
        if self.AUCTION_OPTION_CHOICES:
            return True
        return False
