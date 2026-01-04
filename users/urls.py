from rest_framework import routers
from users.views import UserAPIViewSet, RegisterAPIViewSet, LoginAPIViewSet, RefreshAPIViewSet

router = routers.SimpleRouter()

router.register(r"user", UserAPIViewSet, basename="user")
router.register("users/register", RegisterAPIViewSet, basename="register")
router.register("users/login", LoginAPIViewSet, basename="login")
router.register("users/refresh/token", RefreshAPIViewSet, basename="refresh_token")


urlpatterns = [
  *router.urls,
]
