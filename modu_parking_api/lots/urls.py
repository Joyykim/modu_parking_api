from rest_framework import routers

from lots.views import LotsViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('lots', LotsViewSet)
urlpatterns = router.urls
