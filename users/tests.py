import pytest
from rest_framework import status
from users.models import User


data_user = {
  "username": "test_user",
  "email": "test@gmail.com",
  "first_name": "Test",
  "last_name": "User",
  "password": "test_password"
}
data_superuser = {
  "username": "test_superuser",
  "email": "testsuperuser@gmail.com",
  "first_name": "Test",
  "last_name": "superuser",
  "password": "test_password"
}


@pytest.mark.django_db
def test_create_user():
  user = User.objects.create_user(**data_user)
  assert user.username == data_user["username"]
  assert user.email == data_user["email"]
  assert user.first_name == data_user["first_name"]
  assert user.last_name == data_user["last_name"]


@pytest.mark.django_db
def test_create_superuser():
  user = User.objects.create_superuser(**data_superuser)
  assert user.username == data_superuser["username"]
  assert user.email == data_superuser["email"]
  assert user.first_name == data_superuser["first_name"]
  assert user.last_name == data_superuser["last_name"]
  assert user.is_superuser == True
  assert user.is_staff == True


@pytest.fixture
def user(db) -> User:
  return User.objects.create_user(**data_user)


class TestAuthenticationViewSet:
  endpoint = "/api/v1/"

  def test_login(self, client, user):
    data = {
      "email": user.email,
      "password": "test_password",

    }

    response = client.post(self.endpoint + "users/login/",
                           data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["access"]
    assert response.data["user"]["id"] == user.public_id.hex
    assert response.data["user"]["username"] == user.username
    assert response.data["user"]["email"] == user.email


  @pytest.mark.django_db
  def test_register(self, client):
    data = {
      "username": "johndoe",
      "email": "johndoe@yopmail.com",
      "password": "test_password",
      "first_name": "John",
      "last_name": "Doe"
    }

    response = client.post(self.endpoint + "users/register/", data)

    assert response.status_code == status.HTTP_201_CREATED


  def test_refresh(self, client, user):
    data = {
      "email": user.email,
      "password": "test_password"
    }

    response = client.post(self.endpoint + "users/login/", data, format="json")

    assert response.status_code == status.HTTP_200_OK

    data_refresh = {
      "refresh": response.data["refresh"]
    }

    response = client.post(self.endpoint + "users/refresh/token/", data_refresh)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["access"]

class TestUserViewSet:
  endpoint = "/api/v1/user/"


  def test_list(self, client, user):
    client.force_authenticate(user=user)
    response = client.get(self.endpoint)
    assert response.status_code == status.HTTP_200_OK

  def test_retrieve(self, client, user):
    client.force_authenticate(user=user)
    response = client.get(self.endpoint + str(user.public_id) + "/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == user.public_id.hex
    assert response.data["username"] == user.username
    assert response.data["email"] == user.email

  def test_create(self, client, user):
    client.force_authenticate(user=user)

    data = {}
    response = client.post(self.endpoint, data)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


  def test_update(self, client, user):
    client.force_authenticate(user=user)

    data = {
      "username": "test_user_updated"
    }
    response = client.patch(self.endpoint + str(user.public_id) + "/", data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == data["username"]
