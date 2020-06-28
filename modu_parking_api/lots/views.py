from rest_framework import viewsets
from rest_framework.decorators import action
from lots.models import Lot
from lots.serializers import LotsSerializer, MapSerializer


class LotsViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotsSerializer

    def get_serializer_class(self):
        if self.action == 'map':
            return MapSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        data = self.request.GET
        if self.action == 'map':
            lat = float(data['lat'])
            lon = float(data['lon'])

            min_lat = lat - 0.009
            max_lat = lat + 0.009
            min_lon = lon - 0.015
            max_lon = lon + 0.015

            # 최소, 최대 위경도를 1km씩 설정해서 쿼리
            queryset = self.queryset.filter(latitude__gte=min_lat, latitude__lte=max_lat,
                                            longitude__gte=min_lon, longitude__lte=max_lon)
            return queryset
        return super().get_queryset()

    @action(detail=False)
    def map(self, request, *args, **kwargs):
        """
        사용자의 위치를 기준으로 일정 범위의 주차장 목록 반환
        """
        return super().list(request, *args, **kwargs)
