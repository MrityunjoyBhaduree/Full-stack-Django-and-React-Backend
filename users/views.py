from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView
from users.serializers import UserSerializer, RegisterSerializer, LoginSerializer
from users.models import User



class UserAPIViewSet(viewsets.ModelViewSet):
  http_method_names = ["patch", "get"]
  permission_classes = [IsAuthenticated]
  serializer_class = UserSerializer


  def get_queryset(self):
    if self.request.user.is_superuser:
      return User.objects.all()
    return User.objects.exclude(is_superuser=True)

  def get_object(self):
    obj = User.objects.get_object_by_public_id(self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj


class RegisterAPIViewSet(ViewSet):
  serializer_class = RegisterSerializer
  permission_classes = [AllowAny]
  http_method_names = ["post"]

  def create(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    res = {
      "refresh": str(refresh),
      "access": str(refresh.access_token),
    }
    return Response({
      "user": serializer.data,
      "refresh": res["refresh"],
      "token": res["access"]
    }, status=status.HTTP_201_CREATED
    )

class LoginAPIViewSet(ViewSet):
  serializer_class = LoginSerializer
  permission_classes = [AllowAny]
  http_method_names = ["post"]

  def create(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data)
    try:

      serializer.is_valid(raise_exception=True)
    except TokenError as e:
      raise InvalidToken(e.args[0])
    return Response(serializer.validated_data, status=status.HTTP_200_OK)

class RefreshAPIViewSet(ViewSet, TokenRefreshView):
  permission_classes = [AllowAny]
  http_method_names = ["post"]


  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)

    try:
      serializer.is_valid(raise_exception=True)
    except TokenError as e:
      raise InvalidToken(e.args[0])

    return Response(serializer.validated_data, status=status.HTTP_200_OK)