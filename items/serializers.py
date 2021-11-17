from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    # photo = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'

    # def get_photo(self, obj):
    #     if obj.photo:
    #         return 'http://localhost:8000' + obj.photo.url
