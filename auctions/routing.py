from django.urls import path

from . import consumers

ws_urlpatterns = [
    path('ws/auctions/<uuid:id>', consumers.AuctionConsumer.as_asgi()),
]
