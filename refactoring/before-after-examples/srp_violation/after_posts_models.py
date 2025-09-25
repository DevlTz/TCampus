import uuid
from users.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.utils import timezone

fileStorage = FileSystemStorage(location=settings.MEDIA_ROOT)

#Managers
class PostsManager(models.Manager):
    def get_feed_for_user(self, user):
        """
        Retorna um queryset com os posts do feed de um usuário específico,
        contendo apenas posts de pessoas que ele segue e ordenado por data.
        """
        return self.get_queryset().filter(
            postedBy__in=user.following.all()
        ).order_by('-postedAt')
    
class EventsManager(models.Manager):
    def get_feed_for_user(self, user, scope='following'):
        """
        Retorna o queryset de EVENTOS do feed de um usuário,
        respeitando o escopo ('following' ou 'all').
        """
        now = timezone.now()
        if scope == 'all':
            # Eventos futuros de todos os usuários.
            return self.get_queryset().filter(
                event_date__gte=now
            ).order_by('-event_date')
        else:
            #  Eventos de usuários seguidos.
            return self.get_queryset().filter(
                postedBy__in=user.following.all()
            ).order_by('-event_date')


class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    likes = models.IntegerField(default=0)
    postedAt = models.DateTimeField(auto_now_add=True, editable=False)
    likedBy = models.ManyToManyField(User, related_name="posts_likes")
    postedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts_postedBy", editable=False)
    text = models.TextField(max_length=250, editable=False, default=" ")
    image = models.ImageField(editable=False, default=None, storage=fileStorage)
    objects = PostsManager()

    def __str__(self):
        return f"{self.id} has {self.likes} likes"
    
    

class Events(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("Title: ", max_length=255)
    event_date = models.DateTimeField("Event Date and Time:")
    locate = models.CharField(max_length=512) # can be text or URL 
    postedAt = models.DateTimeField(auto_now_add=True, editable=False) 
    postedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events_postedBy", editable=False)
    objects = models.Manager()
    participants = models.ManyToManyField(User, related_name="events_participants", blank=True)
    participants_count = models.PositiveIntegerField(default=0)
    objects = EventsManager()

    class Meta:
        ordering = ["-event_date"]

    def __str__(self):
        return f"{self.title} — {self.event_date:%Y-%m-%d %H:%M}"
    
    @property
    def total_participants(self):
        """
        Returns the total number of participants for the event.
        """
        # In case of inconsistency, fallback to count()
        if self.participants_count is None:
            return self.participants.count()
        return self.participants_count
    
    



    