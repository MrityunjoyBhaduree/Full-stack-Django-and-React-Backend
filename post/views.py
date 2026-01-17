from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from abstract.views import AbstractViewSet
from post.models import Post
from post.serializers import PostSerializer
from CoreRoot.permissions import UserPermission



class PostAPIViewSet(AbstractViewSet):
  """
  POST /api/v1/post/              → Create a post / List all posts
  GET  /api/v1/post/              → List all posts
  GET  /api/v1/post/<post_id>/    → Retrieve a single post
  PATCH /api/v1/post/<post_id>/   → Update a post
  DELETE /api/v1/post/<post_id>/  → Delete a post

  """
  http_method_names = ["post", "get", "put", "delete"]
  permission_classes = [UserPermission]
  serializer_class = PostSerializer


  def get_queryset(self):
    queryset = Post.objects.all()

    author_public_id = self.request.query_params.get("author__public_id")

    if author_public_id:
      queryset = queryset.filter(author__public_id=author_public_id)

    return queryset
    # return Post.objects.all()

  def get_object(self):
    obj = Post.objects.get_object_by_public_id(self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(
      data=request.data, instance=instance, partial=False
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    if instance is not None:
      self.perform_destroy(instance)
      return Response({"message": "Post Deleted."}, status=status.HTTP_204_NO_CONTENT)
    return Response({"message": "Unable to delete the post."},
                    status=status.HTTP_400_BAD_REQUEST)

  @action(methods=["post"], detail=True)
  def like(self, request, *args, **kwargs):
    post = self.get_object()
    user = self.request.user

    user.like(post)
    serializer = self.serializer_class(post)
    return Response(serializer.data, status=status.HTTP_200_OK)


  @action(methods=["post"], detail=True)
  def remove_like(self, request, *args, **kwargs):
    post = self.get_object()
    user = self.request.user

    user.remove_like(post)
    serializer = self.serializer_class(post)
    return Response(serializer.data, status=status.HTTP_200_OK)