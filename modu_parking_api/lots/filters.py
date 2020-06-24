# from rest_framework_gis.filters import DistanceToPointFilter
#
#
# class OrderedDistanceToPointFilter(DistanceToPointFilter):
#
#     def filter_queryset(self, request, queryset, view):
#         """
#         Add sorting by distance, in addition to DinstanceToPointerFilter filter
#         """
#         if not request.query_params.get(self.point_param, None):
#             return queryset
#
#         point = self.get_filter_point(request)
#
#         queryset = super(OrderedDistanceToPointFilter, self) \
#             .filter_queryset(request, queryset, view)
#
#         queryset = queryset.distance(point)
#         queryset = queryset.order_by('%s' % 'distance')
#
#         add_distance = getattr(view, 'distance_filter_add_distance', False)
#         if add_distance:
#             queryset = self.apply_distance_field(request, queryset, view)
#
#         return queryset
#
#     def apply_distance_field(self, request, queryset, view):
#         """
#         Adds distance info (in meters) to queryset
#         """
#
#         for item in queryset:
#             item.distance = item.distance.m
#
#         return queryset
