from enum import Enum

from django.db import models


class BaseChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class AuctionStatusChoice(BaseChoiceEnum):
    PENDING = 0
    IN_PROGRESS = 1
    CLOSED = 2


class AuctionTypeChoice(BaseChoiceEnum):
    DUTCH = 0
    ENGLISH = 1


class Auction(models.Model):
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
        choices=AuctionStatusChoice.choices(),
        default=AuctionStatusChoice.PENDING,
    )
    type = models.IntegerField(
        choices=AuctionTypeChoice.choices(),
    )
    buy_now_price = models.DecimalField(
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
