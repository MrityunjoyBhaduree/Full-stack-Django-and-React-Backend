from typing import Any

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from users.models import User


class UserSerializer(serializers.ModelSerializer):
  id = serializers.SerializerMethodField(method_name="get_id")
  created = serializers.DateTimeField(read_only=True)
  updated = serializers.DateTimeField(read_only=True)

  @staticmethod
  def get_id(obj):
    return obj.public_id.hex


  class Meta:
    model = User
    fields = ["id", "username", "first_name", "last_name",
              "email", "is_active", "created", "updated"]
    read_only_field = ["is_active"]


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
    fields = ["id", "email", "username", "first_name", "last_name", "password"]


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