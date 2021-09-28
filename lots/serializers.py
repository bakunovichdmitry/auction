from rest_framework import serializers

from .models import Lot
from items.serializers import ItemSerializer
from auctions.serializers import AuctionSerializer


class LotSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    auction = AuctionSerializer()

    class Meta:
        model = Lot
        fields = (
            'item',
            'auction',
        )
