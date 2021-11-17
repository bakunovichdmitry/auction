from django.urls import path

from . import consumers

ws_urlpatterns = [
    path('ws/auctions/<uuid:unique_id>', consumers.AuctionConsumer.as_asgi()),
]