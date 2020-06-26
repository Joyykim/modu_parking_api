from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from lots.models import Lot
from parkings.models import Parking
from parkings.permissions import IsOwner
from parkings.serializers import ParkingSerializer, ParkingListSerializer


class ParkingViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = (IsOwner,)

    def get_serializer_class(self):
        if self.action == "list":
            return ParkingListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        POST /parkings/
        주차 결제를 함으로서 사용자의 포인트 차감

        총비용 = 주차시간 중 처음 1시간만 기본요금, 나머지 시간은 추가요금으로 계산
        """
        lot = Lot.objects.get(id=request.data['lot'])
        parking_time = float(request.data['parking_time'])
        additional_rate = ((parking_time - 1) * 2) * lot.additional_rate  # 추가비용
        total_fee = (lot.basic_rate + additional_rate)  # 총비용

        # 포인트 부족시 거부
        if request.user.points < total_fee:
            return Response({'refuse': '보유한 포인트가 부족합니다'})

        # 사용자 포인트 차감
        request.user.points -= total_fee
        request.user.save()
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        GET /parkings/
        : 유저의 주차 내역 목록(총비용, 주차장 정보)
        : 과거 주차내역 list으로 시간, 가격, 주차장이름 나열
        """
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        PUT /parkings/id/
        사용자가 추가결제하여 주차시간 연장
        """
        instance = self.get_object()
        additional_time = float(request.data['additional_time'])
        lot = Lot.objects.get(id=instance.lot_id)
        additional_rate = (additional_time * 2) * lot.additional_rate

        # 포인트 부족시 거부
        if request.user.points < additional_rate:
            return Response({'refuse': '보유한 포인트가 부족합니다'})

        # 주차시간 연장, 사용자 포인트 차감
        instance.parking_time += additional_time
        request.user.points -= additional_rate

        request.user.save()
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
