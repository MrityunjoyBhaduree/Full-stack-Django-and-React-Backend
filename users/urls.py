from rest_framework import routers
from users.views import UserAPIViewSet

router = routers.SimpleRouter()

router.register(r"user", UserAPIViewSet, basename="user")

urlpatterns = [
  *router.urls
]
