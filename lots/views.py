from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import filters
from rest_framework import pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LotSerializer
from .models import Lot


class LotListView(generics.ListAPIView):
    queryset = Lot.objects.select_related('auction', 'item').all()
    serializer_class = LotSerializer
    pagination_class = pagination.PageNumberPagination
    page_size = 2

    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    ordering_fields = (
        'auction__closing_date',
        'auction__current_price',
    )
    filterset_fields = (
        'auction__status',
        'auction__type',
    )


class LotDetailView(APIView):
    def get(self, request, unique_id):
        lot = get_object_or_404(
            Lot.objects.select_related('auction', 'item'),
            pk=unique_id
        )
        serializer = LotSerializer(lot)
        return Response(serializer.data)
