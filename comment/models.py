from django.db import models

from abstract.models import AbstractModel, AbstractManager


class CommentManager(AbstractManager):
  pass


class Comment(AbstractModel):
  post = models.ForeignKey("post.Post", on_delete=models.PROTECT)
  author = models.ForeignKey("users.User", on_delete=models.PROTECT)

  body = models.TextField()
  edited = models.BooleanField(default=False)

  objects = CommentManager()


  def __str__(self):
    return self.author.name
