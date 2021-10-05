from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Auction
from .serializers import AuctionSerializer


class BuyItNowView(APIView):
    def post(self, request, unique_id):
        auction = get_object_or_404(
            Auction,
            pk=unique_id
        )
        auction.buy_item_now()
        serializer = AuctionSerializer(auction)
        return Response(serializer.data)


class MakeOfferView(APIView):
    def post(self, request, unique_id, raise_price):
        auction = get_object_or_404(
            Auction,
            pk=unique_id
        )
        if auction.make_offer(raise_price):
            return Response({'detail': 'ok'})
        return Response({'detail': 'error'})
