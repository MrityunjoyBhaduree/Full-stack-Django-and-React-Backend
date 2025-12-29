from rest_framework import serializers

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

