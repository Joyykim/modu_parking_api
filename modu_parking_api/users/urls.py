from rest_framework import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)
urlpatterns = router.urls


