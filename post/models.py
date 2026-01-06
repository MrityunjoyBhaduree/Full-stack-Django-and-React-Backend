from django.db import models

from abstract.models import AbstractModel, AbstractManager

class PostManager(AbstractManager):
  pass


class Post(AbstractModel):
  author = models.ForeignKey("users.User", on_delete=models.CASCADE)
  body = models.TextField()
  edited = models.BooleanField(default=False)

  objects = PostManager()

  def __str__(self):
    return f"{self.author.name}"

  class Meta:
    db_table = "post"
