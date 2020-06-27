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

    def get_queryset(self):
        if self.action == 'map':
            lat = float(data['latitude'])
            lon = float(data['longtitude'])
            min_lat = lat - 0.0000001
            max_lat = lat + 0.0000001

            # 모든 data를 확인 하지않고 filter 사용으로 쿼리 줄이기
            qs = self.queryset.filter(latitude__gte=min_lat, latitude__lte=max_lat)

            return qs

        return super().get_queryset()


    @action(detail=False)
    def map(self, request, *args, **kwargs):
        """
        사용자의 위치를 기준으로 일정 범위의 주차장 목록 반환
        """
        result = []
        data = request.GET  # request.GET : 사용자 위도, 경도, 줌레벨

        lat = float(data['latitude'])
        lon = float(data['longtitude'])
        min_lat = lat - 0.0000001
        max_lat = lat + 0.0000001

        # 모든 data를 확인 하지않고 filter 사용으로 쿼리 줄이기
        # get_queryst() override 해서 사용
        self.queryset.filter(latitude__gte=min_lat, latitude__lte=max_lat)

        for lot in self.queryset:
            user_location = (float(data['latitude']), float(data['longitude']))
            lot_location = (lot.latitude, lot.longitude)
            distance = haversine(lot_location, user_location)

            if distance <= float(data['zoom_lv']):
                result.append(lot)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)

    #  drf filterset 사용하면 ordering 구현 불필요
    # https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter
    # static 정보라서 ttl=60m 정도 설정하는게 좋음
    # 클라이언트에서 정렬 가능 하므로 API 필요 없어 보
    @action(detail=False)
    def price_odr(self, request, *args, **kwargs):
        """
        사용자의 위치를 기준으로 1km 이내의 주차장 목록 반환 - 가격순 정렬
        """
        user_location = (float(request.GET['latitude']), float(request.GET['longitude']))

        # 가격 정렬
        ordered_queryset = self.queryset.order_by('basic_rate')임
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


# lot.filter_by_distance() 추출 추천
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
