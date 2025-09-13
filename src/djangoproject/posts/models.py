import uuid
from users.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
# Create your models here.

fileStorage = FileSystemStorage(location=settings.MEDIA_ROOT)


class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    likes = models.IntegerField(default=0)
    postedAt = models.DateTimeField(auto_now_add=True, editable=False)
    likedBy = models.ManyToManyField(User, related_name="posts_likes")
    postedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts_postedBy", editable=False)
    text = models.TextField(max_length=250, editable=False, default=" ")
    image = models.ImageField(editable=False, default=None, storage=fileStorage)


    objects = models.Manager()
    
    def __str__(self):
        return f"{self.id} has {self.likes} likes"

