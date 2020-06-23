from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import status, request, serializers, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

import parkings
# from parkings import models, permissions
from parkings import permissions
from parkings.serializers import ParkingSerializer


def post(self):
    pass

class ParkingViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = parkings.objects.all()
    serializer = ParkingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.CreateOwnTotalFee, IsAuthenticated)

class ParkingSerializer(serializers.ModelSerializer):
    total_fee_calc = serializers.SerializerMethodField
    t = datetime.timedelta(minutes=60)

    class Meta:
        model = parkings

    def get_total_fee_calc(self, obj, parking_time):
        return (lot.basic + (lot.additionalRate * (parking_time - t)))

        """ 
        input : parking time (2H), lot_id(2)

        lot.basic , lot.additionalRate >> 해당 주차장의 기본 요금 * 1시간 + 추가 비용*(1시간 부터 끝나는 시간까지) == totalFee
        additionalRate == 추가 비용(30분 기준, 올림) *(1시간 부터 끝나는 시간까지)

        output = totalFee, additionalRate

        1. request 안에 있는, parking time, lot instance의 pk를 가져와야 한다.
        2. 가져온 lot 인스턴스의 basic rate * 1시간 과 해당 주차장의 추가 요금 값 * 1시간 이후의 값을 합한다. -> totalFee
        3. 추가 요금은 따로 addtionalRate에 넣어준다.
        4. 나온 totalFee와 additionalRate를 되돌려준다.

        - APIView안에서 싹 다 한다 . > serialzier를 쓰지 못한다. >> 기능 구현이 빠르다. [0] -> 최우영 강사님 께 피드백

        - serializer- method field를 이용해서 계산한, 값을 되돌려 준다. >> 굉장히 rest스러움 정석, >>> 어렵죠
                                                                >> self.request 에서 꺼낼 수 있습니다. APIView
        """

        # def get(self, request):
        #     basic = request.data.get('basic')
        #     additional = request.data.get('additionalRate')
        #     t = datetime.timedelta(minutes=30)
        #
        #     if basic && additional is not None:
        #         return (basic) + (additional * t)
        #     return Response(serializer.data)
        @action(detail=False, methods=['post'], permission_classes=[AllowAny])
        def perform_create(self, serializer):
            username = request.data.get('username')
            password = request.data.get('password')
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            if user.check_password(password):
                token, __ = Token.objects.get_or_create(user=user)
                # __에는 bool이 저장
                data = {
                    "token": token.key,
                    "user": serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)

        class UserSerializer(serializers.ModelSerializer):
            full_name = serializers.SerializerMethodField()

            def get_full_name(self, obj):
                return obj.get_full_name().upper()

            class Meta:
                model = User
                fields = ('email', 'first_name', 'last_name', 'full_name')

        request.data('total_fee', 'start_time', 'parking_time')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return super().create(request, *args, **kwargs)
