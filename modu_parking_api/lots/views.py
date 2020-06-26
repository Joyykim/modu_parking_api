from haversine import haversine
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from lots.models import Lot
from lots.serializers import LotsSerializer, OrderSerializer, MapSerializer


class LotsViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotsSerializer

    def get_serializer_class(self):
        if self.action in ('distance_odr', 'price_odr'):
            return OrderSerializer
        elif self.action == 'map':
            return MapSerializer
        return super().get_serializer_class()

    @action(detail=False)
    def map(self, request, *args, **kwargs):
        """
        사용자의 위치를 기준으로 일정 범위의 주차장 목록 반환
        """
        result = []
        data = request.GET  # request.GET : 사용자 위도, 경도, 줌레벨

        for lot in self.queryset:
            user_location = (float(data['latitude']), float(data['longitude']))
            lot_location = (lot.latitude, lot.longitude)
            distance = haversine(lot_location, user_location)

            if distance <= float(data['zoom_lv']):
                result.append(lot)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def price_odr(self, request, *args, **kwargs):
        """
        사용자의 위치를 기준으로 1km 이내의 주차장 목록 반환 - 가격순 정렬
        """
        user_location = (float(request.GET['latitude']), float(request.GET['longitude']))

        # 가격 정렬
        ordered_queryset = self.queryset.order_by('basic_rate')
        serializer = self.get_serializer(ordered_queryset, many=True)

        unfiltered_lots = list(serializer.data)  # ReturnList -> list 형변환

        # 거리 필터링
        filtered_lots = filter_by_distance(unfiltered_lots, user_location)
        return Response(filtered_lots)

    @action(detail=False)
    def distance_odr(self, request, *args, **kwargs):
        """
        사용자의 위치를 기준으로 1km 이내의 주차장 목록 반환 - 거리순 정렬
        """
        user_location = (float(request.GET['latitude']), float(request.GET['longitude']))

        serializer = self.get_serializer(self.queryset, many=True)

        # TODO extract method
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
            lot.distance = distance  # 정렬의 기준
            filtered_lots.append(lot)

    return filtered_lots


def get_distance(lot, user_location):
    lot_location = (lot['latitude'], lot['longitude'])
    distance = haversine(lot_location, user_location)
    return distance
