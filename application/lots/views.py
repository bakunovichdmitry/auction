from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics

from .models import Lot
from .pagination import LotPagination
from .serializers import LotSerializer


class LotListView(generics.ListAPIView):
    queryset = Lot.objects.select_related('auction', 'item')
    serializer_class = LotSerializer
    pagination_class = LotPagination
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


class LotDetailView(generics.RetrieveAPIView):
    lookup_field = 'unique_id'
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
