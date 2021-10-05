import uuid

from django.db import models


class Lot(models.Model):
    unique_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    item = models.ForeignKey(
        'items.Item',
        on_delete=models.CASCADE,
        # related_name='item'
    )
    auction = models.ForeignKey(
        'auctions.Auction',
        on_delete=models.CASCADE,
        # related_name='lots'
    )


class LotHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)