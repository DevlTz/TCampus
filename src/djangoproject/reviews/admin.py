from django.contrib import admin
from .models import ReviewTeacher

# Register your models here.


@admin.register(ReviewTeacher)
class PostsAdmin(admin.ModelAdmin):
    list_display = ["teacher", "student", "score", "created_at"]
