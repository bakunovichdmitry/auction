from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework import pagination
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import LotSerializer
from .models import Lot


class LotListView(generics.ListAPIView):
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (AllowAny,)

    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    ordering_fields = (
        'auction__closing_date',
        'auction__current_price',
    )
    filterset_fields = [
        'auction__status',
        'auction__option',
    ]
