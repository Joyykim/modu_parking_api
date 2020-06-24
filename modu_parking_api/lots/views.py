from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# from lots.filters import OrderedDistanceToPointFilter
from lots.models import Lot
from lots.serializers import LotsSerializer
from users.models import User
import math


class LotsViewSet(viewsets.ModelViewSet):
    """
    사용자에게 주차장들을 보여줌
    1. order : 정렬해서 목록으로
    2. map : 일정범위만큼 잘라서

    order :


    """
    queryset = Lot.objects.all()
    serializer_class = LotsSerializer
    # OrderedDistanceToPointFilter()

    # def filter_queryset(self, queryset):
    #     if self.request.data['order'] == 'price':
    #         self.queryset = Lot.objects.filter().order_by('basic_rate')
    #     elif self.request.data['order'] == 'distance':
    #
    #         distance = self.request.data.pop('zoom_level')  # 줌레벨
    #         lat = self.request.data['lat']
    #         lon = self.request.data['lon']
    #
    #         ref_location = Point(lon, lat)
    #         queryset = Lot.objects.filter(
    #             location__distance_lte=(
    #                 ref_location,
    #                 D(m=distance)
    #             )
    #         ).distance(ref_location).order_by('distance')
    #         return queryset
    #
    #     return super().filter_queryset(queryset)

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

    return d
