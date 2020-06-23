from rest_framework import routers
from parkings.views import ParkingViewSet
from django.urls import path, include

router = routers.SimpleRouter(trailing_slash=False)
router.register('parkingviewset', views.ParkingViewSet.as_view())
urlpatterns = router.urls
