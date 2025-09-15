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

class Event(models.Model):
    title = models.CharField("Título: ", max_length=255)
    date_evento = models.DateTimeField("Data e hora do evento")
    local = models.CharField("Local / link", max_length=512)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date_evento"]  

    def __str__(self):
        return f"{self.title} — {self.date_evento:%Y-%m-%d %H:%M}"
