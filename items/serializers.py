from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'photo',
            'title',
            'description',
        )
        read_only_fields = (
            'id',
        )
