from django.db import models


class Lot(models.Model):
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
