from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from parkings import permissions
from parkings.models import Parking
from parkings.serializers import ParkingSerializer, ParkingListSerializer


class ParkingViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.CreateOwnTotalFee, IsAuthenticated)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.parking_time += float(request.data['additional_time'])
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ParkingListSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy', 'list', 'perform_create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


"""
POST /parkings/	
: 주차 이벤트 생성(주인의 사용내역만)

GET /parkings/
: 유저의 주차 내역 목록(총비용, 주차장 정보)
: 과거 주차내역 list으로 시간, 가격, 주차장이름 나열

GET /parkings/id
: 주차내역 상세

PUT /parkings/id/
: 주차시간을 추가(추가결제) total_fee 계산할 자료 제공
"""
