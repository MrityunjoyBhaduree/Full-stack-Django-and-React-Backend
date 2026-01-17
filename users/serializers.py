from typing import Any
from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from users.models import User
from abstract.serializers import AbstractSerializer


class UserSerializer(AbstractSerializer):

  posts_count = serializers.SerializerMethodField(method_name="get_posts_count")

  @staticmethod
  def get_posts_count(obj):
    return obj.post_set.all().count()


  def to_representation(self, instance):
    representation = super().to_representation(instance)
    if not representation["avatar"]:
      representation["avatar"] = settings.DEFAULT_AVATAR_URL
      return representation
    if settings.DEBUG: # debug enabled for dev
      request = self.context.get("request")
      representation["avatar"] = request.build_absolute_uri(
        representation["avatar"]
      )
    return representation

  class Meta:
    model = User
    fields = ["id", "username", "name", "first_name", "last_name", "bio", "avatar",
               "email", "is_active", "created", "updated", "posts_count"]
    read_only_field = ["is_active"]


  def update(self, instance, validated_data):
    instance.first_name = validated_data.get("first_name", instance.first_name)
    instance.last_name = validated_data.get("last_name", instance.last_name)
    instance.bio = validated_data.get("bio", instance.bio)
    instance.avatar = validated_data.get("avatar", instance.avatar)
    # Only update avatar if a new file is provided
    avatar = validated_data.get("avatar")
    if avatar:
        instance.avatar = avatar
    instance.save()
    return instance


class RegisterSerializer(UserSerializer):
  """
  Registration serializer for requests and user creation
  """

  # Making sure the password is at least 8 characters long, and no longer than 128
  # and can't be read by the user

  password = serializers.CharField(max_length=128, min_length=8, write_only=True,
                                   required=True)

  class Meta:
    model = User
    # List of all the fields that can be included in a request or a response
    fields = ["id", "bio", "avatar", "email", "username", "first_name",
              "last_name", "password"]


  def create(self, validated_data):
    # Use the create_user method we wrote earlier for the UserManager
    # to create a new user
    return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):

  def validate(self, attrs):
    data = super().validate(attrs)
    refresh = self.get_token(self.user)

    data["user"] = UserSerializer(self.user).data
    data["refresh"] = str(refresh)
    data["access"] = str(refresh.access_token)

    if api_settings.UPDATE_LAST_LOGIN:
      update_last_login(None, self.user)
    return data