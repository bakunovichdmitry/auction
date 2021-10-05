import uuid
from enum import IntEnum

from django.db import models


class BaseIntEnumChoice(IntEnum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class AuctionStatusChoice(BaseIntEnumChoice):
    PENDING = 0
    IN_PROGRESS = 1
    CLOSED = 2


class AuctionTypeChoice(BaseIntEnumChoice):
    DUTCH = 0
    ENGLISH = 1


class Auction(models.Model):
    unique_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
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
        choices=AuctionStatusChoice.choices(),
        default=AuctionStatusChoice.PENDING,
    )
    type = models.IntegerField(
        choices=AuctionTypeChoice.choices(),
        default=AuctionTypeChoice.ENGLISH,
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

    def buy_item_now(self):
        self.status = AuctionStatusChoice.CLOSED
        self.current_price = self.buy_now_price
        self.save()

    def make_offer(self, raise_price):
        # print(raise_price, self.step, self.status, self.type == AuctionTypeChoice.ENGLISH)
        if self.type == AuctionTypeChoice.ENGLISH and raise_price < self.step:
            return False
        self.current_price += raise_price
        self.save()
        return True
