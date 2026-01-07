from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from abstract.serializers import AbstractSerializer
from post.models import Post


class PostSerializer(AbstractSerializer):
  author = serializers.SerializerMethodField(method_name="get_author")
  liked = serializers.SerializerMethodField(method_name="get_liked")
  likes_count = serializers.SerializerMethodField(method_name="get_likes_count")
  # date = serializers.SerializerMethodField(method_name="get_date")
  # time = serializers.SerializerMethodField(method_name="get_time")

  def get_liked(self, obj):
    request = self.context.get("request", None)
    if request is None or request.user.is_anonymous:
      return False
    return request.user.has_liked(obj)

  @staticmethod
  def get_likes_count(obj):
    return obj.liked_by.count()

  @staticmethod
  def get_author(obj):
    author = {
      "id": obj.author.public_id.hex,
      "username": obj.author.username,
      "first_name": obj.author.first_name,
      "last_name": obj.author.last_name,
      "bio": obj.author.bio,
      "avatar": obj.author.avatar if obj.author.avatar else None,
      "email": obj.author.email,
      "is_active": obj.author.is_active,
      "created": obj.author.created,
      "updated": obj.author.updated
    }
    return author

  # @staticmethod
  # def get_date(obj):
  #   return obj.created.date()
  #
  # @staticmethod
  # def get_time(obj):
  #   return obj.created.strftime("%I:%M:%S %p")


  class Meta:
    model = Post
    fields = ["id", "author", "body", "edited", "liked", "likes_count",
              "created", "updated"]
    read_only_fields = ["edited"]

  def validate_author(self, value):
    if self.context["request"].user != value:
      raise ValidationError("You can't create a post for another user.")
    return value


  def create(self, validated_data):
    user = self.context["request"].user
    body = validated_data.get("body")
    post = Post.objects.create(author=user, body=body)
    post.save()
    return post

  def update(self, instance, validated_data):
    instance.body = validated_data.get("body", instance.body)
    instance.edited = True
    instance.save()
    return instance
