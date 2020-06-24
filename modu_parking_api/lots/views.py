from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from lots.filters import OrderedDistanceToPointFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from lots.models import Lot
from lots.serializers import LotsSerializer, OrderSerializer, MapSerializer


class LotsViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotsSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action in ('distance_odr', 'price_odr'):
            return OrderSerializer(*args, **kwargs)
        elif self.action == 'map':
            return MapSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False)
    def map(self, request, *args, **kwargs):

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)















    # @action(detail=False)
    # def price_odr(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(self.queryset, many=True)
    #     return Response(serializer.data)
    # @action(detail=False)
    # def distance_odr(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(self.queryset, many=True)
    #     return Response(serializer.data)
