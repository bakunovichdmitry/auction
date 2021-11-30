import uuid

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.utils import timezone

from .tasks import send_reject_email, send_sale_email
from .utils import BaseEnumChoice


class AuctionStatusChoice(BaseEnumChoice):
    PENDING = 0
    IN_PROGRESS = 1
    CLOSED = 2


class AuctionTypeChoice(BaseEnumChoice):
    DUTCH = 0
    ENGLISH = 1


class Auction(models.Model):
    DELAY_AUCTION_TIME = timezone.timedelta(minutes=10)

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
    def buy_item_now(self):
        if self.status == AuctionStatusChoice.CLOSED.value:
            raise ValueError

        if self.current_price > self.buy_item_now:
            raise ValueError

        self.current_price = self.buy_now_price
        self.close()

        self.save(
            update_fields=(
                'status',
                'current_price',
                'updated',
            )
        )

    @transaction.atomic
    def make_offer(self, raise_price, user):
        if self.type != AuctionTypeChoice.ENGLISH.value and self.status == AuctionStatusChoice.CLOSED.value:
            raise ValueError

        self.closing_date = max(
            self.closing_date,
            timezone.now() + self.DELAY_AUCTION_TIME
        )
        self.current_price += raise_price

        previous_offer = self.history.last()
        print(previous_offer.user.email)
        if previous_offer:
            transaction.on_commit(
                lambda: send_reject_email.delay(
                    previous_offer.user.email
                )
            )

        self.create_history(user)

        self.save(
            update_fields=(
                'closing_date',
                'current_price',
                'updated',
            )
        )

    @transaction.atomic
    def update_dutch_price(self):
        if self.type:
            raise ValueError
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
    def close(self, user=None):
        self.status = AuctionStatusChoice.CLOSED.value
        # user_email = self.history.last()
        # if last_offer or user:
        #     transaction.on_commit(
        #         lambda: send_sale_email(
        #             last_offer.user.email
        #         )
        #     )

        self.save(
            update_fields=(
                'status',
                'updated',
            )
        )

    def realtime_update(self):
        from .serializers import AuctionSerializer

        channel_layer = get_channel_layer()
        group_name = 'auction_%s' % self.unique_id
        serializer = AuctionSerializer(self)
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_changed_data',
                'data': serializer.data
            }
        )

    def create_history(self, user):
        return AuctionHistory.objects.create(
            new_price=self.current_price,
            auction=self,
            user=user
        )

    def save(self, *args, **kwargs):
        if self.current_price is None:
            self.current_price = self.start_price
        super(Auction, self).save(*args, **kwargs)


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
