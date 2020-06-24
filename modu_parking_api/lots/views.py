from rest_framework import viewsets
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
