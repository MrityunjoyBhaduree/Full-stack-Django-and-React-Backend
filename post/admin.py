from django.contrib import admin

from post.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ["id", "public_id", "author", "body"]
