from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
    serializer = ParkingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.CreateOwnTotalFee, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in "list":
            serializer_class = ParkingListSerializer
        else:
            serializer_class = ParkingSerializer
        return serializer_class

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy', 'list', 'perform_create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


"""
POST /parkings/	
: 주차 이벤트 생성(주인의 사용내역만)
"""
