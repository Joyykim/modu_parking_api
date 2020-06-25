from rest_framework import routers

from lots import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'lots', views.LotsViewSet)

urlpatterns = router.urls
