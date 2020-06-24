import math
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from lots.filters import OrderedDistanceToPointFilter
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

    @action(detail=False)
    def order(self, request, *args, **kwargs):
        # page = self.paginate_queryset(queryset)
        # if page is not None:        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def order_distance(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        pass


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

