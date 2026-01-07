from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from abstract.serializers import AbstractSerializer
from users.models import User
from users.serializers import UserSerializer
from comment.models import Comment
from post.models import Post


class CommentSerializer(AbstractSerializer):


  author = serializers.SerializerMethodField(method_name="get_author")
  post = serializers.SerializerMethodField(method_name="get_post")

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

  @staticmethod
  def get_post(obj):
    return obj.post.public_id.hex



  class Meta:
    model = Comment
    fields = ["id", "post", "author", "body", "edited", "created", "updated"]
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



