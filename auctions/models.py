import uuid

from django.contrib.auth.models import User
from django.db import models

from .emails import send_rejected_mail, send_sold_mail
from .utils import BaseEnumChoice
from .tasks import work_with_auction

class AuctionStatusChoice(BaseEnumChoice):
    PENDING = 0
    IN_PROGRESS = 1
    CLOSED = 2


class AuctionTypeChoice(BaseEnumChoice):
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
    step = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=None,
    )
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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def buy_item_now(self, user):
        self.status = AuctionStatusChoice.CLOSED
        self.current_price = self.buy_now_price
        self.save(
            update_fields=(
                'status',
                'current_price',
                'updated',
            )
        )
        send_sold_mail.delay(user)

    def make_offer(self, raise_price, user):
        if self.type == AuctionTypeChoice.ENGLISH.value and raise_price < self.step:
            raise ValueError
        self.current_price += raise_price


        # previous_offer_user_mail = self.history.last().user.email if self.history.last() else None

        self.create_history(user)
        self.save(
            update_fields=(
                'current_price',
                'updated',
            )
        )

        if self.type == AuctionTypeChoice.ENGLISH.value:
            work_with_auction.apply_async(
                [self.unique_id, user.id],
                countdown=5
            )
            pass
        # if previous_offer_user_mail:
        #     send_rejected_mail.delay(
        #         previous_offer_user_mail
        #     )

    def update_price(self):
        self.current_price -= self.step
        if self.current_price < self.end_price:
            self.status = AuctionStatusChoice.CLOSED
            raise ValueError
        self.save(
            update_fields=(
                'current_price',
                'updated',
            )
        )

    def create_history(self, user):
        AuctionHistory.objects.create(
            new_price=self.current_price,
            auction=self,
            user=user
        )


class AuctionHistory(models.Model):
    new_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    created = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(
        'auctions.Auction',
        on_delete=models.CASCADE,
        related_name='history'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
