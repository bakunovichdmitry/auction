from django.shortcuts import render
from rest_framework import pagination, generics
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Auction, AuctionHistory
from .serializers import AuctionSerializer, AuctionHistorySerializer, MakeOfferSerializer


class BuyItNowView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, unique_id):
        auction = get_object_or_404(
            Auction,
            pk=unique_id
        )
        auction.buy_item_now(
            request.user
        )
        serializer = AuctionSerializer(auction)
        return Response(serializer.data)


class MakeOfferView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, unique_id):
        auction = get_object_or_404(
            Auction,
            pk=unique_id
        )
        serializer = MakeOfferSerializer(
            data=request.data,
            context={
                'min_rate': auction.step
            }
        )
        if serializer.is_valid():
            auction.make_offer(
                raise_price=request.data.get('raise_price'),
                user=request.user
            )
            return Response(serializer.data)
        return Response(serializer.errors)


class AuctionHistoryView(generics.ListAPIView):
    queryset = AuctionHistory.objects.select_related('auction', 'user').order_by('-created').all()
    serializer_class = AuctionHistorySerializer
    pagination_class = pagination.LimitOffsetPagination
