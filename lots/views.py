from rest_framework import generics
from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
from rest_framework import filters

from .serializers import LotSerializer
from .models import Lot


class LotListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    filter_backends = (
        filters.OrderingFilter,
    )
    ordering_fields = (
        'auction__closing_date',
        'auction__end_price'
    )
    # pagination_class =

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)
