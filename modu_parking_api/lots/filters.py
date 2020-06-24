from haversine import haversine
from rest_framework import filters


class MapFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        distance = haversine(lot_location, user_location)

        return queryset.filter(owner=request.user)
