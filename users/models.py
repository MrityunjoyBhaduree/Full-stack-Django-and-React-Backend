from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


from abstract.models import AbstractModel, AbstractManager




class UserManager(BaseUserManager, AbstractManager):

  def create_user(self, username, email, password=None, **kwargs):
    """
    Create and return a 'User' with an email, phone number, username and password
    :param username:
    :param email:
    :param password:
    :param kwargs:
    :return:
    """
    if username is None:
      raise TypeError('Users must have a username.')
    if email is None:
      raise TypeError('Users must have an email.')
    if password is None:
      raise TypeError("User must have an email.")

    user = self.model(username=username, email=self.normalize_email(email), **kwargs)
    user.set_password(password)
    user.save(using=self.db)

    return user

  def create_superuser(self, username, email, password, **kwargs):
    """
    Create and return a 'User' with superuser (admin) permissions.
    :param username:
    :param email:
    :param password:
    :param kwargs:
    :return:
    """
    if password is None:
      raise TypeError('Superusers must have a password.')
    if email is None:
      raise TypeError('Superusers must have an email.')
    if username is None:
      raise TypeError('Superusers must have an username.')

    user = self.create_user(username, email, password, **kwargs)
    user.is_superuser = True
    user.is_staff = True
    user.save(using=self.db)

    return user



class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=255, db_index=True, unique=True)
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)

  email = models.EmailField(db_index=True, unique=True)
  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)

  bio = models.TextField(null=True)
  avatar = models.ImageField(null=True)

  posts_liked = models.ManyToManyField("post.Post", related_name="liked_by")

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  objects = UserManager()

  def __str__(self):
    return f"{self.email}"

  @property
  def name(self):
    return f"{self.first_name} {self.last_name}"

  def like(self, post):
    """
    Like 'post' if it hasn't been done yet
    :param post:
    :return:
    """
    return self.posts_liked.add(post)

  def remove_like(self, post):
    """
    Remove a like from a post
    :param post:
    :return:
    """
    return self.posts_liked.remove(post)


  def has_liked(self, post):
    """
    Return True if the user has liked a 'post'; else Fals
    :param post:
    :return:
    """
    return self.posts_liked.filter(pk=post.pk).exists()


