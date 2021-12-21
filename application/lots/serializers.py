from rest_framework import serializers

from .models import Lot
from items.serializers import ItemSerializer
from auctions.serializers import AuctionSerializer


class LotSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False)
    auction = AuctionSerializer(many=False)

    class Meta:
        model = Lot
        fields = (
            'unique_id',
            'item',
            'auction',
        )
