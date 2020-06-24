import math
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
    """
    사용자에게 주차장들을 보여줌
    1. order : 정렬해서 목록으로
    2. map : 일정범위만큼 잘라서
    order :
    """
    queryset = Lot.objects.all()
    serializer_class = LotsSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action in ('distance_odr', 'price_odr'):
            return OrderSerializer(*args, **kwargs)
        elif self.action == 'map':
            return MapSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    @action(detail=False)
    def price_odr(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


def distance(origin, destination, radius=1):
    lat1, lon1 = origin
    lat2, lon2 = destination

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

