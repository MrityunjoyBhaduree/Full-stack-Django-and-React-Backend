from rest_framework import serializers


class AbstractSerializer(serializers.ModelSerializer):
  id = serializers.SerializerMethodField(method_name="get_id")
  created = serializers.DateTimeField(read_only=True)
  updated = serializers.DateTimeField(read_only=True)

  @staticmethod
  def get_id(obj):
    return obj.public_id.hex
