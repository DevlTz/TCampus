from django.contrib import admin
from .models import Posts
# Register your models here.

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['postedBy', 'likes', 'postedAt']
