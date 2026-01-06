from rest_framework import routers

from post.views import PostAPIViewSet


router = routers.SimpleRouter()

router.register(r"post", PostAPIViewSet, basename="user")

urlpatterns = [
  *router.urls,
]
