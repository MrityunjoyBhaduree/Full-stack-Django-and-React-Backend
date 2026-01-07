from rest_framework import routers

from post.views import PostAPIViewSet


router = routers.SimpleRouter()

router.register(r"post", PostAPIViewSet, basename="post")

urlpatterns = [
  *router.urls,
]
