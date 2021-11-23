from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Auction, AuctionHistory


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'


class AuctionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionHistory
        fields = '__all__'


class MakeOfferSerializer(serializers.Serializer):
    raise_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def validate_raise_price(self, raise_price):
        if raise_price < self.context.get('min_rate'):
            raise ValidationError('less then minimal rate')
        return raise_price
