from rest_framework import serializers

from abstract.serializers import AbstractSerializer
from comment.models import Comment
from post.models import Post
from django.conf import settings


class CommentSerializer(AbstractSerializer):


  author = serializers.SerializerMethodField(method_name="get_author")
  post = serializers.SerializerMethodField(method_name="get_post")
  liked = serializers.SerializerMethodField(method_name="get_liked")
  likes_count = serializers.SerializerMethodField(
    method_name="get_likes_count")


  def get_liked(self, obj):
    request = self.context.get("request", None)
    if request is None or request.user.is_anonymous:
      return False
    return request.user.has_liked_comment(obj)

  @staticmethod
  def get_likes_count(obj):
    return obj.commented_by.count()

  def get_author(self, obj):
    request = self.context.get("request")
    avatar_url = None
    if obj.author.avatar and hasattr(obj.author.avatar, "url"):
        if request:
            avatar_url = request.build_absolute_uri(obj.author.avatar.url)
        else:
            avatar_url = obj.author.avatar.url
    else:
        if request:
            avatar_url = request.build_absolute_uri(settings.DEFAULT_AVATAR_URL)
        else:
            avatar_url = settings.DEFAULT_AVATAR_URL

    author = {
        "id": obj.author.public_id.hex,
        "username": obj.author.username,
        "first_name": obj.author.first_name,
        "last_name": obj.author.last_name,
        "name": obj.author.name,
        "bio": obj.author.bio,
        "avatar": avatar_url,
        "email": obj.author.email,
        "is_active": obj.author.is_active,
        "created": obj.author.created,
        "updated": obj.author.updated
    }
    return author


  @staticmethod
  def get_post(obj):
    return obj.post.public_id.hex



  class Meta:
    model = Comment
    fields = ["id", "post", "author", "body", "edited", "liked", "likes_count",
              "created", "updated"]
    read_only_fields = ["edited"]


  def validate_post(self, value):
    if self.instance:
      return self.instance.post
    return value



  def create(self, validated_data):
    author = self.context["request"].user
    body = validated_data.get("body")
    post_pk = self.context["post_pk"]
    post = Post.objects.get(public_id=post_pk)

    comment = Comment.objects.create(author=author, body=body, post=post)
    comment.save()
    return comment


  def update(self, instance, validated_data):
    instance.body = validated_data.get("body", instance.body)
    instance.edited = True
    instance.save()
    return instance



