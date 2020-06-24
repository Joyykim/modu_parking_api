from rest_framework import routers

from lots import views

router = routers.SimpleRouter(trailing_slash=False)
router.register('lots/', views.LotsViewSet)

urlpatterns = router.urls
