import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .tasks import process_auction, send_reject_email, send_sale_email
from .utils import BaseEnumChoice
from django.db import transaction


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

    @transaction.atomic
    def buy_item_now(self, user):
        if self.status == AuctionStatusChoice.CLOSED.value:
            raise ValueError

        self.close(user)

        self.current_price = self.buy_now_price
        self.save(
            update_fields=(
                'status',
                'current_price',
                'updated',
            )
        )

    @transaction.atomic
    def make_offer(self, raise_price, user):
        if self.type != AuctionTypeChoice.ENGLISH.value and \
                raise_price < self.step and \
                self.status == AuctionStatusChoice.CLOSED.value:
            raise ValueError

        from datetime import timedelta
        self.closing_date = min(self.closing_date, timezone.now() + timedelta(seconds=5))
        self.current_price += raise_price

        # previous_offer_user_mail = self.history.last().user.email
        # if previous_offer_user_mail:
        #     transaction.on_commit(
        #         lambda: send_rejected_mail.delay(
        #             previous_offer_user_mail
        #         )
        #     )

        self.create_history(user)
        self.save(
            update_fields=(
                'closing_date',
                'current_price',
                'updated',
            )
        )

        transaction.on_commit(
            process_auction.apply_async(
                [self.unique_id],
                eta=self.closing_date
            )
        )


    @transaction.atomic
    #bid_step_decline
    def update_price(self):
        self.current_price -= self.step
        if self.current_price < self.end_price:
            raise ValueError
        
        self.save(
            update_fields=(
                'current_price',
                'updated',
            )
        )

    @transaction.atomic
    def close(self, user=None, send_mail=False):
        if self.status == AuctionStatusChoice.IN_PROGRESS.value:
            self.status = AuctionStatusChoice.CLOSED.value
            if send_mail and user:
                transaction.on_commit(
                    lambda: send_sale_email(user.email)
                )

            self.save(
                update_fields=(
                    'status',
                    'updated',
                )
            )

    def create_history(self, user):
        return AuctionHistory.objects.create(
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
