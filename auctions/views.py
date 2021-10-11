from rest_framework import pagination, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Auction, AuctionHistory
from .serializers import AuctionSerializer, AuctionHistorySerializer


class BuyItNowView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, unique_id):
        auction = get_object_or_404(
            Auction,
            pk=unique_id
        )
        auction.buy_item_now()
        serializer = AuctionSerializer(auction)
        return Response(serializer.data)


class MakeOfferView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, unique_id, raise_price):
        auction = get_object_or_404(
            Auction,
            pk=unique_id
        )
        try:
            auction.make_offer(raise_price, request.user)
            return Response(
                {'detail': 'Your offer has been accepted'}
            )
        except ValueError:
            return Response(
                {'detail': 'Enter a valid price'}
            )


class AuctionHistoryView(generics.ListAPIView):
    queryset = AuctionHistory.objects.select_related('auction', 'user').order_by('-created').all()
    serializer_class = AuctionHistorySerializer
    pagination_class = pagination.LimitOffsetPagination
