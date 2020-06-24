from rest_framework import routers

from lots.views import LotsViewSet

router = routers.SimpleRouter()
router.register('lots/', LotsViewSet)
urlpatterns = router.urls