from django.http.response import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from abstract.views import AbstractViewSet
from comment.models import Comment
from comment.serilaizers import CommentSerializer
from CoreRoot.permissions import UserPermission


class CommentAPIViewSet(AbstractViewSet):
  """
  GET    /api/v1/post/<post_pk>/comment/          → List all comments for a post
  GET    /api/v1/post/<post_pk>/comment/<comment_pk>/    → Retrieve a specific comment
  POST   /api/v1/post/<post_pk>/comment/          → Create a comment for a post
  Put  /api/v1/post/<post_pk>/comment/<comment_pk>/    → Update a specific comment
  DELETE /api/v1/post/<post_pk>/comment/<comment_pk>/    → Delete a specific comment

  """
  http_method_names = ["post", "get", "put", "delete"]
  permission_classes = [UserPermission]
  serializer_class = CommentSerializer


  def get_queryset(self):
    if self.request.user.is_superuser:
      return Comment.objects.all()

    post_pk = self.kwargs["post_pk"]
    if post_pk is None:
      return Http404
    queryset = Comment.objects.filter(post__public_id=post_pk)

    return queryset

  def get_object(self):
    obj = Comment.objects.get_object_by_public_id(self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)

    return obj

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(
      data=request.data,
      context={
        "request": request,
        "post_pk": self.kwargs["post_pk"]
      }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(data=request.data, instance=instance,
                                     partial=False)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    if instance is not None:
      self.perform_destroy(instance)
      return Response({"message": "Comment Deleted."}, status=status.HTTP_204_NO_CONTENT)
    return Response({"message": "Unable to delete comment"},
                    status=status.HTTP_400_BAD_REQUEST)


  @action(methods=["post"], detail=True)
  def like(self, request, *args, **kwargs):
    comment = self.get_object()
    user = self.request.user

    user.like_comment(comment)
    serializer = self.serializer_class(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @action(methods=["post"], detail=True)
  def remove_like(self, request, *args, **kwargs):
    comment = self.get_object()
    user = self.request.user

    user.remove_like_comment(comment)

    serializer = self.serializer_class(comment)

    return Response(serializer.data, status=status.HTTP_200_OK)