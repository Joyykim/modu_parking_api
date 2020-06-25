from rest_framework import routers

from parkings.views import ParkingViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'parkings', ParkingViewSet)
urlpatterns = router.urls
