from rest_framework import routers

from parkings import views
from parkings.views import ParkingViewSet
from django.urls import path, include

router = routers.SimpleRouter(trailing_slash=False)
router.register('', views.ParkingViewSet)
urlpatterns = router.urls
