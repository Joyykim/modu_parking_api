from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import status, serializers, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

import parkings
# from parkings import models, permissions
from lots.models import Lot
from parkings import permissions
from parkings.models import Parking
from parkings.serializers import ParkingSerializer


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

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy', 'list', 'perform_create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    # def create(self, request, *args, **kwargs):
    def create(self, request, *args, **kwargs):
        """
        주인의 사용내용만으로 주차 이벤트 생성, 과거 주차내역 list로 시간, 가격, 주차장 이름
        REQ - start_time, parking_time, lot(foreign)
        RES - total_fee [0] , start_time[0], parking_time[0], lot(foreign)[0], end_time(계산해야함)
        """
        import datetime
        from datetime import timedelta
        parking_time = request.data.get('parking_time')  # 2.5 3
        lot_pk = request.data.get('lot')
        lot_ins = Lot.objects.get(pk=lot_pk)
        # lot_ins = Lot.objects.get(request.data.get('lot'))

        basic_hour = 1
        add_hour = parking_time - basic_hour
        # 주차 비용
        total_fee = (lot_ins.basic_rate * basic_hour) + (add_hour * lot_ins.additional_rate)

        # 현재 시간 기준으로, 주차 만료 예상 시간.
        now = datetime.datetime.now()
        end_time = now + timedelta(hours=parking_time)

        data = {
            "total_fee": total_fee,
            "start_time": now,
            "parking_time": parking_time,
            "lot": lot_ins.name,
            "end_time": end_time
        }
         return Response(data=data, status=status.HTTP_201_CREATED)

    # @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    # def list(self):
    #     """
    #     주차세부정보(총비용, 주차장 기본 정보)
    #     RES-total_fee, start_time, end_time, parking_time, lot(foreign)
    #     extension_rate, extension_time, original_rate(foreign key from lot)
    #     """

    # @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    # def partial_update(self, request, *args, **kwargs):
    #     """주차시간을 추가(추가결제) total_Fee 계산할 자료 제공"""
    #     """REQ - extension_time"""
    #     """RES - extension_time, extension_rate, basic_rate, basic_time"""
    #
    #     """
    #     input : parking time (2H), lot_id(2)
    #
    #     lot.basic , lot.additionalRate >> 해당 주차장의 기본 요금 * 1시간 + 추가 비용*(1시간 부터 끝나는 시간까지) == totalFee
    #     additionalRate == 추가 비용(30분 기준, 올림) *(1시간 부터 끝나는 시간까지)
    #
    #     output = totalFee, additionalRate
    #
    #     1. request 안에 있는, parking time, lot instance의 pk를 가져와야 한다.
    #     2. 가져온 lot 인스턴스의 basic rate * 1시간 과 해당 주차장의 추가 요금 값 * 1시간 이후의 값을 합한다. -> totalFee
    #     3. 추가 요금은 따로 addtionalRate에 넣어준다.
    #     4. 나온 totalFee와 additionalRate를 되돌려준다.
    #
    #     - APIView안에서 싹 다 한다 . > serialzier를 쓰지 못한다. >> 기능 구현이 빠르다. [0] -> 최우영 강사님 께 피드백
    #
    #     - serializer- method field를 이용해서 계산한, 값을 되돌려 준다. >> 굉장히 rest스러움 정석, >>> 어렵죠
    #                                                             >> self.request 에서 꺼낼 수 있습니다. APIView
    #     """
    #     pass
