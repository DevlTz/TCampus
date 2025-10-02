import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_followers = models.IntegerField(null=False, default=0)
    total_following = models.IntegerField(null=False, default=0)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers_set"
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="following_set"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} has {self.total_followers} followers"
