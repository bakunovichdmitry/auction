from django.db import models


class Lot(models.Model):
    item = models.ForeignKey(
        'items.Item',
        on_delete=models.CASCADE
    )
    auction = models.ForeignKey(
        'auctions.Auction',
        on_delete=models.CASCADE,
        null=True
    )
