from rest_framework import serializers

from .models import Auction, AuctionHistory


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'


class AuctionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionHistory
        fields = '__all__'
