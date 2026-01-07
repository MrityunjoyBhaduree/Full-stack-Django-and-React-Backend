from rest_framework_nested import routers

from post.views import PostAPIViewSet
from comment.views import CommentAPIViewSet

router = routers.SimpleRouter()

# Post Router
router.register(r"post", PostAPIViewSet, basename="post")

posts_router = routers.NestedSimpleRouter(router, r"post", lookup="post")
posts_router.register(r"comment", CommentAPIViewSet, basename="post-comment")

urlpatterns = [
  *posts_router.urls
]


