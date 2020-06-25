import math

from haversine import haversine
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

    @action(detail=False)
    def map(self, request, *args, **kwargs):

        result = []
        for lot in self.queryset:
            data = request.GET
            if haversine((lot.latitude, lot.longitude), (float(data['latitude']), float(data['longitude']))) <= 2:
                result.append(lot)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def price_odr(self, request, *args, **kwargs):
        user_location = (float(request.GET['latitude']), float(request.GET['longitude']))

        ordered_queryset = self.queryset.order_by('basic_rate')
        serializer = self.get_serializer(ordered_queryset, many=True)

        unfiltered_lots = list(serializer.data)
        filtered_lots = filter_by_distance(unfiltered_lots, user_location)
        return Response(filtered_lots)

    @action(detail=False)
    def distance_odr(self, request, *args, **kwargs):
        user_location = (float(request.GET['latitude']), float(request.GET['longitude']))

        serializer = self.get_serializer(self.queryset, many=True)

        unfiltered_lots = list(serializer.data)
        filtered_lots = filter_by_distance(unfiltered_lots, user_location)
        # sorting lots with distance
        result = sorted(filtered_lots, key=lambda obj: obj.distance)
        return Response(result)


def filter_by_distance(unfiltered_lots, user_location):
    filtered_lots = []

    for lot in unfiltered_lots:
        # return distance between user and lot
        distance = get_distance(lot, user_location)

        if distance <= 1:
            lot.distance = distance
            filtered_lots.append(lot)

    return filtered_lots


def get_distance(lot, user_location):
    lot_location = (lot['latitude'], lot['longitude'])
    distance = haversine(lot_location, user_location)
    return distance
