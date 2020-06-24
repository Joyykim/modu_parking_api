import math

from rest_framework import filters


class IsOwnerFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        # haversine 메소드를 이용해서 필터 구현
        # distance = haversine(lot_location, user_location)

        return queryset.filter(owner=request.user)
